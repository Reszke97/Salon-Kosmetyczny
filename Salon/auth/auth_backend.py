from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _
from rest_framework_simplejwt.state import token_backend
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import (
    IsAuthenticated,  
    BasePermission, 
    AllowAny
)
from rest_framework.views import APIView
from ..models import *
from ..serializers import *
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.exceptions import TokenError
# Sending E-Mail
from django.core.mail import EmailMultiAlternatives
import threading
import string
import random
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)
from django.utils.encoding import(
    smart_str,
    smart_bytes,
)
from rest_framework.exceptions import AuthenticationFailed
# Sending E-mail End


#  _   _   ____    _____   ____
# | | | | / ___|  | ____| |  _ \ 
# | | | | \___ \  |  _|   | |_) |
# | |_| |  ___) | | |___  |  _ < 
#  \___/  |____/  |_____| |_| \_\
#

class CheckIfPasswordWasChanged(BasePermission):
    message = 'Hasło właśnie zostało zmienione, zaloguj się ponownie.'

    def has_permission(self, request, view):
        try:
            token = request.headers['Authorization']
            token = token[4:-1]
        except Exception as e:
            return False
        try:
            decoded_payload = token_backend.decode(token, verify=False)
            user_id = decoded_payload['user_id']
            iat = decoded_payload['iat']
            user = User.objects.get(pk = user_id)
            updated_at = user.last_password_update
            updated_at = int(updated_at.timestamp())
        except TokenBackendError:
            raise TokenError(_('Token jest niepoprawny.'))

        if iat > updated_at:
            return True
        else:
            return False


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email_for_employee(user, request):
    current_site = get_current_site(request)
    subject = 'Aktywuj swoje konto'
    email_body = render_to_string('authentication/employee_credentials.html', {
        'user': user.user_name,
        'domain': current_site,
        'password': request.data["password"],
    })
    from_email = settings.EMAIL_FROM_USER
    email = EmailMultiAlternatives( subject, email_body, from_email, to=[user.email] )
    email.mixed_subtype = 'related'
    email.attach_alternative(email_body, "text/html")
    EmailThread(email).start()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    token = RefreshToken()
    token.set_exp(lifetime=timedelta(minutes=10))
    subject = 'Aktywuj swoje konto'
    email_body = render_to_string('authentication/activate.html', {
        'user': user.user_name,
        'domain': current_site,
        'uid': urlsafe_base64_encode(smart_bytes(user.pk)),
        'token': token
    })
    from_email = settings.EMAIL_FROM_USER

    email = EmailMultiAlternatives( subject, email_body, from_email, to=[user.email] )
    email.mixed_subtype = 'related'
    email.attach_alternative(email_body, "text/html")

    # email = EmailMessage(
    #     subject=email_subject, 
    #     body=email_body, 
        
        
    # )
    EmailThread(email).start()
    # email.send()

