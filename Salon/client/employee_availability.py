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
        work_hours = { "start_time": timedelta(hours=0, minutes=0), "end_time": timedelta(hours=0, minutes=0) }
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
        appointments_with_time_delta = {
            "time_delta": timedelta(hours=0, minutes=0),
            "work_hours": [],
        }
        for appointment in appointments:
            date = dt.date(1, 1, 1)
            start_time = dt.datetime.strptime(appointment[start_time_key], "%H:%M").time()
            end_time = dt.datetime.strptime(appointment[end_time_key], "%H:%M").time()
            elapsed_time = dt.datetime.combine(date, end_time) - dt.datetime.combine(date, start_time)
            appointments_with_time_delta["time_delta"] += elapsed_time
            appointments_with_time_delta["work_hours"].append({
                "start_time": start_time,
                "end_time": end_time,
            })
        return appointments_with_time_delta
    
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
    
    def calculate_current_day_possible_time(self, availability, appointments, date_now):
        date = dt.date(1, 1, 1)
        avail_end_time = dt.datetime.combine(date, availability["work_hours"]["end_time"]) 
        avail_start_time = dt.datetime.combine(date, availability["work_hours"]["start_time"]) 
        daily_work_time = avail_end_time - avail_start_time
        time_now = timedelta(hours=date_now.hour, minutes=date_now.minute)
    
    def get_possible_overlaping_visits(self, appointments, start, end, date):

        #zrobić for na przerwy(breaks)

        for appointment in appointments:
            appointment_start = appointment["start_time"]
            appointment_start = timedelta(hours=appointment_start.hour, minutes=appointment_start.minute)
            appointment_end = appointment["end_time"]
            appointment_end = timedelta(hours=appointment_end.hour, minutes=appointment_end.minute)
            appointment_iterator_start = appointment_start
            availability_iterator_start = start
            existing_appointment_set = set()

            while appointment_iterator_start < appointment_end:
                existing_appointment_set.add(appointment_iterator_start)
                appointment_iterator_start += timedelta(minutes=1)

            while availability_iterator_start <= end:
                if availability_iterator_start in existing_appointment_set:
                    print(availability_iterator_start)
                availability_iterator_start += timedelta(minutes=1)

        #jeśli nie ma appointments to co godzinę else co pol godziny

        return "a"

    
                
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
            days_left_to_check = availability_config["max_weeks_for_registration"] * 7
            dates = []
            default_availabilities = self.calc_time_from_default_availability(default_availabilities)

            for day in range(days_left_to_check, -1, -1):
                date = date_now + timedelta(days=day)
                day_name = date.strftime("%A")
                day_name = day_name[0].lower() + day_name[1:]
                if len(list(filter(lambda d: d == (str(date)[:10])[5:], holidays))) == 0:
                    day_non_default_availability = self.calc_time_delta_non_default_availability(str(date)[:10], employee)
                    day_default_availability = [
                        dictionary for dictionary in default_availabilities
                        if dictionary.get("weekday") == day_name
                    ]
                    availability_type = "default"
                    if day_non_default_availability["not_assigned"] == False:
                        availability_type = "non_default"
                    
                    availability_dict = {
                        "default": day_default_availability[0],
                        "non_default": day_non_default_availability
                    }
                    earliest_date = date_now + timedelta(hours=int((availability_config["min_time_for_registration"])[:-1]))
                    if day_non_default_availability["is_free"] == False:
                        if (  
                            (day_non_default_availability["not_assigned"] == True
                                and day_default_availability[0]["is_free"] == False
                            ) or day_non_default_availability["not_assigned"] == False
                        ):
                            if earliest_date <= dt.datetime.combine(date, availability_dict[availability_type]["work_hours"]["end_time"]):
                                day_appointments = [
                                    dictionary for dictionary in appointments
                                    if dictionary.get("appointment_date") == str(date)[:10]
                                ]
                                day_appointments = self.calc_day_appointment_time_delta(
                                    day_appointments, "appointment_end_time", "appointment_start_time"
                                )
                                possible_time = availability_dict[availability_type]["time"] - day_appointments["time_delta"]
                                service_duration = timedelta(minutes=int(serialized_service.data["duration"]))
                                if possible_time >= service_duration:
                                    start_time = availability_dict[availability_type]["work_hours"]["start_time"]
                                    start_time = timedelta(hours=start_time.hour, minutes=start_time.minute)
                                    end_time = availability_dict[availability_type]["work_hours"]["end_time"]
                                    end_time = timedelta(hours=end_time.hour, minutes=end_time.minute)
                                    possible_visit_time_start = start_time
                                    possible_visit_time_end = start_time + service_duration

                                    while possible_visit_time_start < end_time:
                                        overlap_found = self.get_possible_overlaping_visits(
                                            day_appointments["work_hours"], possible_visit_time_start, possible_visit_time_end, date
                                        )
                                        possible_visit_time_start += timedelta(minutes=30)
                                        possible_visit_time_end += timedelta(minutes=30)

                                        #
                                
                                # print(str(date)[:10])
                                # if str(date)[:10] == str(date_now)[:10]:
                                #     possible_time = self.calculate_current_day_possible_time(
                                #         availability_dict[availability_type], appointments, date_now
                                #     )

                                # print((str(day_appointments["time_delta"])) + " appointments")
                                # print((str(availability_dict[availability_type]["time"])) + " All Time")
                                # print(str(availability_dict[availability_type]["time"] - day_appointments["time_delta"]) + " final")
                                # print(date)
        # client = User.objects.get(pk = request.user.pk)

    def put(self, request):
        pass
        # data = User.objects.get(pk = request.user.pk)