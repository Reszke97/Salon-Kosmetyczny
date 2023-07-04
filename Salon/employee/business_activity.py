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
            "city": "",
            "is_active": False,
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
        if len(request.FILES.getlist('files')) != 0:
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
            if img_serializer.is_valid() and request.FILES.getlist('files') != None:
                img_serializer.save()
                return Response({ "status": status.HTTP_201_CREATED, "errors": "" })
            else:
                return Response(img_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        b_activity = BusinessActivity.objects.get(pk=employee.business_activity_id)
        serializer = BusinessActivitySerializer(b_activity, data=self.b_activity)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

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
                ses.name as 'spec_name', ss.name as 'service_name', ss.duration, ss.price, ssc.name as 'category_name'
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

class BusinessActivities(APIView):

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

    def all_business_info_query(self):
        return  """SELECT 
            ss.id as 'service_id', ssc.id as 'category_id', se.id as 'employee_id', se.is_owner, su.first_name, su.last_name, su.phone_number, su.email, 
            ses.name as 'spec_name', ses.id as 'spec_id', ss.name as 'service_name', ss.duration, ss.price, ssc.name as 'category_name',
            sba.id as 'b_activity_id', sba.name as 'b_activity_name', sba.post_code, sba.street, sba.apartment_number, sba.house_number,
            sba.contact_phone, sba.city, sba.about
            from salon_user su
            join salon_employee se on se.user_id = su.id
            join salon_businessactivity sba on sba.id = se.business_activity_id
            join salon_employeeserviceconfiguration sesc on sesc.employee_id = se.id
            join salon_employeespecialization ses on ses.id = se.spec_id
            left join salon_service ss on ss.id = sesc.service_id
            left join salon_servicecategory ssc on ssc.id = ss.service_category_id
        """

    def all_employees_query(self):
        return  """SELECT se.id as 'employee_id', su.id as 'user_id',
                su.first_name, su.last_name,  ses.name as 'spec_name'
            from salon_employee se
            join salon_user su on su.id = se.user_id
            join salon_employeespecialization ses on ses.id = se.spec_id
            where se.business_activity_id = %s
        """

    def get_employees_with_avatar(self, b_activity_id):
        cursor = connection.cursor()
        cursor.execute(self.all_employees_query(), [b_activity_id])
        all_employees = cursor_to_array_of_dicts(cursor)
        idx = 0

        for employee in all_employees:
            avatar_encoded = {
                "image": "",
                "file_type": ""
            }
            try:
                avatar = EmployeeAvatar.objects.get(employee_id = employee['employee_id'])
                avatar_encoded = self.map_images(avatar)
                all_employees[idx]["avatar"] = avatar_encoded
            except EmployeeAvatar.DoesNotExist:
                all_employees[idx]["avatar"] = avatar_encoded
            idx += 1
        return all_employees

    def group_business_activity_services(self, all_businesses_info):
        return_list = {}
        unique_sets = set(b_info['b_activity_id'] for b_info in all_businesses_info)

        for b_activity_id in unique_sets:
            employees = self.get_employees_with_avatar(b_activity_id)
            items_for_b_activity = list(filter(lambda x: (x["b_activity_id"] == b_activity_id),all_businesses_info))
            business_name = items_for_b_activity[0]["b_activity_name"]

            b_image_encoded = None
            try:
                image = BusinessActivityImage.objects.get(business_activity_id=items_for_b_activity[0]["b_activity_id"])
                b_image_encoded = self.map_image(image)
            except BusinessActivityImage.DoesNotExist:
                pass

            return_list[business_name] = {
                "id": items_for_b_activity[0]["b_activity_id"],
                "name": items_for_b_activity[0]["b_activity_name"],
                "post_code": items_for_b_activity[0]["post_code"],
                "street": items_for_b_activity[0]["street"],
                "apartment_number": items_for_b_activity[0]["apartment_number"],
                "house_number": items_for_b_activity[0]["house_number"],
                "contact_phone": items_for_b_activity[0]["contact_phone"],
                "city": items_for_b_activity[0]["city"],
                "about": items_for_b_activity[0]["about"],
                "image": b_image_encoded,
                "categories": {},
                "employees": employees,
            }
            unique_categories = set(b_info['category_id'] for b_info in items_for_b_activity)
            for unique_category in unique_categories:
                min_max_values = {
                    "duration": [],
                    "price": [],
                }
                services = list(filter(lambda x: (x["category_id"] == unique_category),items_for_b_activity))
                unique_services = set(b_info['service_id'] for b_info in services)
                category_name = services[0]["category_name"]
                i = 0
                return_list[business_name]["categories"][services[0]["category_name"]] = [{
                    "category_id": services[0]["category_id"],
                    "category_name": services[0]["category_name"],
                }]
                for unique_service in unique_services:
                    service = list(filter(lambda x: (x["service_id"] == unique_service),services))
                    employee_avatar = list(filter(lambda x: (x["employee_id"] == service[0]["employee_id"]),employees))
                    if i == 0:
                        min_max_values["duration"].append({
                            "service:": service[0]["service_name"],
                            "idx": i,
                            "values": [service[0]["duration"]],
                        })
                        min_max_values["price"].append({
                            "service:": service[0]["service_name"],
                            "values": [service[0]["price"]],
                            "idx": i,
                        })
                        return_list[business_name]["categories"][category_name][i]["service_name"] = service[0]["service_name"]
                        return_list[business_name]["categories"][category_name][i]["duration"] = service[0]["duration"]
                        return_list[business_name]["categories"][category_name][i]["price"] = service[0]["price"]
                        return_list[business_name]["categories"][category_name][i]["employees"] = [{
                            "avatar": employee_avatar[0]["avatar"],
                            "business_activity_id": return_list[business_name]["id"],
                            "id": service[0]["employee_id"],
                            "is_owner": service[0]["is_owner"],
                            "service": {
                                "category_id": service[0]["category_id"],
                                "category_name": service[0]["category_name"],
                                "duration": service[0]["duration"],
                                "price": service[0]["price"],
                                "service_id": service[0]["service_id"],
                                "service_name": service[0]["service_name"],
                            },
                            "spec": {
                                "id": service[0]["spec_id"],
                                "name": service[0]["spec_name"],
                            },
                            "user": {
                                "email": service[0]["email"],
                                "first_name": service[0]["first_name"], 
                                "last_name": service[0]["last_name"],
                                "phone_number": service[0]["phone_number"],
                            }
                        }]
                    else:
                        found_idx = next(
                            (
                                index for (index, d) in enumerate(
                                    return_list[business_name]["categories"][category_name]
                                ) if d["service_name"] == service[0]["service_name"]
                            )
                            , None
                        )
                        if found_idx is not None:
                            min_max_values["duration"][found_idx]["values"].append(service[0]["duration"])
                            min_max_values["price"][found_idx]["values"].append(service[0]["price"])

                            return_list[business_name]["categories"][category_name][found_idx]["employees"].append(
                                {
                                    "avatar": employee_avatar[0]["avatar"],
                                    "business_activity_id": return_list[business_name]["id"],
                                    "id": service[0]["employee_id"],
                                    "is_owner": service[0]["is_owner"],
                                    "service": {
                                        "category_id": service[0]["category_id"],
                                        "category_name": service[0]["category_name"],
                                        "duration": service[0]["duration"],
                                        "price": service[0]["price"],
                                        "service_id": service[0]["service_id"],
                                        "service_name": service[0]["service_name"],
                                    },
                                    "spec": {
                                        "id": service[0]["spec_id"],
                                        "name": service[0]["spec_name"],
                                    },
                                    "user": {
                                        "email": service[0]["email"],
                                        "first_name": service[0]["first_name"], 
                                        "last_name": service[0]["last_name"],
                                        "phone_number": service[0]["phone_number"],
                                    }
                                }
                            )
                        else:
                            min_max_values["duration"].append({
                                "service:": service[0]["service_name"],
                                "values": [service[0]["duration"]],
                                "idx": i,
                            })
                            min_max_values["price"].append({
                                "service:": service[0]["service_name"],
                                "values": [service[0]["price"]],
                                "idx": i,
                            })
                            return_list[business_name]["categories"][category_name].append({
                                "category_id": return_list[business_name]["categories"][category_name][0]["category_id"],
                                "category_name": return_list[business_name]["categories"][category_name][0]["category_name"],
                                "service_name": service[0]["service_name"],
                                "duration": service[0]["duration"],
                                "price": service[0]["price"],
                                "employees": [{
                                    "avatar": employee_avatar[0]["avatar"],
                                    "business_activity_id": return_list[business_name]["id"],
                                    "id": service[0]["employee_id"],
                                    "is_owner": service[0]["is_owner"],
                                    "service": {
                                        "category_id": service[0]["category_id"],
                                        "category_name": service[0]["category_name"],
                                        "duration": service[0]["duration"],
                                        "price": service[0]["price"],
                                        "service_id": service[0]["service_id"],
                                        "service_name": service[0]["service_name"],
                                    },
                                    "spec": {
                                        "id": service[0]["spec_id"],
                                        "name": service[0]["spec_name"],
                                    },
                                    "user": {
                                        "email": service[0]["email"],
                                        "first_name": service[0]["first_name"], 
                                        "last_name": service[0]["last_name"],
                                        "phone_number": service[0]["phone_number"],
                                    }
                                }]
                            })
                    i += 1
                for (idx, val) in enumerate(min_max_values["duration"]):
                    min_price = min(min_max_values["price"][idx]["values"])
                    max_price = max(min_max_values["price"][idx]["values"])
                    min_duration = min(min_max_values["duration"][idx]["values"])
                    max_duration = max(min_max_values["duration"][idx]["values"])
                    if min_duration != max_duration:
                        return_list[business_name]["categories"][category_name][val["idx"]]["duration"] = str(min_duration) + ' - ' + str(max_duration)
                    else:
                        return_list[business_name]["categories"][category_name][val["idx"]]["duration"] = min_duration
                    if min_price != max_price:
                        return_list[business_name]["categories"][category_name][val["idx"]]["price"] = str(min_price) + ' - ' + str(max_price)
                    else:
                        return_list[business_name]["categories"][category_name][val["idx"]]["price"] = min_price
        return return_list

    def get(self, request):
        cursor = connection.cursor()
        cursor.execute(self.all_business_info_query())
        all_businesses_info = cursor_to_array_of_dicts(cursor)
        all_businesses_info = self.group_business_activity_services(all_businesses_info)

        return Response(all_businesses_info, status=status.HTTP_200_OK)