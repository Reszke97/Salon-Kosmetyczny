from rest_framework.permissions import (
    IsAuthenticated,
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..serializers import *
import datetime as dt
from datetime import timedelta
from django.db import connection
from operator import itemgetter
from ..employee.utils.cursor_to_array_of_dicts import cursor_to_array_of_dicts

class VisitApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def convert_time_from_string_to_time_object(self, time, format):
        return dt.datetime.strptime(time, format).time()

    def get_modified_availability(self, availability):
        modified_availability = {
            "day_is_free": False,
            "availability": {
                "breaks": [],
            },
            "work_time": {
                "start": None,
                "end": None,
            }
        }
        if any(dict["is_default"] == 0 for dict in availability):
            for avail in availability:
                if avail["is_default"] == 0:
                    if(avail["is_break"] == 0 and avail["is_free"] == 0):
                        modified_availability["work_time"]["start"] = self.convert_time_from_string_to_time_object(avail["start_time"], "%H:%M")
                        modified_availability["work_time"]["end"] = self.convert_time_from_string_to_time_object(avail["end_time"], "%H:%M")
                    elif avail["is_break"] == 1 and avail["is_free"] == 0:
                        modified_availability["availability"]["breaks"].append(avail)
                    else:
                        modified_availability["day_is_free"] = True
                        break   
        else:
            for avail in availability:
                if avail["is_default"] == 1:
                    if(avail["is_break"] == 0 and avail["is_free"] == 0):
                        modified_availability["time"]["start"] = self.convert_time_from_string_to_time_object(avail["start_time"], "%H:%M")
                        modified_availability["time"]["end"] = self.convert_time_from_string_to_time_object(avail["end_time"], "%H:%M")
                    elif avail["is_break"] == 1 and avail["is_free"] == 0:
                        modified_availability["availability"]["breaks"].append(avail)
                    else:
                        modified_availability["day_is_free"] = True
                        break
        return modified_availability
    
    def time_in_range(self, start, end, current):
        """Returns whether current is in the range [start, end]"""
        return start <= current <= end
    
    def get_availability_config_for_given_date(self, data):
        cursor = connection.cursor()
        cursor.execute(
            """
                select 
                    sea.*, 
                    sea.start_time as 'appointment_start_time', 
                    sea.end_time as 'appointment_end_time',
                    sea.date as 'appointment_date'
                from salon_employeeavailabilityconfiguration seac
                join salon_employeeavailability sea on sea.availability_config_id = seac.id
                where seac.employee_id = %s
                    and(
                        sea.weekday = %s
                            and sea.is_default = 1
                        
                        or (
                            sea.date = %s
                                and sea.is_default = 0
                        )
                    )
            """
        , [data["employee_id"], data["day_name"], data["date"]])

        return cursor_to_array_of_dicts(cursor)
    
    def get_appointments_for_given_date(self, data):
        cursor = connection.cursor()
        cursor.execute(
            """
                select tab.* 
                from(
                    SELECT 
                        ss.duration, sa.date as 'appointment_date', sa.time_start as 'appointment_start_time', 1 as 'is_appointment',
                    DATE_FORMAT((Time(sa.time_start) + INTERVAL ss.duration MINUTE), '%%H:%%i') as 'appointment_end_time'
                    from salon_cosmeticprocedure scp
                    join salon_appointment sa on sa.id = scp.appointment_id
                    join salon_service ss on ss.id = scp.service_id
                    where ss.employee_id = %s
                        and sa.date = %s
                ) tab
                where( 
                    tab.appointment_end_time BETWEEN %s and %s
                ) or (tab.appointment_start_time BETWEEN %s and %s)
            """
        , [data["employee_id"], data["date"], data["start_time"], data["end_time"], data["start_time"], data["end_time"] ])
        return cursor_to_array_of_dicts(cursor)
    
    def create_set_from_existing_appointments(self, reserved_activities):
        existing_activities_set = set()
        for reserved_activity in reserved_activities:
    
            activity_start = self.convert_time_from_string_to_time_object(reserved_activity["appointment_start_time"], "%H:%M")
            activity_start = timedelta(hours=activity_start.hour, minutes=activity_start.minute)
            activity_end = self.convert_time_from_string_to_time_object(reserved_activity["appointment_end_time"], "%H:%M")
            activity_end = timedelta(hours=activity_end.hour, minutes=activity_end.minute)
            iterator = activity_start

            while iterator <= activity_end:
                if iterator not in existing_activities_set:
                    existing_activities_set.add(iterator)
                iterator += timedelta(minutes=1) 
        return existing_activities_set
    
    def check_if_visit_overlaps(self, availability, visit):
        existing_activities_set = self.create_set_from_existing_appointments(availability["reserved_activities"])
        duration = (
            timedelta(hours=visit["service_end"].hour, minutes=visit["service_end"].minute) - 
            timedelta(hours=visit["service_start"].hour, minutes=visit["service_start"].minute)
        ).seconds/60

        exists = False
        loop_current_time = timedelta(hours=visit["service_start"].hour, minutes=visit["service_start"].minute)
        duration_progress = 0

        while True:
            if loop_current_time + timedelta(minutes=duration_progress) in existing_activities_set:
                exists = True
                break
            else:
                duration_progress += 1
                if duration_progress == duration:
                    break
        return exists

    def check_if_visit_still_available(self, start_time, end_time, date, employee_id):
        date_time = dt.datetime.strptime(date + ' ' + start_time, "%Y-%m-%d %H:%M:%S")
        day_name = date_time.date().strftime("%A")
        day_name = day_name[0].lower() + day_name[1:]
        time_object = {
            "service_start": self.convert_time_from_string_to_time_object(start_time, "%H:%M:%S"),
            "service_end": self.convert_time_from_string_to_time_object(end_time, "%H:%M:%S"),
            "work_start": None,
            "work_end": None,
        }
        availability = self.get_availability_config_for_given_date(data={
            "employee_id": employee_id,
            "day_name": day_name,
            "date": date,
        })
        availability, day_is_free, work_time = itemgetter('availability', 'day_is_free', "work_time")(self.get_modified_availability(availability))
        time_object["work_start"] = work_time["start"]
        time_object["work_end"] = work_time["end"]

        if day_is_free == True:
            return False
        else:
            appointments = self.get_appointments_for_given_date(data={
                "employee_id": employee_id,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
            })
            if (
                self.time_in_range(time_object["work_start"], time_object["work_end"], time_object["service_start"])
                    and self.time_in_range(time_object["work_start"], time_object["work_end"], time_object["service_end"])
            ):
                appointments_with_avail = appointments + availability["breaks"]
                return not self.check_if_visit_overlaps({
                    "reserved_activities": appointments_with_avail
                }, time_object)

            else:
                return False
            
    def post(self, request):
        data = request.data
        user_pk = request.user.pk
        appointment_pk = None
        visit_available = self.check_if_visit_still_available(
            data["dateTime"]["start_time"], 
            data["dateTime"]["end_time"],
            data["dateTime"]["date"],
            data["employee_id"]
        )
        if visit_available:
            appointment_serializer = ApointmentSerializer(data = {
                "date": data["dateTime"]["date"],
                "time_start": data["dateTime"]["start_time"][:5],
            })

            if appointment_serializer.is_valid():
                appointment_pk = appointment_serializer.save().pk
            else:
                return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            appointment_history_serializer = AppointmentHistorySerializer(data = {
                "appointment": appointment_pk,
            })

            if appointment_history_serializer.is_valid():
                appointment_history_serializer.save()
            else:
                return Response(appointment_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            cosmetic_procedure_serializer = CosmeticProcedureSerializer(data = {
                "appointment": appointment_pk,
                "client": user_pk,
                "service": data["service_id"]
            })

            if cosmetic_procedure_serializer.is_valid():
                cosmetic_procedure_serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(cosmetic_procedure_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
