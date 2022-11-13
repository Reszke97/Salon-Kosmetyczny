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
from ..models import Service, ServiceComment

def append_comments(employee_config):

    for config in employee_config:
        comments = ServiceComment.objects.filter(comment_set = config["comment_set_id"])
        comments_serialized = EmployeeCommentSerialier(comments, many=True)
        config["employee_comments"] = comments_serialized.data
class ServiceApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]
    parser_classes = (MultiPartParser, FormParser)

    def __init__(self):
        self.employee_id = None
        self.category = { "is_new": False, "category": "" }
        self.service = { "name": "", "price": 0, "duration": 0, "employee": 0, "service_category": 0 }

    def add_service(self, service):
        service_serializer = ModifyServiceSerializer(data=service)
        if service_serializer.is_valid():
            service_id = service_serializer.save().pk
            return { "status": status.HTTP_201_CREATED, "data": service_id }
        else:
            return { "status": status.HTTP_400_BAD_REQUEST, "errors": service_serializer.errors, }

    def update_service(self):
        service = Service.objects.get(pk = self.service["service_id"], employee_id = self.employee_id)
        service_serializer = ModifyServiceSerializer(service, data=self.service)
        if service_serializer.is_valid():
            service_serializer.save()
            return { "status": status.HTTP_200_OK }
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

    def map_request_data(self, data):
        for key in data:
            if key.find("service") != -1:
                self.service[key[(key.find('[')) + 1:-1]] = data[key]
            elif key.find("category") != -1:
                self.category[key[(key.find('[')) + 1:-1]] = data[key]

    def post(self, request):
        self.employee_id = Employee.objects.get(user = request.user.pk).pk
        self.map_request_data(request.data)
        files = request.FILES.getlist('files')
        img_response = { "data": None, "status": status.HTTP_201_CREATED }
        if files:
            img_response = prepare_and_create_images(files, self.employee_id)
        if img_response["status"] == 400:
            return Response(img_response["errors"], status=[img_response["status"]])
        cat_res = { "status": 201, "data": self.category["category"]}
        if self.category["is_new"] == "true":
            biggest_display_order_number = self.find_biggest_display_order(self.employee_id)
            if len(biggest_display_order_number) >= 1  and biggest_display_order_number[0] != None:
                biggest_display_order_number = biggest_display_order_number[0] + 1
            else:
                biggest_display_order_number = 1
            cat_res = self.add_category(
                {
                    "name": self.category["category"],
                    "display_order": biggest_display_order_number
                }
            )
            if cat_res["status"] == 400:
                return Response(cat_res["errors"], status=status.HTTP_400_BAD_REQUEST)
        else:
            cat_res = { "data": self.category["category"] }
        self.service["employee"] = self.employee_id
        self.service["service_category"] = cat_res["data"]
        service_res = self.add_service(self.service)
        if service_res["status"] == 400:
            return Response(service_res["errors"], status=service_res["status"])
        comment_set = EmployeeCommentSet.objects.create().id
        return self.create_emp_service_config({
            "employee": self.employee_id,
            "service": service_res["data"],
            "image_set": img_response["image_set"],
            "comment_set": comment_set
        })
        
        
    def put(self, request):
        self.employee_id = Employee.objects.get(user = request.user.pk).pk
        self.map_request_data(request.data)
        files = None
        if "files" in request.data:
            files = request.FILES.getlist('files')
            img_res = prepare_and_create_images(files, self.employee_id, request.data["image_set_id"])
            if img_res["status"] == 400:
                return Response(img_res["errors"], status=[img_res["status"]])
        if self.category["is_new"] == "true":
            biggest_display_order_number = self.find_biggest_display_order(self.employee_id)
            if len(biggest_display_order_number) >= 1  and biggest_display_order_number[0] != None:
                biggest_display_order_number = biggest_display_order_number[0] + 1
            else:
                biggest_display_order_number = 1
            cat_res = self.add_category(
                {
                    "name": self.category["category"],
                    "display_order": biggest_display_order_number
                }
            )
            if cat_res["status"] == 400:
                return Response(cat_res["errors"], status=status.HTTP_400_BAD_REQUEST)
        else:
            cat_res = { "data": self.category["category"] }
        self.service["employee"] = self.employee_id
        self.service["service_category"] = cat_res["data"]
        service_res = self.update_service()
        if service_res["status"] == 400:
            return Response(service_res["errors"], status=service_res["status"])
        return Response(status=service_res["status"])

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
        append_comments(employee_service_configs_serialized.data)
        response = {
            "avatar": avatar_encoded if preview_selected else "",
            "service_info": employee_service_configs_serialized.data
        }
        return Response(response, status=status.HTTP_200_OK)


class ServiceCommentApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get(self, request):
        employee = Employee.objects.get(user_id = request.user.pk)
        service = Service.objects.filter(pk = request.data["service_id"])
        if service.employee_id == employee.pk:
            srv_comment_serializer = ServiceCommentSerializer(service, many=True)
            return Response(srv_comment_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        employee = Employee.objects.get(user_id = request.user.pk)
        service = Service.objects.get(pk = request.data["service_id"])
        if service.employee_id == employee.pk:
            srv_comment_set_id = EmployeeCommentSet.objects.create().id
            srv_comment_serializer = ServiceCommentSerializer(data={
                "service": service.pk, "text": request.data["text"], "comment_set": srv_comment_set_id
            })
            if srv_comment_serializer.is_valid():
                srv_comment_serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(srv_comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        employee = Employee.objects.get(user_id = request.data.pk)
        if Service.objects.get(pk = request.data["service_id"]).employee == employee.pk:
            service_comment = ServiceComment.objects.get(pk=request.data.srvCommentId)
            srv_comment_serializer = ServiceCommentSerializer(service_comment, data=request.data)
            if srv_comment_serializer.is_valid():
                srv_comment_serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(srv_comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        employee = Employee.objects.get(user_id = request.data.pk)
        if Service.objects.get(pk = request.data["service_id"]).employee == employee.pk:
            ServiceComment.objects.delete(pk=request.data.srvCommentId)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ManageServiceApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    # def get(self, request):