from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from experchat.enumerations import ExpertNotificationSettingCodes
from experchat.models.base import ExperChatBaseModel


class ExpertNotificationSettings(ExperChatBaseModel):
    """
    Store Notification Settings for User.
    """
    userbase = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('userbase'),
        related_name='notification_settings',
    )
    code = models.CharField(_('code'), max_length=32, choices=ExpertNotificationSettingCodes.choices())
    status = models.BooleanField(_('code status'), default=True)

    class Meta:
        unique_together = ('userbase', 'code')

    def __str__(self):
        return '{userbase}: {code} {status}'.format(
            user=self.userbase.id,
            code=self.code,
            status=self.status
        )
