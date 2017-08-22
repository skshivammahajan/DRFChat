from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core import exceptions
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from registration.forms import PasswordResetForm, SetPasswordForm
from registration.models import VerificationToken
from registration.utils import check_verify_notification_spamming

UserBase = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Register a new user or expert based on provided user-type.
    Validates email and password.
    """

    class Meta:
        model = UserBase
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                "error_messages": {
                    "required": "ERROR_REQUIRED",
                    "null": "ERROR_NULL",
                    "blank": "ERROR_BLANK",
                }
            },
            'email': {
                "error_messages": {
                    "invalid": "ERROR_INVALID_EMAIL",
                    "required": "ERROR_REQUIRED",
                    "null": "ERROR_NULL",
                    "blank": "ERROR_BLANK",
                }
            },
        }

    def validate_email(self, value):
        """
        Validate uniqueness of email field.
        """
        user_type = self.context['view'].kwargs['user_type']
        if UserBase.objects.filter(email=value,
                                   **{'%s__isnull' % user_type: False}).exists():
            raise serializers.ValidationError('ERROR_DUPLICATE_EMAIL')
        return value

    def validate_password(self, value):
        try:
            validate_password(password=value)
        except exceptions.ValidationError:
            raise serializers.ValidationError('ERROR_INVALID_PASSWORD')
        return value

    def create(self, validated_data):
        user_type = self.context['view'].kwargs['user_type']
        # Generate default and unique username based on user_type and email.
        if user_type == 'user':
            username = "user_%s" % validated_data['email']
        else:
            username = "expert_%s" % validated_data['email']

        # signup userbase. Note: create user or expert based on user_type in view.
        instance = UserBase.signup(username=username, **validated_data)

        return instance


class AuthTokenSerializer(serializers.Serializer):
    """
    Validates user/expert credentials for login.
    """
    email = serializers.CharField(
        label=_("Email"),
        error_messages={
            "required": "ERROR_REQUIRED",
            "null": "ERROR_NULL",
            "blank": "ERROR_BLANK",
        }
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        error_messages={
            "required": "ERROR_REQUIRED",
            "null": "ERROR_NULL",
            "blank": "ERROR_BLANK",
        }
    )

    def validate(self, attrs):
        """
        Validate credentials for verified-email user/expert and return authenticated UserBase.
        """
        user_type = self.context['view'].kwargs['user_type']
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password, user_type=user_type)

            if user:
                if not user.is_email_verified:
                    msg = 'ERROR_UNVERIFIED_EMAIL'
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = 'ERROR_INVALID_CREDENTIALS'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'ERROR_REQUIRED_VALUE'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    """
    For password change api, validates current and new password.
    """
    current_password = serializers.CharField(
        max_length=28,
        allow_blank=False,
        error_messages={
            "required": "ERROR_REQUIRED",
            "null": "ERROR_NULL",
            "blank": "ERROR_BLANK",
        }
    )
    new_password = serializers.CharField(
        max_length=28,
        allow_blank=False,
        error_messages={
            "required": "ERROR_REQUIRED",
            "null": "ERROR_NULL",
            "blank": "ERROR_BLANK",
        }
    )

    def validate_current_password(self, value):
        request = self.context.get('request')
        if not request.user.check_password(value):
            raise serializers.ValidationError('ERROR_INVALID_CURRENT_PASSWORD')
        return value

    def validate_new_password(self, value):
        try:
            # Apply django password validators
            validate_password(password=value)
        except exceptions.ValidationError:
            raise serializers.ValidationError('ERROR_INVALID_PASSWORD')

        return value

    def validate(self, data):
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError('ERROR_PASSWORD_REUSED')

        return data


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting an email for reset password.
    """
    email = serializers.EmailField(
        error_messages={
            "invalid": "ERROR_INVALID_EMAIL",
            "required": "ERROR_REQUIRED",
            "null": "ERROR_NULL",
            "blank": "ERROR_BLANK",
        }
    )

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):

        """Override this method to change default e-mail options"""
        user_type = self.context['view'].kwargs['user_type']

        return {
            'user_type': user_type,
            'extra_email_context': {
                'frontend_url': getattr(settings, '%s_FRONTEND_URL' % user_type.upper()),
                'password_reset_url': getattr(settings, '%s_PASSWORD_RESET_URL' % user_type.upper()),
            }
        }

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        user_type = self.context['view'].kwargs['user_type']
        try:
            user = UserBase.objects.get(email=value, **{'%s__isnull' % user_type: False})
        except UserBase.DoesNotExist:
            raise serializers.ValidationError('ERROR_NO_EMAIL')

        if check_verify_notification_spamming(user, VerificationToken.PASSWORD_RESET):
            raise serializers.ValidationError('ERROR_MAX_ATTEMPTS_PASSWORD_RESET')

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'email_template_name': 'registration/forgot_password_email.html',
            'html_email_template_name': 'registration/forgot_password_email.html'
        }

        opts.update(self.get_email_options())
        return self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for resetting the password.
    """
    password = serializers.CharField(
        max_length=28,
        style={'input_type': 'password'},
        error_messages={
            "required": "ERROR_REQUIRED",
            "null": "ERROR_NULL",
            "blank": "ERROR_BLANK",
        }
    )
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = UserBase._default_manager.get(pk=uid)

        except (TypeError, ValueError, OverflowError, UserBase.DoesNotExist):
            raise serializers.ValidationError('ERROR_TOKEN_EXPIRED')

        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError('ERROR_INVALID_TOKEN')

        attrs['user'] = self.user
        return attrs

    def save(self):
        self.set_password_form.save()


class ResendVerifyEmailSerializer(serializers.Serializer):
    """
    Serializer for resend email for verification .
    """
    email = serializers.EmailField(
        error_messages={
            "invalid": "ERROR_INVALID_EMAIL",
            "required": "ERROR_REQUIRED",
            "null": "ERROR_NULL",
            "blank": "ERROR_BLANK",
        }
    )

    def validate(self, attrs):
        user_type = self.context['view'].kwargs['user_type']
        try:
            user = UserBase.objects.get(email=attrs['email'], **{'%s__isnull' % user_type: False})
        except UserBase.DoesNotExist:
            raise serializers.ValidationError('ERROR_NO_EMAIL')

        if user.is_email_verified:
            raise serializers.ValidationError('ERROR_EMAIL_ALREADY_VERIFIED')

        if check_verify_notification_spamming(user, VerificationToken.EMAIL_VERIFICATION):
            raise serializers.ValidationError('ERROR_MAX_ATTEMPTS_EMAIL_VERIFY')

        attrs['userbase'] = user
        return attrs
