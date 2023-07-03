from rest_framework.permissions import (
    IsAuthenticated,  
    BasePermission, 
    AllowAny
)
from rest_framework.views import APIView
from ..models import *
from ..serializers import *
from ..auth.auth_backend import CheckIfPasswordWasChanged
from .utils.non_working_days import NonWorkingDays
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.db import connection
from .utils.cursor_to_array_of_dicts import cursor_to_array_of_dicts
from .utils.weekdays import weekdays
from ..employee.utils.image_actions import map_images
import datetime as dt

class Holidays(APIView):
    # permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get_holidays(self, year):
        return NonWorkingDays(year).non_working_days

    def get(self, request):
        non_working_days = self.get_holidays(request.query_params.get("year"))
        return Response(data=non_working_days, status=status.HTTP_200_OK)
    
class HolidaysForThreeYears(APIView):

    def get_holidays(self, year):
        non_working_days_current_year = NonWorkingDays(year).non_working_days_with_year
        non_working_days_prev_year = NonWorkingDays(str(int(year) - 1)).non_working_days_with_year
        non_working_days_next_year = NonWorkingDays(str(int(year) +1)).non_working_days_with_year
        non_working_days = non_working_days_prev_year + non_working_days_current_year + non_working_days_next_year
        return non_working_days

    def get(self, request):
        return Response(data=self.get_holidays(int(request.query_params.get("year"))), status=status.HTTP_200_OK)
    
