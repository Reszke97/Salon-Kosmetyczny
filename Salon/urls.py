from django.urls import path
from django.views.generic.base import View
# from rest_framework import views
from .auth.auth_backend import *
from .auth import auth_backend
from .employee.Calendar import *
from .employee.Service import *
from .client.client_info import *


urlpatterns = [
    # User

    path('api/v1/client/token/', CustomTokenObtainPairViewClient.as_view(), name = 'token_obtain_pair_client'),
    path('api/v1/employee/token/', CustomTokenObtainPairViewEmployee.as_view(), name = 'token_obtain_pair_employee'),
    path('api/v1/token/refresh/', CustomTokenRefreshView.as_view(), name = 'token_refresh'),
    path('api/v1/token/verify/', CustomTokenVerifyView.as_view(), name = 'token_verify'),
    path('api/v1/user/register/', CustomUserCreate.as_view(), name = "register"),
    path('api/v1/user/passwordchange/', ChangePasswordView.as_view(), name = "changepass"),
    path('api/v1/user/activateuser/<uidb64>/<token>/', auth_backend.activate_user, name = 'activate_user'),
    path('api/v1/user/logout/', BlacklistTokenUpdateView.as_view(), name = 'logout'),
    path('api/v1/user/checkresettoken/<uidb64>/<token>/', auth_backend.check_reset_token, name = 'check_reset_token'),
    path('api/v1/user/requestpasswordreset/', RequestPasswordResetEmail.as_view(), name = 'request_passwordreset'),
    path('api/v1/user/passwordresetcomplete/', ResetPassword.as_view(), name = 'password_reset_complete'),
    path('api/v1/user/getuserrole/', GetUserRole.as_view(), name= 'get_user_role'),
    path('api/v1/employee/getmonth/', GetMonthDays.as_view(), name= 'get_month'),
    path('api/v1/employee/postnewservice/', ServiceApi.as_view(), name= 'post_new_service'),
    path('api/v1/client/info/', ClientApi.as_view(), name= 'client_api'),



    
    # path('api/user/isauthenticated/', IsUserAuthenticated.as_view(), name = 'is_authenticated'),
]