def activate_user(request, uidb64, token):
    try:
        token_backend.decode(token, verify=True)
    except TokenBackendError:
        return HttpResponse(
            """<html 
                style="max-height:41px"
            >
            <body>
                <pre style="word-wrap: break-word; white-space: pre-wrap;">{"detail":"Token is invalid"}</pre>
            </body>
            </html>""", status=401
        )
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        return HttpResponse(
            """<html 
                style="max-height:41px"
            >
            <body>
                <pre style="word-wrap: break-word; white-space: pre-wrap;">{"detail":"Activation Failed"}</pre>
            </body>
            </html>""", status=401
        )

    if user and user.is_active == False:
        user.is_active = True
        user.save()
        RefreshToken(str(token)).blacklist()
        try:
            if(Employee.objects.get(user_id = user.pk)):
                return redirect('http://localhost:8080/employee/emailactivation/true')
        except Employee.DoesNotExist:
            return redirect('http://localhost:8080/client/emailactivation/true')

    return HttpResponse(
        """<html 
            style="max-height:41px"
        >
        <body>
            <pre style="word-wrap: break-word; white-space: pre-wrap;">{"detail":"Activation Failed"}</pre>
        </body>
        </html>""", status=401
    )
    # return render(request, 'authentication/activatefailed.html', {"user":user})

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        formatted_email = request.data["email"].lower()
        request.data["email"] = formatted_email
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                send_activation_email(user, request)
                messages.add_message(request, messages.SUCCESS, 'Activation link was sent to given email.')
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateEmployee(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def pass_generator(self, size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def post(self, request):
        user = User.objects.get(pk = request.user.pk)
        try:
            employee = Employee.objects.get(user_id = user.pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if employee.is_owner:
            formatted_email = request.data["email"].lower()
            request.data["email"] = formatted_email
            request.data["password"] = self.pass_generator()
            user_serializer = CustomUserSerializer(data={
                'email': request.data["email"],
                'user_name': request.data["userName"],
                'password': request.data["password"],
                'first_name': request.data["name"],
                'last_name': request.data["lastName"],
                'phone_number': request.data["phoneNumber"],
            })
            if user_serializer.is_valid():
                user = user_serializer.save()
                user = User.objects.get(pk=user.pk)
                user.is_active = 1
                user.save()
                if user:
                    if request.data["isNewSpec"]:
                        emp_spec_serializer = NewEmployeeSpecializationSerializer(data={ "name": request.data["employee_spec"] })
                        if emp_spec_serializer.is_valid():
                            spec = emp_spec_serializer.save()
                            request.data["employee_spec"] = spec.pk
                    employee_serializer = EmployeeSerializer(data={
                        "is_owner": 0,
                        "user": user.pk,
                        "business_activity": employee.business_activity_id,
                        "spec": request.data["employee_spec"]
                    })
                    if employee_serializer.is_valid():
                        employee_serializer.save()
                        send_activation_email_for_employee(user, request)
                        messages.add_message(request, messages.SUCCESS, 'Login and password were sent.')
                        return Response(status=status.HTTP_201_CREATED)
                    return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        

class GetUserRole(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_anonymous:
                raise Exception()
        except Exception:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST
            })
        try:
            employee = Employee.objects.get(user_id = request.user.pk)
            if employee.is_owner:
                role = "owner"
            else:
                role = "employee"
        except Employee.DoesNotExist:
            role = "Client"
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'role': role
        }
        return Response(response)


def send_reset_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Zresetuj hasło'
    email_body = render_to_string('authentication/request_passwordchange.html', {
        'user': user.user_name,
        'domain': current_site,
        'uid': urlsafe_base64_encode(smart_bytes(user.pk)),
        'token': PasswordResetTokenGenerator().make_token(user)
    })

    email = EmailMessage(
        subject=email_subject, 
        body=email_body, 
        from_email = settings.EMAIL_FROM_USER,
        to = [user.email]
    )
    EmailThread(email).start()
    # email.send()

class RequestPasswordResetEmail(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            send_reset_email(user, request)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_201_CREATED)
        return Response('Podany email nie istnieje.', status=status.HTTP_404_NOT_FOUND)

def check_reset_token(request, uidb64, token):

    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
    except Exception as e:
        uid = None

    try:
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    
    if user and PasswordResetTokenGenerator().check_token(user, token):
        return redirect('http://localhost:8080/passwordreset?uidb64='+uidb64+'&token='+token)

    return HttpResponse(
        """<html 
            style="max-height:41px"
        >
        <body>
            <pre style="word-wrap: break-word; white-space: pre-wrap;">{"detail":"The reset link is invalid"}</pre>
        </body>
        </html>""", status=401
    )

class ResetPassword(APIView):

    permission_classes = [AllowAny]
    def patch(self, request, *args, **kwargs):

        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = smart_str(urlsafe_base64_decode(request.data["uidb64"]))
                user = User.objects.get(pk=uid)
                if not PasswordResetTokenGenerator().check_token(user, request.data["token"]):
                    raise AuthenticationFailed('The reset token is invalid', 401)
                user.set_password(request.data["password"])
                user.last_password_update = timezone.now()
                user.save()
            except Exception as e:
                raise AuthenticationFailed('The reset link is invalid', 401)
        return Response(status=status.HTTP_200_OK)        

class CustomTokenObtainPairViewClient(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializerClient
class CustomTokenObtainPairViewEmployee(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializerEmployee

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenRefreshSerializer

class CustomTokenVerifyView(TokenVerifyView):
    permission_classes = [AllowAny]
    serializer_class = TokenVerifySerializer


# Logout
class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny,]
    # authentication_classes = ()

    def post(self, request):
        try:
            if request.data["refresh_token"] is not None:
                refresh_token = request.data["refresh_token"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response('Pusty token', status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.last_password_update = timezone.now()
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)