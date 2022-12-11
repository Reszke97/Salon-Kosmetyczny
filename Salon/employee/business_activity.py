from django.db import connection
from rest_framework.permissions import (
    IsAuthenticated,  
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from ..serializers import *
from ..models import BusinessActivity, Employee

class ServiceApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    # def get(self, request):
