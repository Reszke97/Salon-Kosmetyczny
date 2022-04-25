from django.urls import path
from django.views.generic.base import View
# from rest_framework import views
from .auth_views import *
from . import auth_views
from .employee_views import *


urlpatterns = [
    # User
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/v1/token/refresh/', CustomTokenRefreshView.as_view(), name = 'token_refresh'),
    path('api/v1/token/verify/', CustomTokenVerifyView.as_view(), name = 'token_verify'),
    path('api/v1/user/register/', CustomUserCreate.as_view(), name = "register"),
    path('api/v1/user/passwordchange/', ChangePasswordView.as_view(), name = "changepass"),
    path('api/v1/user/activateuser/<uidb64>/<token>/', auth_views.activate_user, name = 'activate_user'),
    path('api/v1/user/logout/', BlacklistTokenUpdateView.as_view(), name = 'logout'),
    path('api/v1/user/checkresettoken/<uidb64>/<token>/', auth_views.check_reset_token, name = 'check_reset_token'),
    path('api/v1/user/requestpasswordreset/', RequestPasswordResetEmail.as_view(), name = 'request_passwordreset'),
    path('api/v1/user/passwordresetcomplete/', ResetPassword.as_view(), name = 'password_reset_complete'),
    path('api/v1/user/getuserrole/', GetUserRole.as_view(), name= 'get_user_role'),
    path('api/v1/employee/getmonth/', GetMonthDays.as_view(), name= 'get_user_role'),



    
    # path('api/user/isauthenticated/', IsUserAuthenticated.as_view(), name = 'is_authenticated'),
]