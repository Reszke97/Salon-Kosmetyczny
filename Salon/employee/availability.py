from rest_framework.permissions import (
    IsAuthenticated,  
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response
from django.http import HttpResponse
from django.db import connection

from rest_framework import status
from rest_framework.views import APIView
from ..serializers import *
from .utils.cursor_to_array_of_dicts import cursor_to_array_of_dicts
import datetime as dt

class AvailabilityApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]
    def get(self, request):
        user = request.user
        employee = Employee.objects.get(user_id = user.pk)
        cursor = connection.cursor()
        cursor.execute("""SELECT 
                seac.max_weeks_for_registration, seac.min_time_for_registration, sea.*
                from salon_employeeavailabilityconfiguration seac
                join salon_employeeavailability sea on sea.availability_config_id = seac.id
                where seac.employee_id = %s
                    and ( sea.date is null or Date(sea.date) >= %s )
            """
        , [employee.pk, dt.date.today()])
        res = cursor_to_array_of_dicts(cursor)
        return Response(res, status=status.HTTP_200_OK)