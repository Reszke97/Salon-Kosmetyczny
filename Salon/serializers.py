from rest_framework import serializers
from . models import *
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import TokenBackendError
from django.utils.translation import gettext as _

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    #password = serializers.CharField(min_length=8, write_only=True)
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ('email', 'user_name', 'password','first_name', 'last_name','phone_number','id')
        # extra_kwargs = {'password': {'write_only': True}}
        extra_kwargs = {
            'email': {'write_only': True, 'required': True},
            'user_name': {'write_only': True, 'required': True},
            'password': {'write_only': True, 'required': True},
            'first_name': {'write_only': True, 'required': True},
            'last_name': {'write_only': True, 'required': True},
            'phone_number': {'write_only': True, 'required': False},
            # 'id': {'write_only': True, 'required': False},
        }
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

class UserRoleSerializer(serializers.Serializer):
    model = User
    fields = ('role')
    extra_kwargs = {
        'role': {'write_only': True, 'required': True},
    }

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ('password', 'token', 'uidb64')

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        # sprawdzenie czy Issued_at jest > updated_at
        try:
            print('refresh')
            print(attrs['refresh'])
            decoded_payload = token_backend.decode(attrs['refresh'])
            user_id = decoded_payload['user_id']
            iat = decoded_payload['iat']
            user = User.objects.get(pk = user_id)
            updated_at = user.last_password_update
            updated_at = int(updated_at.timestamp())
        except TokenBackendError:
            raise TokenError(_('Token jest niepoprawny.'))

        if iat > updated_at:
            data = super().validate(attrs)
            return data
        else:
            raise TokenError(_('Twoje Hasło zostało przed chwilą zmienione, proszę zalogować się ponownie.'))

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)