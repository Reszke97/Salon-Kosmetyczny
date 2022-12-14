from django.db import connection
import base64
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

    # def put(self, request):
