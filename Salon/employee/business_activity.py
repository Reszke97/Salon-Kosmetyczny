from django.db import connection
import base64
import os
from rest_framework.permissions import (
    IsAuthenticated,  
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from ..serializers import *
from ..models import BusinessActivity, Employee, BusinessActivityImage
from rest_framework.parsers import MultiPartParser, FormParser

class BusinessActivityApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def __init__(self):
        self.b_activity = { 
            "name": "", 
            "post_code": "", 
            "street": "", 
            "apartment_number": None, 
            "house_number": None,
            "contact_phone": "",
            "city": ""
        }

    def map_request_data(self, data):
        for key in data:
            self.b_activity[key] = data[key]

    def map_image(self, image ):
        content = str(image.content).replace("/", "\\")
        file_type = content[content.find('.') + 1::].upper()
        # Note: The "rb" option stands for "read binary".
        with open(settings.MEDIA_ROOT + "\\" + content, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            encoded_image = {
                "image": image_data,
                "file_type": file_type
            }
            return encoded_image

    def create_or_update_img(self, request, employee, img = None):
        file = request.FILES.getlist('files')
        object = {
            "content": file[0],
            "business_activity": employee.business_activity_id,
        }
        if img != None:
            return BusinessActivityImageUpdateSerializer(img, data=object)
        else:
            return BusinessActivityImageCreateSerializer(data=object)

    def get(self, request):
        user = request.user
        employee = Employee.objects.get(user_id = user.pk)
        b_activity = BusinessActivity.objects.get(pk=employee.business_activity_id)
        b_activity_data = BusinessActivitySerializer(b_activity).data
        image_encoded = None
        try:
            image = BusinessActivityImage.objects.get(business_activity_id=b_activity.pk)
            image_encoded = self.map_image(image)
        except BusinessActivityImage.DoesNotExist:
            pass
        b_activity_data["image"] = image_encoded

        return Response(b_activity_data, status=status.HTTP_200_OK)

    def put(self, request):
        employee = Employee.objects.get(user = request.user.pk)
        self.map_request_data(request.data)
        try:
            img = BusinessActivityImage.objects.get(business_activity_id = employee.business_activity_id)
        except BusinessActivityImage.DoesNotExist:
            img = None
        if img != None:
            content = str(img.content).replace("/", "\\")
            os.remove(os.path.join(settings.MEDIA_ROOT, content))
            img_serializer = self.create_or_update_img(request, employee, img )
        else:
            img_serializer = self.create_or_update_img(request, employee)
        if img_serializer.is_valid():
            img_serializer.save()
            return Response({ "status": status.HTTP_201_CREATED, "errors": "" })
        else:
            return Response(img_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

