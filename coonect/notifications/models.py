from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import JSONField

from experchat.models.base import ExperChatBaseModel


class Activity(ExperChatBaseModel):
    PENDING = 1
    IN_PROGRESS = 2
    SUCCESS = 3
    FAILURE = 4

    ACTIVITY_STATUS_CHOICES = (
        (PENDING, 'Pending Status'),
        (IN_PROGRESS, 'In progress Status'),
        (SUCCESS, 'Success Status'),
        (FAILURE, 'Failure Status'),
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('actor'),
        related_name='activities',
    )
    notify_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('notification reciever'),
        related_name='notification_activities',
    )
    code = models.CharField(_('activity code'), max_length=32)
    email_status = models.PositiveIntegerField(_('email status'), default=PENDING, choices=ACTIVITY_STATUS_CHOICES)
    push_status = models.PositiveIntegerField(_('push status'), default=PENDING, choices=ACTIVITY_STATUS_CHOICES)
    data = JSONField()

    def __str__(self):
        return "{actor}-<{code}>: {notify_to}".format(
            actor=self.actor,
            code=self.code,
            notify_to=self.notify_to,
        )


class Notification(ExperChatBaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='notifications',
    )
    code = models.CharField(_('activity code'), max_length=32)
    data = JSONField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_timestamp',)

    def __str__(self):
        return "{user}-{code}".format(
            user=self.user,
            code=self.code,
        )
