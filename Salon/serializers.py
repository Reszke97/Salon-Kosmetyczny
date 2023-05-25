from rest_framework import serializers
from . models import *
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import TokenBackendError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'is_owner',
            'user',
            'business_activity',
            'spec'
        )

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

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('duration', 'name', 'price',)

class ModifyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('duration', 'name', 'price', 'employee', 'service_category')

class ServiceCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="id")
    category_display_order = serializers.IntegerField(source="display_order")
    class Meta:
        model = ServiceCategory
        fields = ('category_id', 'name', 'styles', 'category_display_order')

class ModifyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ('name', 'display_order')

class ExistingServiceSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(source="id")
    service_category = ServiceCategorySerializer()
    class Meta:
        model = Service
        fields = ('duration', 'name', 'price', 'service_id', 'service_category')

class ServiceCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceComment
        fields = ("service", "text", "comment_set")


class EmployeeServiceConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeServiceConfiguration
        fields = (
            'styles', 
            'employee_id',
            'employee_image_id',
            'service_id',
        )

class EmployeeAvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAvatar
        fields = (
            'content', 
            'id',
            'employee',
        )
class EmployeeAvatarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAvatar
        fields = (
            'content', 
            'employee',
        )



class BusinessActivityImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessActivityImage
        fields = (
            'content',
            'business_activity'
        )
class BusinessActivityImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessActivityImage
        fields = (
            'id',
            'content',
            'business_activity'
        )
    
class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImage
        fields = (
            'content',
            'employee',
            'image_set',
        )

class CreateEmployeeServiceConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeServiceConfiguration
        fields = (
            'image_set',
            'service',
            'employee'
        )

class EmployeeServiceWithConfig(serializers.ModelSerializer):
    service = ExistingServiceSerializer()
    employee_service_config_id = serializers.IntegerField(source="id")

    class Meta:
        model = EmployeeServiceConfiguration
        fields = (
            'employee_service_config_id',
            'styles',
            'image_set_id',
            'comment_set_id',
            'service',
        )

class EmployeeCommentSerialier(serializers.ModelSerializer):
    class Meta:
        model = ServiceComment
        fields = (
            'service',
            'text',
            'comment_set',
            'id',
        )

class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "user_name",
            "email",
            "id"
        )
class TokenObtainPairSerializerEmployee(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        try:
            if(Employee.objects.get(user_id = user.pk)):
                token = super().get_token(user)
                return token
        except Employee.DoesNotExist:
            raise Exception("Błędny login lub hasło")



class TokenObtainPairSerializerClient(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        try:
            if(Employee.objects.get(user_id = user.pk)):
                raise Exception("Błędny login lub hasło")
        except Employee.DoesNotExist:
            token = super().get_token(user)
            return token

class BusinessActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessActivity
        fields = (
            "id",
            "name",
            "city",
            "post_code",
            "street",
            "apartment_number",
            "house_number",
            "contact_phone",
            "about",
            "is_active",
        )

class EmployeeSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSpecialization
        fields = (
            "id",
            "name",
        )

class NewEmployeeSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSpecialization
        fields = (
            "name",
        )

class EmployeeFullInfoSerializer(serializers.ModelSerializer):
    user = GetUserInfoSerializer()
    spec = EmployeeSpecializationSerializer()
    class Meta:
        model = Employee
        fields = (
            "id",
            "is_owner",
            "user",
            "business_activity_id",
            "spec",
        )
class UpdateEmployeeSpecSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "spec",
        )
class DistinctServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "id",
            "name", 
        )

class AvailabilitySerializer(serializers.ModelSerializer):
    availability_config_id = serializers.IntegerField()
    class Meta:
        model = EmployeeAvailability
        fields = (
            "date",
            "is_free",
            "is_holiday",
            "is_default",
            "weekday",
            "start_time",
            "end_time",
            "is_break",
            "availability_config_id",
            "created_at"
        )

class AvailabilityConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAvailabilityConfiguration
        fields = (
            "max_weeks_for_registration",
            "min_time_for_registration",
            "employee"
        )

# class EmployeeServices(serializers.ModelSerializer):
#     service = ServiceSerializer()
#     class Meta:
#         model = EmployeeServiceRelation
#         fields = (
#             "service",
#         )