class Employees(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get(self, request):
        user = request.user
        employee = Employee.objects.get(user = user)
        if employee.is_owner:
            employees = Employee.objects.filter(business_activity_id = employee.business_activity_id)
            employees_serializer = OwnerEmployeesSerializer(employees, many=True)
            return Response(data=employees_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeApointmentsApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]
    earliest_date = None
    latest_date = None
    user = None

    def set_earliest_and_latest_date(self, data):
        self.earliest_date = data[0]["date"]
        self.latest_date = data[len(data) -1]["date"]

    def group_non_default_availability(self, availability, dates):
        days = []
        for day in dates:
            day_items = {
                "date": day["date"],
                "weekday": str(dt.datetime.strptime(day["date"], "%Y-%m-%d").date().strftime("%A")).lower(),
                "is_default": False,
                "is_holiday": False,
                "is_appointment": False,
                "is_free": False,
                "breaks": [],
                "work_time": {
                    "start_time": None,
                    "end_time": None,
                }
            }
            exists = False
            for avail in availability:
                if avail["date"] == day["date"]:
                    exists = True
                    if avail["is_break"] == 1:
                        day_items["breaks"].append({
                            "start_time": avail["start_time"],
                            "end_time": avail["end_time"],
                        })
                    elif avail["is_free"] == 1:
                        day_items["is_free"] = 1
                        break
                    else:
                        day_items["work_time"]["start_time"] = avail["start_time"]
                        day_items["work_time"]["end_time"] = avail["end_time"]
            if exists:
                days.append(day_items)
        return days


    def group_default_availability(self, data):
        days = []
        for day in weekdays:
            day_items = {
                "weekday": day,
                "is_default": True,
                "is_holiday": False,
                "is_appointment": False,
                "is_free": False,
                "breaks": [],
                "work_time": {
                    "start_time": None,
                    "end_time": None,
                }
            }
            for avail in data:
                if avail["weekday"] == day:
                    if avail["is_break"] == 1:
                        day_items["breaks"].append({
                            "start_time": avail["start_time"],
                            "end_time": avail["end_time"],
                        })
                    elif avail["is_free"] == 1:
                        day_items["is_free"] = 1
                        break
                    else:
                        day_items["work_time"]["start_time"] = avail["start_time"]
                        day_items["work_time"]["end_time"] = avail["end_time"]
            days.append(day_items)
        return days

    def get_employee_non_default_availability(self, dates):
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT 
                    sea.start_time, sea.end_time, sea.is_default, sea.is_free, 0 as 'is_holiday',
                    sea.is_break, sea.`weekday`, 0 AS 'is_appointment', sea.`date`
                FROM salon_user su
                JOIN salon_employee se ON se.user_id = su.id
                JOIN salon_employeeavailabilityconfiguration seac ON seac.employee_id = se.id
                JOIN salon_employeeavailability sea ON sea.availability_config_id = seac.id
                WHERE su.id = %s
                    AND sea.is_default = 0
                    AND sea.`date` >= %s
                    AND sea.`date` <= %s
            """
        , [self.user.pk, self.earliest_date, self.latest_date])
        return(self.group_non_default_availability(cursor_to_array_of_dicts(cursor), dates))

    def get_employee_default_availability(self):
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT 
                    sea.start_time, sea.end_time, sea.is_default, sea.is_free,
                    sea.is_break, sea.`weekday`, 0 AS 'is_appointment', 0 as 'is_holiday'
                FROM salon_user su
                JOIN salon_employee se ON se.user_id = su.id
                JOIN salon_employeeavailabilityconfiguration seac ON seac.employee_id = se.id
                JOIN salon_employeeavailability sea ON sea.availability_config_id = seac.id
                WHERE su.id = %s
                    AND sea.is_default = 1
            """
        , [self.user.pk])
        return(self.group_default_availability(cursor_to_array_of_dicts(cursor)))
    
    def group_appointments(self, appointments, dates):
        days = []
        for day in dates:
            day_items = {
                "date": day["date"],
                "weekday": str(dt.datetime.strptime(day["date"], "%Y-%m-%d").date().strftime("%A")).lower(),
                "is_appointment": True,
                "is_default": False,
                "is_holiday": False,
                "is_free": False,
                "day_appointments": [],
            }
            exists = False
            for appointment in appointments:
                if appointment["date"] == day["date"]:
                    exists = True
                    day_items["day_appointments"].append(appointment)
            if exists:
                days.append(day_items)
        return days
    
    def get_employee_appointments(self, dates):
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT 
                    suc.first_name AS 'client_name', suc.last_name AS 'client_last_name', suc.email AS 'client_mail',
                    ss.duration, ss.`name` AS 'service_name', ss.price,
                    sa.`date`, LOWER(DAYNAME(sa.`date`)) AS 'day_name', sa.time_start,  
                    DATE_FORMAT((Time(sa.time_start) + INTERVAL ss.duration MINUTE), '%%H:%%i') as 'end_time', 1 AS 'is_appointment', 0 as 'is_holiday'
                FROM salon_user su
                JOIN salon_employee se ON se.user_id = su.id
                JOIN salon_service ss ON ss.employee_id = se.id
                JOIN salon_cosmeticprocedure scp ON scp.service_id = ss.id
                JOIN salon_appointment sa ON scp.appointment_id = sa.id
                JOIN salon_user suc ON scp.client_id = suc.id
                WHERE su.id = %s
                    AND sa.`date` >= %s
		            AND sa.`date` <= %s
                ORDER BY sa.date, sa.time_start
            """
        , [self.user.pk, self.earliest_date, self.latest_date])
        return(self.group_appointments(cursor_to_array_of_dicts(cursor), dates))
    
    def combine_appointments_and_availability(self, dates, appointments, def_avail, non_def_avail):
        holidays = HolidaysForThreeYears()
        non_working_dates = holidays.get_holidays(dates[0]["date"][:4])
        non_default_dates = []
        combined_data = []
        for day in dates:
            weekday = str(dt.datetime.strptime(day["date"], "%Y-%m-%d").date().strftime("%A")).lower(),
            for appointment in appointments:
                if appointment["date"] == day["date"]:
                    combined_data.append(appointment)
            for non_def_av in non_def_avail:
                if non_def_av["date"] == day["date"]:
                    non_default_dates.append(day["date"])
                    combined_data.append(non_def_av)
            for date in non_working_dates:
                if date == day["date"]:
                    non_default_dates.append(date)
                    combined_data.append({
                        "date": date,
                        "is_appointment": False,
                        "is_default": False,
                        "is_holiday": True,
                        "is_free": True,
                        "weekday": weekday[0],
                    })
            for def_av in def_avail:
                if weekday[0] == def_av["weekday"] and day["date"] not in non_default_dates:
                    combined_data.append({**def_av, "date": day["date"]})
        return { "events": combined_data, "def_avail":  def_avail }
    
    def get_employee_calendar(self, dates):
        appointments = self.get_employee_appointments(dates)
        default_availability = self.get_employee_default_availability()
        non_default_availability = self.get_employee_non_default_availability(dates)
        return self.combine_appointments_and_availability(dates, appointments, default_availability, non_default_availability)

    def post(self, request):
        user = request.user
        chosen_employee = request.query_params.get("employee")
        employee = Employee.objects.get(user_id=user)
        if employee.is_owner:
            chosen_employee = Employee.objects.get(pk=chosen_employee)
            self.user = User.objects.get(pk=chosen_employee.user_id)
        data = request.data
        if type(data) is not list:
            data = list(data.values())
        self.set_earliest_and_latest_date(data)
        if request.query_params.get("operation") == "get":
            return Response(data=self.get_employee_calendar(data), status=status.HTTP_200_OK)

class CompleteVisitInfo(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]
    employee = None
    user = None

    def map_visit_info(self, data):
        class Img():
            def __init__(self, content):
                self.content = content
        
        service_info = {
            "business": {
                "business_name": data[0]["business_name"],
                "business_house_number": data[0]["business_house_number"],
                "business_city": data[0]["business_city"],
                "business_post_code": data[0]["business_post_code"],
                "business_street": data[0]["business_street"],
                "business_apartment_number": data[0]["business_apartment_number"],
            },
            "employees": [],
        }

        for item in data:
            avatar = {
                "image_id": None,
                "file_type": None,
                "image_id": None,
            }
            if item["content"]:
                avatar = map_images(Img(item["content"]))
            service_info["employees"].append({
                "avatar": avatar,
                "business_activity_id": item["business_activity_id"],
                "id": item["employee_id"],
                "is_owner": item["is_owner"],
                "service": {
                    "category_id": item["category_id"],
                    "category_name": item["category_name"],
                    "duration": item["duration"],
                    "price": item["price"],
                    "service_id": item["service_id"],
                    "service_name": item["service_name"],
                },
                "spec": {
                    "id": item["spec_id"],
                    "name": item["spec_name"],
                },
                "user": {
                    "email": item["email"],
                    "first_name": item["first_name"],
                    "last_name": item["last_name"],
                    "phone_number": item["phone_number"]
                },
            })
        
        return service_info

    def get_complete_visit_info(self, data):
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT 
                    su.email, su.first_name, su.last_name, su.phone_number, se.id as 'employee_id',
                    ses.id as 'spec_id', ses.name as 'spec_name', se.id as 'employee_id',
                    se.is_owner, se.business_activity_id, sea.content,
                    sba.name as 'business_name', sba.house_number as 'business_house_number',
                    sba.city as 'business_city', sba.post_code as 'business_post_code',
                    sba.street as 'business_street', sba.apartment_number as 'business_apartment_number',
                    ss.price, ss.id as 'service_id', ss.name as 'service_name', ss.duration, ssc.id as 'category_id',
                    ssc.name as 'category_name'
                from salon_employee se
                join salon_service ss on ss.employee_id = se.id
                join salon_user su on su.id = se.user_id
                join salon_employeespecialization ses on ses.id = se.spec_id
                left join salon_employeeavatar sea on sea.employee_id = se.id
                join salon_businessactivity sba on sba.id = se.business_activity_id
                join salon_servicecategory ssc on ssc.id = ss.service_category_id
                where se.business_activity_id = %s
                    and ss.name = %s
            """
        , [self.employee.business_activity_id, data["name"]])
        return(cursor_to_array_of_dicts(cursor))

    def post(self, request):
        operation = request.query_params.get("operation")
        data = request.data
        self.user = request.user
        self.employee = Employee.objects.get(user_id=self.user.pk)
        chosen_employee = request.query_params.get("employee")

        if self.employee.is_owner:
            chosen_employee = Employee.objects.get(pk=chosen_employee)
            self.employee = chosen_employee
            self.user = User.objects.get(pk=chosen_employee.user_id)
        if operation == "get":
            visit_info = self.map_visit_info(self.get_complete_visit_info(data))
            return Response(data=visit_info, status=status.HTTP_200_OK)
