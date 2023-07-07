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
from ..models import EmployeeAvailability
from .utils.cursor_to_array_of_dicts import cursor_to_array_of_dicts
from .utils.non_working_days import NonWorkingDays
import datetime as dt

class AvailabilityApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get_emp_availability(self, user = None, emp = None):
        today = dt.date.today()
        employee = emp
        if(emp is None):
            employee = Employee.objects.get(user_id = user.pk)
        cursor = connection.cursor()
        cursor.execute("""SELECT 
                seac.max_weeks_for_registration, seac.min_time_for_registration, sea.*
                from salon_employeeavailabilityconfiguration seac
                join salon_employeeavailability sea on sea.availability_config_id = seac.id
                where seac.employee_id = %s
                    and ( sea.date is null or Date(sea.date) >= %s )
            """
        , [employee.pk, today])
        res = cursor_to_array_of_dicts(cursor)
        non_working_days = NonWorkingDays(str(today).split('-')[0])
        for item in res:
            if item["date"] != None:
                split_date = item["date"].split('-')
                if non_working_days.checkForHoliday(split_date[2], split_date[1]):
                    item["is_holiday"] = True
        return res

    def get(self, request):
        res = self.get_emp_availability(user=request.user)
        return Response(res, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = User.objects.get(pk = request.user.pk)
        try:
            employee = Employee.objects.get(user_id = user.pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data
        for availabilityId in data:
            availability = EmployeeAvailability.objects.get(pk = availabilityId)
            availability.delete()
        return Response({ "status": status.HTTP_200_OK, "errors": "" })

    def serializer_save(self, serializer):
        if serializer.is_valid():
                serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def updateOrAddNewAvailiabilityEvent(self, data, action, id):
        if action == "update":
            availability = EmployeeAvailability.objects.get(pk=id)
            availability_serializer = AvailabilitySerializer(availability, data=data)
            self.serializer_save(availability_serializer)
        else:
            availability_serializer = AvailabilitySerializer(data=data)
            self.serializer_save(availability_serializer)


    def post(self, request):
        user = User.objects.get(pk = request.user.pk)
        try:
            employee = Employee.objects.get(user_id = user.pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cursor = connection.cursor()
        cursor.execute("""SELECT 
                seac.id
                from salon_employeeavailabilityconfiguration seac
                where seac.employee_id = %s
            """
        , [employee.pk])
        res = cursor_to_array_of_dicts(cursor)
        availability_config_id = res[0]["id"]
        
        for data in request.data:
            data_action = {
                "is_free": data["default"]["is_free"],
                "is_holiday": data["default"]["is_holiday"],
                "weekday": data["default"]["day"]["gb"],
                "start_time": data["default"]["work_hours"][0]["start_time"] if(len(data["default"]["work_hours"])) else None,
                "end_time": data["default"]["work_hours"][0]["end_time"] if(len(data["default"]["work_hours"])) else None,
                "is_break": False,
                "availability_config_id": availability_config_id,
                "date": None,
                "is_default": True,
            }
            if data["default"]["id"] == "new":
                self.updateOrAddNewAvailiabilityEvent(
                    data_action, "add", data["default"]["id"]
                )
            else:
                self.updateOrAddNewAvailiabilityEvent(
                    data_action, "update", data["default"]["id"]
                )
            for def_breaks in data["default"]["breaks"]:
                def_breaks_action = {
                    "is_free": False,
                    "is_holiday": False,
                    "weekday": data["default"]["day"]["gb"],
                    "start_time": def_breaks["start_time"],
                    "end_time": def_breaks["end_time"],
                    "is_break": True,
                    "is_default": True,
                    "availability_config_id": availability_config_id,
                    "date": None
                }
                if def_breaks["id"] == "new":
                    self.updateOrAddNewAvailiabilityEvent(
                        def_breaks_action, "add", def_breaks["id"]
                    )
                else:
                    self.updateOrAddNewAvailiabilityEvent(
                        def_breaks_action, "update", def_breaks["id"]
                    )
            for extra in data["extra"]:
                extra_action = {
                    "is_free": extra["is_free"],
                    "is_holiday": extra["is_holiday"],
                    "weekday": data["default"]["day"]["gb"],
                    "start_time": extra["work_hours"][0]["start_time"] if(len(extra["work_hours"])) else None,
                    "end_time": extra["work_hours"][0]["end_time"] if(len(extra["work_hours"])) else None,
                    "is_break": False,
                    "is_default": False,
                    "date": extra["date"],
                    "availability_config_id": availability_config_id,
                }
                if extra["id"] == "new":
                    self.updateOrAddNewAvailiabilityEvent(
                        extra_action, "add", extra["id"]
                    )
                else:
                    self.updateOrAddNewAvailiabilityEvent(
                        extra_action, "update", extra["id"]
                    )
                for extra_breaks in extra["breaks"]:
                    extra_breaks_action = {
                        "is_free": False,
                        "is_holiday": False,
                        "weekday": data["default"]["day"]["gb"],
                        "start_time": extra_breaks["start_time"],
                        "end_time": extra_breaks["end_time"],
                        "is_break": True,
                        "is_default": False,
                        "date": extra["date"],
                        "availability_config_id": availability_config_id, 
                    }
                    if extra_breaks["id"] == "new":
                        self.updateOrAddNewAvailiabilityEvent(
                            extra_breaks_action, "add", extra_breaks["id"],
                        )
                    else:
                        self.updateOrAddNewAvailiabilityEvent(
                            extra_breaks_action, "update", extra_breaks["id"]
                        )
        return Response({ "status": status.HTTP_200_OK, "errors": "" })
    
class AvailabilityConfigApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get_emp_config(self, user = None, emp = None):
        employee = emp
        if(emp is None):
            try:
                employee = Employee.objects.get(user_id = user.pk)
            except Employee.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        emp_config = EmployeeAvailabilityConfiguration.objects.get(employee=employee.pk)
        return {
            "max_weeks_for_registration": emp_config.max_weeks_for_registration,
            "min_time_for_registration": emp_config.min_time_for_registration
        }

    def get(self, request):
        data = self.get_emp_config(user=User.objects.get(pk = request.user.pk))
        return Response(status=status.HTTP_200_OK, data={
            "max_weeks_for_registration": data["max_weeks_for_registration"],
            "min_time_for_registration": data["min_time_for_registration"]
        })
        

    def put(self, request):
        data = request.data
        data["min_time_for_registration"] = "24h"
        user = User.objects.get(pk = request.user.pk)
        try:
            employee = Employee.objects.get(user_id = user.pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        emp_config = EmployeeAvailabilityConfiguration.objects.get(employee=employee.pk)
        serializer = AvailabilityConfigSerializer(emp_config, data={ **data, "employee": employee.pk })
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(exception=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
        
