import uuid

from django.conf import settings
from django.utils import timezone

from experchat.utils import custom_send_mail
from registration.models import VerificationToken


def check_verify_notification_spamming(user, purpose):
    """
    Check if notification count is exceeded more than limit.

    Args:
        user: Respective userbase instance.
        purpose: Purpose of notification.
    Returns:
        True if max-limit is reached else return False. In case of False system should send notification again.
    """
    token_expiry = {
        VerificationToken.EMAIL_VERIFICATION: settings.EMAIL_VERIFICATION_TOKEN_EXPIRY,
        VerificationToken.PHONE_VERIFICATION: settings.PHONE_VERIFICATION_TOKEN_EXPIRY,
        VerificationToken.PASSWORD_RESET: settings.PASSWORD_RESET_TOKEN_EXPIRY,
    }[purpose]

    verification_token_obj = VerificationToken.objects.filter(
        user=user,
        purpose=purpose,
        created_timestamp__gt=(timezone.now()-timezone.timedelta(minutes=token_expiry)),
        expired_at__isnull=True
    ).first()
    if verification_token_obj is None:
        return False

    api_limit = {
        VerificationToken.EMAIL_VERIFICATION: settings.RESEND_VERIFY_EMAIL_LIMIT,
        VerificationToken.PHONE_VERIFICATION: settings.RESET_PHONE_OTP_LIMIT,
        VerificationToken.PASSWORD_RESET: settings.RESET_PASSWORD_EMAIL_LIMIT,
    }[purpose]
    if verification_token_obj.notify_count > api_limit:
        return True

    return False


def send_verification_email(user):
    """
    Sends email to verify email on signup or requesting to send verification email again.

    Args:
        user: User base instance.
    Returns:
        Unique verification token to verify email for testing automation.
    """
    verification_token_obj = VerificationToken.objects.filter(
        user=user,
        purpose=VerificationToken.EMAIL_VERIFICATION,
        created_timestamp__gt=(timezone.now()-timezone.timedelta(minutes=settings.EMAIL_VERIFICATION_TOKEN_EXPIRY)),
        expired_at__isnull=True
    ).first()

    if verification_token_obj is None:
        verification_token = uuid.uuid4()
        VerificationToken.objects.create(
            user=user,
            token=verification_token,
            purpose=VerificationToken.EMAIL_VERIFICATION
        )
    else:
        verification_token_obj.notify_count += 1
        verification_token_obj.save()
        verification_token = verification_token_obj.token

    user_type = 'expert' if hasattr(user, 'expert') else 'user'

    mail_context = {
        'verification_token': verification_token,
        'frontend_url': getattr(settings, '%s_FRONTEND_URL' % user_type.upper()),
        'email_verification_url': getattr(settings, '%s_VERIFICATION_EMAIL_URL' % user_type.upper()),
        'fb_logo': getattr(settings, 'AWS_FB_LOGO'),
        'insta_logo': getattr(settings, 'AWS_INSTA_LOGO'),
        'twitter_logo': getattr(settings, 'AWS_TWIT_LOGO'),
        'experchat_logo': getattr(settings, 'AWS_EXPERCHAT_LOGO'),
    }
    custom_send_mail(
        'registration/verification_email_subject.txt',
        'registration/verification_email.txt',
        mail_context,
        user.email,
        html_email_template_name='registration/verification_email.html',
    )

    return verification_token
