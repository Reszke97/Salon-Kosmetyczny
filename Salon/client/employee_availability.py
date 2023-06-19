from rest_framework.permissions import (
    IsAuthenticated,  
    BasePermission, 
    AllowAny
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from ..serializers import *
from ..employee.availability import *
import datetime as dt
from datetime import timedelta
from django.db import connection
from ..employee.utils.cursor_to_array_of_dicts import cursor_to_array_of_dicts
from ..employee.Calendar import Holidays

class ClientEmployeeAvailability(APIView):
    permission_classes = [AllowAny]
    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]

    def get_appointments(self, employee):
        cursor = connection.cursor()
        cursor.execute("""SELECT 
                ss.duration, sa.date as 'appointment_date', sa.time_start as 'appointment_start_time', 1 as 'is_appointment',
                DATE_FORMAT((Time(sa.time_start) + INTERVAL ss.duration MINUTE), '%%H:%%i') as 'appointment_end_time'
                from salon_cosmeticprocedure scp
                join salon_appointment sa on sa.id = scp.appointment_id
                join salon_service ss on ss.id = scp.service_id
                where ss.employee_id = %s
            """
        , [employee.pk])
        return cursor_to_array_of_dicts(cursor)
    
    def get_default_emp_availability(self, employee):
        cursor = connection.cursor()
        cursor.execute("""SELECT
                sea.weekday, sea.start_time, sea.end_time, sea.is_break,
                sea.is_free, sea.is_holiday
                from salon_employeeavailability sea
                join salon_employeeavailabilityconfiguration seac on seac.id = sea.availability_config_id
                where seac.employee_id = %s
                    and sea.is_default = 1
            """
        , [employee.pk])
        return cursor_to_array_of_dicts(cursor)
    
    def get_default_availability_by_key_value(self, availability, key, value):
        return  [
            dictionary for dictionary in availability
            if dictionary.get(key) == value
        ]
    
    def calc_breaks_and_time(self, availability, extra_value = None, extra_value_key = "date"):
        date_availability = availability
        if extra_value_key == "weekday":
            date_availability = self.get_default_availability_by_key_value(availability, extra_value_key, extra_value)
        _starting_date = dt.datetime(year=1, month=1, day=1, hour=0, minute=0)
        time = _starting_date
        breaks = _starting_date
        is_free = False
        not_assigned = True
        break_times = []
        work_hours = { "start_time": 0, "end_time": 0 }
        for avail in date_availability:
            is_free = False
            not_assigned = False
            if avail["is_free"] == 1:
                is_free = True
                break
            _date = dt.date(1, 1, 1)
            start_time = dt.datetime.strptime(avail["start_time"], "%H:%M").time()
            end_time = dt.datetime.strptime(avail["end_time"], "%H:%M").time()
            time_elapsed = dt.datetime.combine(_date, end_time) - dt.datetime.combine(_date, start_time)
            if avail["is_break"] == 1:
                breaks += time_elapsed
                break_times.append({
                    "start_time": start_time,
                    "end_time": end_time
                })
            else:
                work_hours["start_time"] = start_time
                work_hours["end_time"] = end_time
                time += time_elapsed
        return {
            extra_value_key: extra_value,
            "time": time - breaks,
            "is_free": is_free,
            "break_times": break_times,
            "work_hours": work_hours,
            "not_assigned": not_assigned
        }

    
    def calc_time_from_default_availability(self, availability):
        calculated_def_avail = []
        for day in self.weekdays:
            calculated_def_avail.append(self.calc_breaks_and_time(availability, day, "weekday"))
        return calculated_def_avail
    
    def calc_day_appointment_time_delta(self, appointments, end_time_key, start_time_key):
        time_delta = timedelta(hours=0, minutes=0)
        for appointment in appointments:
            date = dt.date(1, 1, 1)
            start_time = dt.datetime.strptime(appointment[start_time_key], "%H:%M").time()
            end_time = dt.datetime.strptime(appointment[end_time_key], "%H:%M").time()
            elapsed_time = dt.datetime.combine(date, end_time) - dt.datetime.combine(date, start_time)
            time_delta += elapsed_time
        return time_delta
    
    def calc_time_delta_non_default_availability(self, date, employee):
        cursor = connection.cursor()
        cursor.execute("""SELECT
                sea.weekday, sea.start_time, sea.end_time, sea.is_break,
                sea.is_free, sea.is_holiday
                from salon_employeeavailability sea
                join salon_employeeavailabilityconfiguration seac on seac.id = sea.availability_config_id
                where seac.employee_id = %s
                    and sea.is_default = 0
                    and sea.date = %s
            """
        , [employee.pk, date])
        data = cursor_to_array_of_dicts(cursor)
        return self.calc_breaks_and_time(data, date, "date")
                
    def get(self, request):
        data = request.query_params.dict()
        service_name = data.pop("service_name")
        date_now = dt.datetime.now()
        holidays = Holidays().get_holidays(str(date_now.year))

        for key in data:
            employee = Employee.objects.get(pk=data[key])
            service = Service.objects.get(employee = employee, name = service_name)
            availability_config = AvailabilityConfigApi().get_emp_config(emp=employee)
            serialized_service = ServiceSerializer(service)
            appointments = self.get_appointments(employee)
            default_availabilities = self.get_default_emp_availability(employee)
            latest_date = date_now + timedelta(days=availability_config["max_weeks_for_registration"] * 7)
            earliest_date = date_now + timedelta(hours=int((availability_config["min_time_for_registration"])[:-1]))
            days_left_to_check = availability_config["max_weeks_for_registration"] * 7
            dates = []
            default_availabilities = self.calc_time_from_default_availability(default_availabilities)

            for day in range(days_left_to_check, -1, -1):
                date = date_now + timedelta(days=day)
                day_name = date.strftime("%A")
                day_name = day_name[0].lower() + day_name[1:]
                if date >= earliest_date and len(list(filter(lambda d: d == (str(date)[:10])[5:], holidays))) == 0:
                    day_non_default_availability = self.calc_time_delta_non_default_availability(str(date)[:10], employee)
                    day_default_availability = [
                        dictionary for dictionary in default_availabilities
                        if dictionary.get("weekday") == day_name
                    ]
                    if day_non_default_availability["is_free"] == False:
                        if (  
                            (day_non_default_availability["not_assigned"] == True
                                and day_default_availability[0]["is_free"] == False
                            ) or day_non_default_availability["not_assigned"] == False
                        ):
                            today_time = timedelta(hours=0, minutes=0)
                            # if str(date)[:10] == str(date_now)[:10]:
                            availability_type = "default"
                            if day_non_default_availability["not_assigned"] == False:
                                availability_type = "non_default"

                            day_appointments = [
                                dictionary for dictionary in appointments
                                if dictionary.get("appointment_date") == str(date)[:10]
                            ]
                            day_appointments = self.calc_day_appointment_time_delta(
                                day_appointments, "appointment_end_time", "appointment_start_time"
                            )
                            
                            print(str(day_appointments) + " appointments")
                            
                            if availability_type == "default":
                                print(str(day_default_availability[0]["time"]) + " All Time")
                                print(str(day_default_availability[0]["time"] - day_appointments) + " final default")
                                print(date)
                            else:
                                print(str(day_non_default_availability["time"]) + " All Time")
                                print(str(day_non_default_availability["time"] - day_appointments) + " final Non default")
                                print(date)

        # client = User.objects.get(pk = request.user.pk)

    def put(self, request):
        pass
        # data = User.objects.get(pk = request.user.pk)