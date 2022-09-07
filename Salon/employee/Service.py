from pickle import TRUE
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

class ServiceApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def post(self, request):
        request.data["employee"] = Employee.objects.get(user = request.user.pk).pk
        # serializer = ServiceSerializer(data=request.data)

        serializer = EmployeeImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     request.data["employee"] = Employee.objects.get(user = request.user.pk).pk
    #     serializer = ServiceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     request.data["employee"] = Employee.objects.get(user = request.user.pk).pk
    #     data = request.data
    #     serializer = GetUserInfoSerializer(data, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # EmployeeServices
        employee = Employee.objects.get(user_id = request.user.pk)
        employee_service_configs = EmployeeServiceConfiguration.objects.filter(employee_id=employee)
        employee_service_configs_serialized = EmployeeServiceConfigurationSerializer(employee_service_configs, many=True)

        services = []
        for empl_srv_config in employee_service_configs_serialized.data:
            services.append(
                ServiceSerializer(Service.objects.get(pk=empl_srv_config["service_id"])).data
            )
        # print(services)
        # services = Service.objects.filter(pk=)
        return Response(services, status=status.HTTP_200_OK)