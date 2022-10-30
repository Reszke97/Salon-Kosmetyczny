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

class ServiceCategoryApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]
    def get(self, request):
        user = request.user
        employee = Employee.objects.get(user_id = user.pk)

        cursor = connection.cursor()
        cursor.execute("""SELECT ssc.name, ssc.id from salon_servicecategory ssc 
                where ssc.id in (
                    SELECT ss.service_category_id from salon_service ss
                    where ss.employee_id = %s
                )
            """, [employee.pk]
        )
        res = cursor_to_array_of_dicts(cursor)
        return Response(res, status=status.HTTP_200_OK)



