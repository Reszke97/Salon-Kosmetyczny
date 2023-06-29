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
import datetime as dt

class Holidays(APIView):
    # permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get_holidays(self, year):
        return NonWorkingDays(year).non_working_days

    def get(self, request):
        non_working_days = self.get_holidays(request.query_params.get("year"))
        return Response(data=non_working_days, status=status.HTTP_200_OK)
    
class HolidaysForThreeYears(APIView):
    def get(self, request):
        non_working_days_current_year = NonWorkingDays(request.query_params.get("year")).non_working_days_with_year
        non_working_days_prev_year = NonWorkingDays(str(int(request.query_params.get("year")) - 1)).non_working_days_with_year
        non_working_days_next_year = NonWorkingDays(str(int(request.query_params.get("year")) +1)).non_working_days_with_year
        non_working_days = non_working_days_prev_year + non_working_days_current_year + non_working_days_next_year
        return Response(data=non_working_days, status=status.HTTP_200_OK)
    
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
                "is_appointment": False,
                "breaks": [],
                "work_time": {
                    "start_time": None,
                    "end_time": None,
                    "is_free": False,
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
                        day_items["work_time"]["is_free"] = 1
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
                "is_appointment": False,
                "breaks": [],
                "work_time": {
                    "start_time": None,
                    "end_time": None,
                    "is_free": False,
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
                        day_items["work_time"]["is_free"] = 1
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
                    sea.start_time, sea.end_time, sea.is_default, sea.is_free,
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
                    sea.is_break, sea.`weekday`, 0 AS 'is_appointment'
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
                    ss.duration, ss.`name` AS 'service_name', ss.price, sa.`date`, LOWER(DAYNAME(sa.`date`)) AS 'day_name', sa.time_start,  
                    DATE_FORMAT((Time(sa.time_start) + INTERVAL ss.duration MINUTE), '%%H:%%i') as 'end_time', 1 AS 'is_appointment'
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
        self.user = request.user
        data = request.data
        if type(data) is not list:
            data = list(data.values())
        self.set_earliest_and_latest_date(data)
        if request.query_params.get("operation") == "get":
            return Response(data=self.get_employee_calendar(data), status=status.HTTP_200_OK)

