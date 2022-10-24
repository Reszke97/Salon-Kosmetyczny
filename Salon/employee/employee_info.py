import base64
import os
from rest_framework.permissions import (
    IsAuthenticated,  
)
from ..auth.auth_backend import CheckIfPasswordWasChanged
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from ..serializers import *
from rest_framework.parsers import MultiPartParser, FormParser

class EmployeeApi(APIView):
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
        user = User.objects.get(pk = request.user.pk)
        try:
            employee = Employee.objects.get(user_id = user.pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        avatar_encoded = ""
        try:
            avatar = EmployeeAvatar.objects.get(employee_id = employee.pk)
            avatar_encoded = self.map_images(avatar)
        except EmployeeAvatar.DoesNotExist:
            pass
        spec = EmployeeSpecialization.objects.get(pk = employee.spec_id)
        all_specs = EmployeeSpecialization.objects.all()
        all_specs_serialized = EmployeeSpecializationSerializer(all_specs, many=True)
        return Response(
            {
                "employee_info": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                    "user_name": user.user_name,
                    "email": user.email,
                    "avatar": avatar_encoded,
                    "employee_spec": { "name": spec.name, "id": spec.pk },
                    
                },
                "existing_specs": all_specs_serialized.data,
            },
            status=status.HTTP_200_OK
        )

    def put(self, request):
        user = User.objects.get(pk = request.user.pk)
        try:
            employee = Employee.objects.get(user_id = user.pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request_data = request.data
        if request_data["employee_spec"]["isNew"] == True:

            new_spec_serializer = NewEmployeeSpecializationSerializer(
                data={ "name": request_data["employee_spec"]["value"] }
            )
            if new_spec_serializer.is_valid():
                new_spec = new_spec_serializer.save()
                spec_id = new_spec.pk
            else:
                return Response(new_spec_serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        else:
            spec_id = request_data["employee_spec"]["value"]
        employee_serializer = UpdateEmployeeSpecSeriazlier(employee, data={
            "id": employee.pk,
            "spec": spec_id
        })
        if employee_serializer.is_valid():
            employee_serializer.save()
        else:
            return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_serializer = GetUserInfoSerializer(user, data={
            "first_name": request_data["first_name"],
            "last_name": request_data["last_name"],
            "phone_number": request_data["phone_number"],
            "user_name": request_data["user_name"],
            "email": request_data["email"],
        })
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class EmployeeAvatarApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]
    parser_classes = (MultiPartParser, FormParser)

    def create_or_update_avatar(self, request, employee, avatar = None):
        newAvatar = request.FILES.get('avatar')
        object = {
            "content": newAvatar,
            "employee": employee.pk,
        }
        if avatar != None:
            return EmployeeAvatarUpdateSerializer(avatar, data=object)
        else:
            return EmployeeAvatarCreateSerializer(data=object)

    def post(self, request):
        user = User.objects.get(pk = request.user.pk)
        try:
            employee = Employee.objects.get(user_id = user.pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            avatar = EmployeeAvatar.objects.get(employee_id = employee.pk)
        except EmployeeAvatar.DoesNotExist:
            avatar = None
        if avatar != None:
            content = str(avatar.content).replace("/", "\\")
            os.remove(os.path.join(settings.MEDIA_ROOT, content))
            avatar_serializer = self.create_or_update_avatar(request, employee, avatar )
        else:
            avatar_serializer = self.create_or_update_avatar(request, employee)
        if avatar_serializer.is_valid():
            avatar_serializer.save()
            return Response({ "status": status.HTTP_201_CREATED, "errors": "" })
        else:
            return Response({ "status": status.HTTP_400_BAD_REQUEST, "errors": avatar_serializer.errors })