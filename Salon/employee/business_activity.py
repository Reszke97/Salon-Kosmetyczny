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
from ..models import BusinessActivity, Employee, BusinessActivityImage, EmployeeAvatar
from rest_framework.parsers import MultiPartParser, FormParser
from collections import OrderedDict
from django.db import connection
from .utils.cursor_to_array_of_dicts import cursor_to_array_of_dicts

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

class BusinessActivityEmployeesApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def map_images(self, image ):
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
        owner = Employee.objects.get(user_id = user.pk)
        employees = Employee.objects.filter(business_activity_id = owner.business_activity)
        b_activity_employees = EmployeeFullInfoSerializer(employees, many=True)
        idx = 0

        for b_activity_employee in b_activity_employees.data:
            try:
                avatar = EmployeeAvatar.objects.get(employee_id = b_activity_employee['id'])
                avatar_encoded = self.map_images(avatar)
                b_activity_employees.data[idx]["avatar"] = OrderedDict([
                    ('image', avatar_encoded["image"]),
                    ('file_type', avatar_encoded["file_type"]),
                ])
            except EmployeeAvatar.DoesNotExist:
                b_activity_employees.data[idx]["avatar"] = OrderedDict([
                    ('image', ''),
                    ('file_type', ''),
                ])
            idx += 1

        return Response(b_activity_employees.data, status=status.HTTP_200_OK)


class BusinessActivityServices(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get(self, request):
        user = request.user
        employee = Employee.objects.get(user_id = user.pk)

        cursor = connection.cursor()
        cursor.execute("""SELECT 
                ss.id as 'service_id', ssc.id as 'category_id', se.id as 'employee_id', su.first_name, su.last_name, su.phone_number, su.email, 
                ses.name as 'spec_name', ss.name as 'service_name', 'ss.duration', 'ss.price', ssc.name as 'category_name'
                from salon_user su
                join salon_employee se on se.user_id = su.id
                join salon_employeeserviceconfiguration sesc on sesc.employee_id = se.id
                join salon_employeespecialization ses on ses.id = se.spec_id
                left join salon_service ss on ss.id = sesc.service_id
                left join salon_servicecategory ssc on ssc.id = ss.service_category_id
                where se.business_activity_id = %s
            """, [employee.business_activity_id]
        )
        res = cursor_to_array_of_dicts(cursor)
        return Response(res, status=status.HTTP_200_OK)