import base64
from django.db import connection
from ..models import Service
from django.db.models import Max
from rest_framework.permissions import (
    IsAuthenticated,  
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from ..serializers import *

class ServiceApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def add_service(self, service):
        service_serializer = ModifyServiceSerializer(data=service)
        if service_serializer.is_valid():
            service_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(service_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def add_category(self, category):
        category_serializer = ModifyCategorySerializer(data=category)
        if category_serializer.is_valid():
            cat_id = category_serializer.save().pk
            return { "status": 201, "data": cat_id}
        else:
            return { "status": 400, "errors": category_serializer.errors}

    def append_images(self, employee_config):
        for config in employee_config:
            images = EmployeeImage.objects.filter(image_set = config["image_set_id"])
            image_list = []
            for image in images:
                self.map_images(image, image_list)
            config["employee_image"] = image_list

    def map_images(self, image, image_list = None, ):
        content = str(image.content).replace("/", "\\")
        file_type = content[content.find('.') + 1::].upper()
        # Note: The "rb" option stands for "read binary".
        with open(settings.MEDIA_ROOT + "\\" + content, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            encoded_image = {
                "image": image_data,
                "file_type": file_type
            }
            if(image_list != None):
                image_list.append(encoded_image)
            return encoded_image

    def post(self, request):
        employee_id = Employee.objects.get(user = request.user.pk).pk
        cursor = connection.cursor()
        cursor.execute("""SELECT 
                max(my_tab.display_order) from (
                    select ssc.display_order, ssc.name ssc from salon_employeeserviceconfiguration sesc
                    left join salon_service ss on ss.id = sesc.service_id
                    left join salon_servicecategory ssc on ssc.id = ss.service_category_id
                    where sesc.employee_id = %s
                ) my_tab
            """, [employee_id]
        )
        res = cursor.fetchone()
        print(res)
        cat_res = self.add_category(
            {
                "name": request.data["category"],
                "display_order": res[0] + 1
            }
        )
        if cat_res["status"] == 400:
            return Response(cat_res["errors"], status=status.HTTP_400_BAD_REQUEST)
        request.data["srv"]["employee"] = employee_id
        request.data["srv"]["service_category"] = cat_res["data"]
        return self.add_service(request.data["srv"])
        
    def put(self, request):
        request.data["employee"] = Employee.objects.get(user = request.user.pk).pk
        data = request.data
        serializer = ServiceSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        employee = Employee.objects.get(user_id = request.user.pk)
        employee_service_configs = EmployeeServiceConfiguration.objects.filter(employee_id=employee)
        employee_service_configs_serialized = EmployeeServiceWithConfig(employee_service_configs, many=True)
        preview_selected = True if request.query_params.get("preview") == "true" else False    
        avatar = EmployeeAvatar.objects.get(employee = employee.pk)
        avatar_encoded = self.map_images(avatar)
        self.append_images(employee_service_configs_serialized.data)

        response = {
            "avatar": avatar_encoded if preview_selected else "",
            "service_info": employee_service_configs_serialized.data
        }
        return Response(response, status=status.HTTP_200_OK)


class ManageServiceApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    # def get(self, request):