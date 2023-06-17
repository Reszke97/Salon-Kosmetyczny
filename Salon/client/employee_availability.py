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
    
    def calc_time_from_default_availability(self, def_availability):
        calculated_def_avail = []
        for day in self.weekdays:
            day_default_availability = [
                dictionary for dictionary in def_availability
                if dictionary.get("weekday") == day
            ]
            _starting_date = dt.datetime(year=1, month=1, day=1, hour=0, minute=0)
            time = _starting_date
            breaks = _starting_date
            for def_avail in day_default_availability:
                if def_avail["is_free"] == 1:
                    calculated_def_avail.append({
                        "day": day,
                        "time": time - breaks
                    })
                    break
                _date = dt.date(1, 1, 1)
                start_time = dt.datetime.strptime(def_avail["start_time"], "%H:%M").time()
                end_time = dt.datetime.strptime(def_avail["end_time"], "%H:%M").time()
                time_elapsed = dt.datetime.combine(_date, end_time) - dt.datetime.combine(_date, start_time)
                if def_avail["is_break"] == 1:
                    breaks += time_elapsed
                else:
                    time += time_elapsed
            calculated_def_avail.append({
                "day": day,
                "time": time - breaks
            })
        return calculated_def_avail
                      
    def get(self, request):
        data = request.query_params.dict()
        service_name = data.pop("service_name")
        date_now = dt.datetime.now()

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

            for day in range(days_left_to_check, 0, -1):
                date = date_now + timedelta(days=day)
                day_name = date.strftime("%A")
                day_name = day_name[0].lower() + day_name[1:]
                # str(date)[:10] -> sama data
                day_default_availability = [
                    dictionary for dictionary in default_availabilities
                    if dictionary.get("day") == day_name
                ]
                print(day_default_availability)

                #obliczyć time_delta dla appointments
                #obliczyć time_delta dla is_default = 0

                # if "is_free" in availability and availability["is_free"]:
                #     dates = filter(lambda d: d != str(date)[:10], dates)
                #     break
                # if time_is > latest_date
                # if time_is > earliest_date
        pass
        # client = User.objects.get(pk = request.user.pk)

    def put(self, request):
        pass
        # data = User.objects.get(pk = request.user.pk)