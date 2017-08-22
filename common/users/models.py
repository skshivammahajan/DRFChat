from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from experchat.models.base import ExperChatBaseModel
from experchat.models.domains import Tag
from experchat.models.users import User


class ExpertAccount(ExperChatBaseModel):
    expert = models.ForeignKey(settings.AUTH_USER_MODEL)
    account_name = models.CharField(max_length=256)
    account_number = models.CharField(max_length=32)
    routing_number = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{id}: {account_name} {account_number}'.format(
            id=self.id if self.id else "",
            account_name=self.account_name,
            account_number=self.account_number,
        )


class FollowTags(ExperChatBaseModel):
    """
    Model class for Tags being followed by the user .
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='following_tags',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name=_('tags'),
        related_name='followers',
    )

    class Meta:
        unique_together = ('user', 'tag')

    def __str__(self):
        return '{id}: {user} {tag}'.format(
            id=self.id if self.id else "",
            user=self.user,
            tag=self.tag
        )
