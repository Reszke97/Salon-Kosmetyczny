import base64
from rest_framework.parsers import MultiPartParser, FormParser
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

class ImagesApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]
    parser_classes = (MultiPartParser, FormParser)
    def add_images(self, images):
        images_serializer = EmployeeImageSerializer(data=images)
        if images_serializer.is_valid():
            images_serializer.save()
            return { "status": status.HTTP_201_CREATED, "errors": "" }
        else:
            return { "status": status.HTTP_400_BAD_REQUEST, "errors": images_serializer.errors }

    def post(self, request):
        employee = Employee.objects.get(user = request.user.pk).pk
        response = { "status": status.HTTP_201_CREATED, "errors": "" }
        print(request.data)
        for a in request.data:
            print({ a: request.data[a] })
        for key in request.FILES.getlist('files'):
            object = {
                "content": key,
                "employee": employee,
            }
            response = self.add_images(object)
            if response["status"] == 400:
                return Response(response["errors"], status=response["status"])
        return Response(status=response["status"])