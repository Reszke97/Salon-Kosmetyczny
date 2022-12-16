import base64
import os
from rest_framework.permissions import (
    IsAuthenticated,  
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from ..serializers import *
from rest_framework.parsers import MultiPartParser, FormParser

class EmployeeSpecsApi(APIView):

    def get(self, request):
        all_specs = EmployeeSpecialization.objects.all()
        all_specs_serialized = EmployeeSpecializationSerializer(all_specs, many=True)

        return Response(all_specs_serialized.data, status=status.HTTP_200_OK)