import base64
from email.policy import HTTP
import os
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (
    IsAuthenticated,
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response

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
        for key in request.FILES.getlist('files'):
            object = {
                "content": key,
                "employee": employee,
            }
            response = self.add_images(object)
            if response["status"] == 400:
                return Response(response["errors"], status=response["status"])
        return Response(status=response["status"])

    def delete(self, request):
        employee = Employee.objects.get(user = request.user.pk)
        img_id = request.query_params.get("image_id")
        img = EmployeeImage.objects.get(pk = img_id, employee_id = employee.pk)
        content = str(img.content).replace("/", "\\")
        os.remove(os.path.join(settings.MEDIA_ROOT, content))
        img.delete()
        return Response(status=status.HTTP_200_OK)
