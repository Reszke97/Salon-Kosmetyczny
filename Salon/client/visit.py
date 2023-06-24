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
from ..employee.utils.cursor_to_array_of_dicts import cursor_to_array_of_dicts

class VisitApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def check_if_visit_still_available(self, start_time, end_time, date, employee_id):
        date_time = dt.datetime.strptime(date + ' ' + start_time, "%Y-%m-%d %H:%M:%S")
        cursor = connection.cursor()
        cursor.execute("""SELECT 
                ss.duration, sa.date as 'appointment_date', sa.time_start as 'appointment_start_time', 1 as 'is_appointment',
                DATE_FORMAT((Time(sa.time_start) + INTERVAL ss.duration MINUTE), '%%H:%%i') as 'appointment_end_time'
                from salon_cosmeticprocedure scp
                join salon_appointment sa on sa.id = scp.appointment_id
                join salon_service ss on ss.id = scp.service_id
                where ss.employee_id = %s
                    and sa.date = %s
            """
        , [employee_id, date])
        appointments = cursor_to_array_of_dicts(cursor)
        
        # day_name = date.strftime("%A")
        # day_name = day_name[0].lower() + day_name[1:]

        data = cursor_to_array_of_dicts(cursor)


    def post(self, request):
        data = request.data
        user_pk = request.user.pk
        appointment_pk = None
        self.check_if_visit_still_available(
            data["dateTime"]["start_time"], 
            data["dateTime"]["end_time"],
            data["dateTime"]["date"],
            data["employee_id"]
        )

        # appointment_serializer = ApointmentSerializer(data = {
        #     "date": data["dateTime"]["date"],
        #     "time_start": data["dateTime"]["start_time"][:5],
        # })

        # if appointment_serializer.is_valid():
        #     appointment_pk = appointment_serializer.save().pk
        # else:
        #     return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # appointment_history_serializer = AppointmentHistorySerializer(data = {
        #     "appointment": appointment_pk,
        # })

        # if appointment_history_serializer.is_valid():
        #     appointment_history_serializer.save()
        # else:
        #     return Response(appointment_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # cosmetic_procedure_serializer = CosmeticProcedureSerializer(data = {
        #     "appointment": appointment_pk,
        #     "client": user_pk,
        #     "service": data["service_id"]
        # })

        # if cosmetic_procedure_serializer.is_valid():
        #     cosmetic_procedure_serializer.save()
        #     return Response(status=status.HTTP_201_CREATED)
        # else:
        #     return Response(cosmetic_procedure_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
