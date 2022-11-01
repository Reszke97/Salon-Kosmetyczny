from django.db import connection
from rest_framework.permissions import (
    IsAuthenticated,  
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from ..serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from .utils.image_actions import map_images, append_images, prepare_and_create_images

class ServiceApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]
    parser_classes = (MultiPartParser, FormParser)

    def add_service(self, service):
        service_serializer = ModifyServiceSerializer(data=service)
        if service_serializer.is_valid():
            service_id = service_serializer.save().pk
            return { "status": status.HTTP_201_CREATED, "data": service_id }
        else:
            return { "status": status.HTTP_400_BAD_REQUEST, "errors": service_serializer.errors, }

    def add_category(self, category):
        category_serializer = ModifyCategorySerializer(data=category)
        if category_serializer.is_valid():
            cat_id = category_serializer.save().pk
            return { "status": 201, "data": cat_id}
        else:
            return { "status": 400, "errors": category_serializer.errors}

    def find_biggest_display_order(self, employee_id):
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
        return res

    def create_emp_service_config(self, data):
        emp_srv_conf_serializer = CreateEmployeeServiceConfigSerializer(data=data)
        if emp_srv_conf_serializer.is_valid():
            emp_srv_conf_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(emp_srv_conf_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        employee_id = Employee.objects.get(user = request.user.pk).pk
        category = { "is_new": False, "category": "" }
        service = { "name": "", "price": 0, "duration": 0, "employee": 0, "service_category": 0 }
        files = request.FILES.getlist('files')
        img_response = { "data": None, "status": status.HTTP_201_CREATED }
        for key in request.data:
            if key.find("service") != -1:
                service[key[(key.find('[')) + 1:-1]] = request.data[key]
            elif key.find("category") != -1:
                category[key[(key.find('[')) + 1:-1]] = request.data[key]
        if files:
            img_response = prepare_and_create_images(files, employee_id)
        if img_response["status"] == 400:
            return Response(img_response["errors"], status=[img_response["status"]])
        cat_res = { "status": 201, "data": category["category"]}
        if category["is_new"] == "true":
            biggest_display_order_number = self.find_biggest_display_order(employee_id)
            if len(biggest_display_order_number) > 1:
                biggest_display_order_number = biggest_display_order_number[0] + 1
            else:
                biggest_display_order_number = 1
            cat_res = self.add_category(
                {
                    "name": category["category"],
                    "display_order": biggest_display_order_number
                }
            )
        if cat_res["status"] == 400:
            return Response(cat_res["errors"], status=status.HTTP_400_BAD_REQUEST)
        service["employee"] = employee_id
        service["service_category"] = cat_res["data"]
        service_res = self.add_service(service)
        if service_res["status"] == 400:
            return Response(service_res["errors"], status=service_res["status"])
        return self.create_emp_service_config({
            "employee": employee_id,
            "service": service_res["data"],
            "image_set": img_response["image_set"]
        })
        
        
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
        try:  
            avatar = EmployeeAvatar.objects.get(employee = employee.pk)
            avatar_encoded = map_images(avatar)
        except EmployeeAvatar.DoesNotExist:
            avatar_encoded = None
        append_images(employee_service_configs_serialized.data)
        response = {
            "avatar": avatar_encoded if preview_selected else "",
            "service_info": employee_service_configs_serialized.data
        }
        return Response(response, status=status.HTTP_200_OK)


class ManageServiceApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    # def get(self, request):