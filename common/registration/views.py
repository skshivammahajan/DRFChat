from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.settings import api_settings

from experchat.authentication import TokenAuthentication
from experchat.messages import get_message
from experchat.models.users import Expert, User
from experchat.views import ExperChatAPIView
from registration.models import VerificationToken
from registration.serializers import (
    AuthTokenSerializer, PasswordChangeSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer,
    ResendVerifyEmailSerializer, UserRegistrationSerializer
)
from registration.utils import send_verification_email
from users.serializers import UserBasicInfoSerializer

UserBase = get_user_model()


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'token', 'uidb64'
    )
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = UserBase.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        userbase = self.perform_create(serializer)
        verification_code = send_verification_email(userbase)

        headers = self.get_success_headers(serializer.data)

        response = {"results": serializer.data}
        response.update(get_message('OK_USER_REGISTERED'))

        if getattr(settings, 'TEST_MODE', False):
            response['results'].update(
                verification_code=verification_code
            )
        return Response(response, headers=headers)

    def perform_create(self, serializer):
        """
        Signup user and create user or expert based on user_type.
        """
        userbase = serializer.save()

        if self.kwargs.get('user_type') == 'user':
            User.objects.create(userbase=userbase)
        else:
            Expert.objects.create(userbase=userbase)

        return userbase


class LoginView(ExperChatAPIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (JSONParser,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request, 'view': self})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = TokenAuthentication.generate_credentials(request, user.id)

        response = {'token': token}
        response.update(UserBasicInfoSerializer(user).data)

        if getattr(settings, 'TEST_MODE', False):
            response.update(id=user.id)

        return Response(response)


class PasswordChangeView(ExperChatAPIView):
    throttle_classes = ()
    parser_classes = (JSONParser,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def post(self, request, user_type, format=None):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(get_message('OK_PASSWORD_CHANGED'))


class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    queryset = UserBase.objects.all()  # Add to avoid exception in browsable api.
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid, token = serializer.save()

        response = get_message('OK_PASSWORD_RESET_EMAIL')

        if getattr(settings, 'TEST_MODE', False):
            results = {
                'email': serializer.validated_data['email'],
                'uid': uid,
                'token': token,
            }
            response.update({'results': results})

        # Return the success message with OK HTTP status
        return Response(response)


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (permissions.AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer.save()

        verification_token_obj = VerificationToken.objects.filter(
            user=user,
            purpose=VerificationToken.PASSWORD_RESET,
            created_timestamp__gt=(
                timezone.now() - timezone.timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRY)
            ),
            expired_at__isnull=True
        ).first()
        if verification_token_obj is not None:
            verification_token_obj.perform_verification()

        return Response(get_message('OK_PASSWORD_RESETED'))


class VerifyEmailView(GenericAPIView):
    """
    Allow user to verify email using email-verification token.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, verification_token=None):
        verification_token_obj = VerificationToken.objects.filter(
            token=verification_token,
            purpose=VerificationToken.EMAIL_VERIFICATION,
            created_timestamp__gt=(timezone.now()-timezone.timedelta(minutes=settings.EMAIL_VERIFICATION_TOKEN_EXPIRY)),
            expired_at__isnull=True
        ).first()

        if verification_token_obj is None:
            return Response({
                "errors": {
                    api_settings.NON_FIELD_ERRORS_KEY: [get_message('ERROR_VERIFICATION_LINK_EXPIRED')]
                }
            })

        verification_token_obj.perform_verification()
        return Response(get_message('OK_EMAIL_VERIFIED'))


class ResendVerifyEmailView(GenericAPIView):
    """
    Resend User Verification e-mail link.

    Returns:
        success message
    Exception:
        If request data is not valid raise the Exception
    """
    queryset = UserBase.objects.all()  # Add to avoid exception in browsable api.
    serializer_class = ResendVerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        userbase = serializer.validated_data['userbase']
        verification_code = send_verification_email(userbase)

        response = get_message('OK_VERIFY_EMAIL')
        if getattr(settings, 'TEST_MODE', False):
            results = {
                'email': serializer.validated_data['email'],
                'verification_code': verification_code,
            }
            response.update({'results': results})
        return Response(response)
