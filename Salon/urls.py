from django.urls import path
from django.views.generic.base import View

from Salon.employee.Images import ImagesApi
# from rest_framework import views
from .auth.auth_backend import *
from .auth import auth_backend
from .employee.Calendar import *
from .employee.Service import ServiceApi, ServiceCommentApi, ServiceApiClient
from .employee.employee_info import *
from .employee.service_category import *
from .employee.business_activity import *
from .employee.all_specs import *
from .employee.availability import *
from .client.client_info import *
from .client.business_activity_info import *
from .client.employee_availability import *
from .client.visit import *

urlpatterns = [
    path('api/v1/token/refresh/', CustomTokenRefreshView.as_view(), name = 'token_refresh'),
    path('api/v1/token/verify/', CustomTokenVerifyView.as_view(), name = 'token_verify'),
    path('api/v1/client/token/', CustomTokenObtainPairViewClient.as_view(), name = 'token_obtain_pair_client'),
    path('api/v1/client/info/', ClientApi.as_view(), name = 'client_api'),
    path('api/v1/client/business-activities/', BusinessActivities.as_view(), name = 'business_activities'),
    path('api/v1/client/employee-preview/', ServiceApiClient.as_view(), name = 'services_clients'),
    path('api/v1/client/employee-availability/', ClientEmployeeAvailability.as_view(), name = 'client_employee_availability'),
    path('api/v1/client/visit/', VisitApi.as_view(), name = 'client_register_visit_api'),
    path('api/v1/client/my-visits/', ClientVisitApi.as_view(), name = 'client_my_visit_api'),
    path('api/v1/client/message/', MessageToEmployee.as_view(), name = 'message_to_employee'),

    path('api/v1/user/register/', CustomUserCreate.as_view(), name = "register"),
    path('api/v1/user/check-for-unique-names/', CheckForUniqueNames.as_view(), name = "check_for_unique_names"),
    path('api/v1/user/passwordchange/', ChangePasswordView.as_view(), name = "changepass"),
    path('api/v1/user/activateuser/<uidb64>/<token>/', auth_backend.activate_user, name = 'activate_user'),
    path('api/v1/user/logout/', BlacklistTokenUpdateView.as_view(), name = 'logout'),
    path('api/v1/user/checkresettoken/<uidb64>/<token>/', auth_backend.check_reset_token, name = 'check_reset_token'),
    path('api/v1/user/requestpasswordreset/', RequestPasswordResetEmail.as_view(), name = 'request_passwordreset'),
    path('api/v1/user/passwordresetcomplete/', ResetPassword.as_view(), name = 'password_reset_complete'),
    path('api/v1/user/getuserrole/', GetUserRole.as_view(), name = 'get_user_role'),
    
    path('api/v1/employee/token/', CustomTokenObtainPairViewEmployee.as_view(), name = 'token_obtain_pair_employee'),
    path('api/v1/employee/service/', ServiceApi.as_view(), name = 'service'),
    path('api/v1/employee/images/', ImagesApi.as_view(), name = 'images'),
    path('api/v1/employee/employee-info/', EmployeeApi.as_view(), name = 'employee_info'),
    path('api/v1/employee/employee-avatar/', EmployeeAvatarApi.as_view(), name = 'employee_avatar'),
    path('api/v1/employee/employee-category/', ServiceCategoryApi.as_view(), name = 'employee_category'),
    path('api/v1/employee/comment/', ServiceCommentApi.as_view(), name = 'service_comment'),
    path('api/v1/employee/business-activity/', BusinessActivityApi.as_view(), name = 'business_activity'),
    path('api/v1/employee/all-specs/', EmployeeSpecsApi.as_view(), name = 'all_specs'),
    path('api/v1/employee/create-employee/', CreateEmployee.as_view(), name = 'create_employee'),
    path('api/v1/employee/business-activity-employees/', BusinessActivityEmployeesApi.as_view(), name = 'business_activity_employees'),
    path('api/v1/employee/business-activity-services/', BusinessActivityServices.as_view(), name = 'business_activity_services'),
    path('api/v1/employee/availability/', AvailabilityApi.as_view(), name = 'employee_availability'),
    path('api/v1/employee/non-working-days/', Holidays.as_view(), name = 'non_working_days'),
    path('api/v1/employee/non-working-days-three-years/', HolidaysForThreeYears.as_view(), name = 'non_working_days_three_years'),
    path('api/v1/employee/availability-config/', AvailabilityConfigApi.as_view(), name = 'availability_config'),
    path('api/v1/employee/appointments/', EmployeeApointmentsApi.as_view(), name = 'employee_appointments'),
    path('api/v1/employee/owner-employees/', Employees.as_view(), name = 'owner_employees'),
    path('api/v1/employee/change-visit/', CompleteVisitInfo.as_view(), name = 'change_visit'),
    path('api/v1/employee/new-visit/', DailyWorkHours.as_view(), name = 'employee_new_visit'),
    path('api/v1/employee/services-clients/', EmployeeServicesAndClients.as_view(), name = 'employee_services_with_clients'),
    # path('api/user/isauthenticated/', IsUserAuthenticated.as_view(), name = 'is_authenticated'),
]