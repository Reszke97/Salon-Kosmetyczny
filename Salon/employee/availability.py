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
    
    def delete(self, request):
        user = User.objects.get(pk = request.user.pk)
        try:
            employee = Employee.objects.get(user_id = user.pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data
        # print(request.data)
        return Response({ "status": status.HTTP_200_OK, "errors": "" })






        # try:
        #     avatar = EmployeeAvatar.objects.get(employee_id = employee.pk)
        # except EmployeeAvatar.DoesNotExist:
        #     avatar = None
        # if avatar != None:
        #     content = str(avatar.content).replace("/", "\\")
        #     os.remove(os.path.join(settings.MEDIA_ROOT, content))
        #     avatar_serializer = self.create_or_update_avatar(request, employee, avatar )
        # else:
        #     avatar_serializer = self.create_or_update_avatar(request, employee)
        # if avatar_serializer.is_valid():
        #     avatar_serializer.save()
        #     return Response({ "status": status.HTTP_201_CREATED, "errors": "" })
        # else:
        #     return Response({ "status": status.HTTP_400_BAD_REQUEST, "errors": avatar_serializer.errors })

    def post(self, request):
        user = User.objects.get(pk = request.user.pk)
        try:
            employee = Employee.objects.get(user_id = user.pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for data in request.data:
            if data["default"]["id"] == "new":
                pass
                #add
            else:
                pass
                #update
            for def_breaks in data["default"]["breaks"]:
                if def_breaks["id"] == "new":
                    pass
                    #add
                else:
                    pass
                    #update
            for extra in data["extra"]:
                if extra["id"] == "new":
                    pass
                    #add
                else:
                    pass
                    #update
                for extra_breaks in extra["breaks"]:
                    if extra_breaks["id"] == "new":
                        pass
                    #add
                    else:
                        pass
                        #update
        return Response({ "status": status.HTTP_200_OK, "errors": "" })