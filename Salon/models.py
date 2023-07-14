from unicodedata import category, name
from django.db import models
from django.db.models.fields import IntegerField, TextField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        if other_fields.get('is_admin') is not True:
            raise ValueError(
                'Superuser must be assigned to is_admin=True.')
        

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email,user_name,first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        #other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'staffuser must be assigned to is_staff=True.')
        return self.create_user(email, user_name, first_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    last_password_update = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

def upload_path(instance, filename):
    try:
        name = "employee_" + str(instance.employee.pk)
    except:
        name = "business_activity_" + str(str(instance.business_activity.pk))
    return '/'.join(["images", name,filename])
class Appointment(models.Model):
    date = models.CharField(max_length=100)
    time_start = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BusinessActivity(models.Model):
    name = models.CharField(blank=False, max_length=100)
    post_code = models.CharField(blank=False, max_length=45)
    street = models.CharField(blank=False, max_length=45)
    apartment_number = models.CharField(default="", max_length=45, null=True, blank=True)
    house_number = models.CharField(blank=False, max_length=45)
    contact_phone = models.CharField(blank=True, max_length=45)
    city = models.CharField(blank=False, max_length=200)
    about = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BusinessActivityImage(models.Model):
    content = models.ImageField(blank=True, null=True, upload_to=upload_path)
    business_activity = models.ForeignKey(BusinessActivity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class EmployeeSpecialization(models.Model):
    name = models.CharField(blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Employee(models.Model):
    is_owner = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_activity = models.ForeignKey(BusinessActivity, on_delete=models.CASCADE)
    spec = models.ForeignKey(EmployeeSpecialization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmployeeAvatar(models.Model):
    content = models.ImageField(blank=True, null=True, upload_to=upload_path)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ServiceCategory(models.Model):
    name = models.CharField(blank=False, max_length=100)
    is_active = models.BooleanField(default=True)
    styles = models.TextField(blank=True, null=True)
    display_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['display_order']

class Service(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    duration = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(blank=True, null=True)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=True)
    styles = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['display_order']

class EmployeeImageSet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class EmployeeCommentSet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ServiceComment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    text = models.TextField()
    comment_set = models.ForeignKey(EmployeeCommentSet, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class EmployeeImage(models.Model):
    content = models.ImageField(blank=True, null=True, upload_to=upload_path)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    image_set = models.ForeignKey(EmployeeImageSet, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EmployeeServiceConfiguration(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    image_set = models.ForeignKey(EmployeeImageSet, on_delete=models.CASCADE, null=True)
    comment_set = models.ForeignKey(EmployeeCommentSet, on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    styles = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CosmeticProcedure(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    non_user_client = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmployeeAvailabilityConfiguration(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    max_weeks_for_registration = models.IntegerField()
    min_time_for_registration = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmployeeAvailability(models.Model):
    availability_config = models.ForeignKey(EmployeeAvailabilityConfiguration, on_delete=models.CASCADE)
    date = models.CharField(max_length=255, blank=True, null=True)
    is_free = models.BooleanField(default=False)
    is_holiday = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    weekday = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255, blank=True, null=True)
    end_time = models.CharField(max_length=255, blank=True, null=True)
    is_break = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


