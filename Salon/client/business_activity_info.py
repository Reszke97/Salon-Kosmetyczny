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

class BusinessActivityInfo(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        business_activity = BusinessActivity.objects.all()
        employees = Employee.objects.all()
        emoloyees_serialized = EmployeeFullInfoSerializer(employees, many=True)
        business_activity_serialized = BusinessActivitySerializer(business_activity, many=True)
        business_activity_with_employees = []
        distinct_services = Service.objects.all()
        distinct_services_serialized = DistinctServiceSerializer(distinct_services, many=True)
        employee_spec = EmployeeSpecialization.objects.all()
        employee_spec_serialized = EmployeeSpecializationSerializer(employee_spec, many=True)
        actual_employees = []
        
        for b_activity in business_activity_serialized.data:
            _employees = list(
                filter(
                    lambda item: (
                        item["business_activity_id"] == b_activity["id"]
                    ), emoloyees_serialized.data
                )
            )
            actual_employees = []
            for _employee in _employees:
                employees = []
                service = []
                services_ids = EmployeeServiceRelation.objects.filter(employee=_employee["id"])
                if services_ids:
                    for _service_id in services_ids:
                        _service = Service.objects.get(pk=_service_id.service_id)
                        _service = ServiceSerializer(_service)
                        service = [*service, _service.data]
                    employees = {
                        "employee_details": _employee,
                        "provided_service": service
                    }
                    actual_employees = [*actual_employees, employees]
                else: 
                    actual_employees = [{
                        "employee_details": _employee,
                        "provided_service": service
                    }]

            business_activity_with_employees = [*business_activity_with_employees, {
                    "business_info": b_activity,
                    "employees": actual_employees,
                }
            ]
            
        return Response(
            {
                "business_activity": business_activity_with_employees,
                "distinct_services": distinct_services_serialized.data,
                "distinct_employee_specs": employee_spec_serialized.data,
            },
            status=status.HTTP_200_OK
        )