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
    def get(self, request):
        availability_api = AvailabilityApi()
        data = request.query_params.dict()
        service_name = data.pop("service_name")
        date_now = dt.datetime.now()

        for key in data:
            employee = Employee.objects.get(pk=data[key])
            service = Service.objects.get(employee = employee, name = service_name)
            availabilities = availability_api.get_emp_availability(emp=employee)
            serialized_services = ServiceSerializer(service)
            appointments = []
            latest_date = date_now + timedelta(days=availabilities[0]["max_weeks_for_registration"] * 7)
            earliest_date = date_now + timedelta(hours=availabilities[0]["min_time_for_registration"])
            
            for weekday in self.weekdays:
                day_availability = [
                    dictionary for dictionary in availabilities
                    if dictionary.get("weekday") == weekday
                ]
        pass
        # client = User.objects.get(pk = request.user.pk)

    def put(self, request):
        pass
        # data = User.objects.get(pk = request.user.pk)