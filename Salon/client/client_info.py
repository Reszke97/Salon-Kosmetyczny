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

class ClientApi(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get(self, request, *args, **kwargs):
        client = User.objects.get(pk = request.user.pk)
        return Response(
            {
                "first_name": client.first_name,
                "last_name": client.last_name,
                "phone_number": client.phone_number,
                "user_name": client.user_name,
                "email": client.email
            },
            status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        data = User.objects.get(pk = request.user.pk)
        serializer = GetUserInfoSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)