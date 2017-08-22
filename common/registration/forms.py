from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from registration.models import VerificationToken


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password, self.user)
        return password

    def save(self, commit=True):
        password = self.cleaned_data["password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordResetForm(DjangoPasswordResetForm):

    def get_users(self, email, user_type=None):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)

        # If user_type is provided, get users of that user-type only.
        if user_type in ['expert', 'user']:
            active_users = active_users.filter(**{'%s__isnull' % user_type: False})
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None, user_type=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.

        Returns:
            `uid` and `token` to return in API response if TEST_MODE is enabled.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email, user_type):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override

            verification_token_obj = VerificationToken.objects.filter(
                user=user,
                purpose=VerificationToken.PASSWORD_RESET,
                created_timestamp__gt=(
                    timezone.now() - timezone.timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRY)
                ),
                expired_at__isnull=True
            ).first()

            if verification_token_obj is None:
                VerificationToken.objects.create(
                    user=user,
                    purpose=VerificationToken.PASSWORD_RESET
                )
            else:
                verification_token_obj.notify_count += 1
                verification_token_obj.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            context = {
                'email': user.email,
                'name': user.name,
                'domain': domain,
                'site_name': site_name,
                'uid': uid,
                'user': user,
                'token': token,
                'protocol': 'https' if use_https else 'http',
                'fb_logo': getattr(settings, 'AWS_FB_LOGO'),
                'insta_logo': getattr(settings, 'AWS_INSTA_LOGO'),
                'twitter_logo': getattr(settings, 'AWS_TWIT_LOGO'),
                'experchat_logo': getattr(settings, 'AWS_EXPERCHAT_LOGO'),
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user.email, html_email_template_name=html_email_template_name,
            )
        return uid, token
