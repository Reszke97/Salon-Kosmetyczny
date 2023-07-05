from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime as dt
from datetime import timedelta
from django.db import connection
from operator import itemgetter
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from ..serializers import *
from ..employee.utils.cursor_to_array_of_dicts import cursor_to_array_of_dicts
from ..employee.utils.image_actions import map_images
from ..auth.auth_backend import CheckIfPasswordWasChanged
from ..auth.auth_backend import EmailThread

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
                        modified_availability["work_time"]["start"] = self.convert_time_from_string_to_time_object(avail["start_time"], "%H:%M")
                        modified_availability["work_time"]["end"] = self.convert_time_from_string_to_time_object(avail["end_time"], "%H:%M")
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

            while iterator < activity_end:
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
            
    def send_notification_to_employee(self, user, data):
        emp = Employee.objects.get(pk=data["employee_id"])
        user_employee = User.objects.get(pk=emp.user_id)

        subject = "Nowa wizyta"
        email_body = render_to_string('client/send_notifcation_to_employee.html', {
            "full_client_name": user.first_name + ' ' + user.last_name,
            "appointment_date": data["dateTime"]["date"],
            "appointment_start_time": data["dateTime"]["start_time"][:5],
            "appointment_end_time": data["dateTime"]["end_time"][:5],
            "full_employee_name": user_employee.first_name + ' ' + user_employee.last_name
        })
        from_email = settings.EMAIL_FROM_USER
        email = EmailMultiAlternatives( subject, email_body, from_email, to=[user_employee.email])
        email.mixed_subtype = "related"
        email.attach_alternative(email_body, "text/html")
        EmailThread(email).start()
    
    def send_visit_swap_notification(self, employee, data):
        cursor = connection.cursor()
        cursor.execute(
            """
                select su.email
                from salon_appointment sa
                join salon_cosmeticprocedure scp on scp.appointment_id = sa.id
                join salon_user su on su.id = scp.client_id
                    where sa.id = %s
            """
        , [data["swappedVisit"]["appointment_id"]])
        client_mail = cursor_to_array_of_dicts(cursor)[0]["email"]

        subject = "Przełożenie wizyty"
        email_body = render_to_string('client/swap_visit.html', {
            "full_client_name": data["swappedVisit"]["client_name"] + ' ' + data["swappedVisit"]["client_last_name"] ,
            "appointment_date": data["dateTime"]["date"],
            "appointment_start_time": data["dateTime"]["start_time"][:5],
            "appointment_end_time": data["dateTime"]["end_time"][:5],
            "service_name": data["service_name"],
            "old_appointment_date": data["swappedVisit"]["date"],
            "old_appointment_time": data["swappedVisit"]["time"],
            "full_employee_name": employee.first_name + ' ' + employee.last_name
        })
        from_email = settings.EMAIL_FROM_USER
        email = EmailMultiAlternatives( subject, email_body, from_email, to=[client_mail])
        email.mixed_subtype = "related"
        email.attach_alternative(email_body, "text/html")
        EmailThread(email).start()
            
    def post(self, request):
        data = request.data
        user_pk = request.user.pk
        appointment_pk = None
        appointment_serializer = ApointmentSerializer(data = {
            "date": data["dateTime"]["date"],
            "time_start": data["dateTime"]["start_time"][:5],
        })

        if appointment_serializer.is_valid():
            if self.check_if_visit_still_available(
                data["dateTime"]["start_time"], 
                data["dateTime"]["end_time"],
                data["dateTime"]["date"],
                data["employee_id"]
            ):
                appointment_pk = appointment_serializer.save().pk
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cosmetic_procedure_serializer = CosmeticProcedureSerializer(data = {
            "appointment": appointment_pk,
            "client": user_pk,
            "service": data["service_id"]
        })

        if cosmetic_procedure_serializer.is_valid():
            cosmetic_procedure_serializer.save()
        else:
            return Response(cosmetic_procedure_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.send_notification_to_employee(request.user, data)
        return Response(status=status.HTTP_201_CREATED)
    
    def put(self, request):
        appointment_id = request.data["swappedVisit"]["appointment_id"]
        employee_id = request.data["swappedVisit"]["employees"][0]["id"]
        appointment = Appointment.objects.get(pk=appointment_id)
        appointment_serializer = ApointmentSerializer(appointment, data={
            "date": request.data["dateTime"]["date"],
            "time_start": request.data["dateTime"]["start_time"][:5]
        })
        if appointment_serializer.is_valid():
            if self.check_if_visit_still_available(
                request.data["dateTime"]["start_time"], 
                request.data["dateTime"]["end_time"],
                request.data["dateTime"]["date"],
                employee_id
            ):
                appointment_serializer.save()
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            self.send_visit_swap_notification(request.user, request.data)
        return Response(status=status.HTTP_200_OK)

        
class ClientVisitApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get_client_visits(self, user, visit_type):
        date_now = dt.datetime.now()
        time = str(date_now.time())[:5]
        date = str(date_now.date())
        where_query = """
            where scp.client_id = %s
            and concat(sa.date, ' ', sa.time_start) >= %s
        """
        if visit_type == "historical":
            where_query = """
                where scp.client_id = %s
                and concat(sa.date, ' ', sa.time_start) <= %s
            """
        cursor = connection.cursor()
        cursor.execute(
            """
                select
                    ss.name as 'service_name', ss.price, su.first_name as 'employee_name', su.last_name as 'employee_last_name', 
                    DATE_FORMAT((Time(sa.time_start) + INTERVAL ss.duration MINUTE), '%%H:%%i') as 'appointment_end_time',
                    su.phone_number as 'employee_phone', su.email as 'employee_mail', sa.date as 'appointment_date', 
                    sa.time_start as 'appointment_start_time', sba.name as 'business_name', sba.post_code as 'business_post_code',
                    sba.apartment_number as 'business_apartment_number', sba.house_number as 'business_house_number', 
                    sba.contact_phone as 'business_phone', sba.city as 'business_city', sbai.content as 'business_img', 
                    sba.street as 'business_street', sa.id as 'appointment_id'
                from salon_cosmeticprocedure scp
                join salon_appointment sa on sa.id = scp.appointment_id
                join salon_service ss on ss.id = scp.service_id
                join salon_employee se on se.id = ss.employee_id
                join salon_user su on su.id = se.user_id
                join salon_businessactivity sba on sba.id = se.business_activity_id 
                join salon_businessactivityimage sbai on sbai.business_activity_id = sba.id
            """ + where_query + " order by sa.date, sa.time_start"
        , [user.pk, date + ' ' + time])

        return cursor_to_array_of_dicts(cursor)

    def get(self, request):
        visit_type = request.query_params.get("visitType")
        items = self.get_client_visits(request.user, visit_type)
        for idx, item in enumerate(items):
            if item["business_img"]:
                class Img():
                    def __init__(self, content):
                        self.content = content
                items[idx]["business_img"] = map_images(Img(item["business_img"]))
        return Response(status=status.HTTP_200_OK, data=items)
    
    def send_delete_email_for_employee(self, user, data):
        subject = "Odwołanie wizyty"
        email_body = render_to_string('client/cancel_visit.html', {
            "full_client_name": user.first_name + ' ' + user.last_name,
            "appointment_date": data["appointment_date"],
            "appointment_start_time": data["appointment_start_time"],
            "appointment_end_time": data["appointment_end_time"],
            "full_employee_name": data["employee_name"] + ' ' + data["employee_last_name"]
        })
        from_email = settings.EMAIL_FROM_USER
        email = EmailMultiAlternatives( subject, email_body, from_email, to=[data["employee_mail"]])
        email.mixed_subtype = "related"
        email.attach_alternative(email_body, "text/html")
        EmailThread(email).start()
    
    def delete(self, request):
        data = request.data
        user = request.user
        appointment_id = request.query_params.get("appointment_id")

        cosmetic_procedure = CosmeticProcedure.objects.get(appointment_id=appointment_id, client_id=user.pk)
        appointment = Appointment.objects.get(pk=appointment_id)
        cosmetic_procedure.delete()
        appointment.delete()
        self.send_delete_email_for_employee(user, data)

        return Response(status=status.HTTP_200_OK)
    
class MessageToEmployee(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def send_message_to_employee(self, user, data):
        subject = "Komentarz do wizyty"
        email_body = render_to_string('client/send_message_to_employee.html', {
            "full_client_name": user.first_name + ' ' + user.last_name,
            "duration": data["duration"],
            "full_employee_name": data["employee_full_name"],
            "message": data["message"],
            "date": data["date"],
            "user_mail": user.email,
            "date_now": str(dt.datetime.now())[:19]
        })
        from_email = settings.EMAIL_FROM_USER
        email = EmailMultiAlternatives( subject, email_body, from_email, to=[data["employee_mail"]])
        email.mixed_subtype = "related"
        email.attach_alternative(email_body, "text/html")
        EmailThread(email).start()

    def post(self, request):
        data = request.data
        user = request.user
        self.send_message_to_employee(user, data)
        return Response(status=status.HTTP_200_OK)

