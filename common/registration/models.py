from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from experchat.models.base import ExperChatBaseModel


class VerificationToken(ExperChatBaseModel):
    """
    Store the verification token to verify user and hit count to prevent spamming user.
    Hit count is stored for APIs email verification, phone verification and password reset.
    """
    EMAIL_VERIFICATION = 1
    PHONE_VERIFICATION = 2
    PASSWORD_RESET = 3

    VERIFICATION_PURPOSE_CHOICES = (
        (EMAIL_VERIFICATION, 'Email Verification'),
        (PHONE_VERIFICATION, 'Phone Verification'),
        (PASSWORD_RESET, 'Password Reset'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    token = models.CharField(
        _('verification token'),
        max_length=64,
        db_index=True,
        null=True,  # Nullable for password reset case
        blank=True,
    )
    purpose = models.PositiveSmallIntegerField(
        verbose_name=_('purpose'),
        choices=VERIFICATION_PURPOSE_CHOICES,
        db_index=True,
    )
    notify_count = models.PositiveSmallIntegerField(_('api hit count'), default=1)
    expired_at = models.DateTimeField(_('expired at'), blank=True, null=True)

    class Meta:
        ordering = ('-modified_timestamp',)

    def __str__(self):
        return "{email}-{purpose}".format(
            email=self.user.email,
            purpose=self.get_purpose_display(),
        )

    def perform_verification(self):
        """
        Verify user's email or phone and expire self.
        """
        if self.purpose == self.EMAIL_VERIFICATION:
            self.user.is_email_verified = True
        elif self.purpose == self.PHONE_VERIFICATION:
            self.user.is_phone_number_verified = True

        self.expired_at = timezone.now()

        with transaction.atomic():
            self.user.save()
            self.save()
