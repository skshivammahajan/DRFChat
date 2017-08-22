from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import JSONField

from experchat.models.base import ExperChatBaseModel
from experchat.models.domains import Tag
from experchat.models.users import Expert, ExpertProfile, User
from feeds.choices import FeedProviders, FeedTypes


class SocialAccount(ExperChatBaseModel):
    """
    Model to store the access token Details
    """
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        verbose_name=_('expert'),
        related_name='experts'
    )
    access_token = models.TextField(_('access token'))
    provider = models.CharField(
        _('Social Provider'),
        max_length=15,
        choices=FeedProviders.choices(),
        default=FeedProviders.FACEBOOK.value
    )
    name = models.CharField(_('Page/Channel/User Name'), max_length=100)
    user_id = models.CharField(_('user id'), max_length=255)
    refresh_token = models.CharField(
        _('refresh token'),
        max_length=255,
        blank=True,
        null=True
    )
    access_token_expiry_timestamp = models.DateTimeField(_('access token expiration time'), blank=True, null=True)

    def __str__(self):
        return "{id}: {provider}".format(
            id=self.id,
            provider=self.get_provider_display()
        )


class SocialLink(ExperChatBaseModel):
    """
    Model to store the information of the social links
    """
    account = models.ForeignKey(
        SocialAccount,
        on_delete=models.CASCADE,
        verbose_name=_('Social Account'),
        related_name='social_accounts'
    )
    expert_profiles = models.ManyToManyField(
        ExpertProfile,
        verbose_name=_('Expert Profiles'),
        related_name='social_links'
    )
    feed_type = models.CharField(
        _('Feed Type'),
        max_length=15,
        choices=FeedProviders.choices(),
        default=FeedProviders.FACEBOOK.value
    )
    feed_sub_type = models.CharField(
        _('Feed Sub Type'),
        max_length=10,
        choices=FeedTypes.choices(),
        default=FeedTypes.USER.value
    )
    detail = models.CharField(_('Page/channel/User Id'), max_length=252)
    display_name = models.CharField(_('display name'), max_length=252)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    def __str__(self):
        return "{id} :{feed_type}".format(
            id=self.id,
            feed_type=self.get_feed_type_display()
        )

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class Content(ExperChatBaseModel):
    """
    Model to store the information which are published or unpublished
    """
    content_id = models.CharField(_('content id'), unique=True, max_length=252)
    title = models.CharField(
        _('Content Title'),
        max_length=252,
        blank=True,
        null=True
    )
    content_type = models.CharField(
        _('content type'),
        max_length=15,
        choices=FeedProviders.choices(),
        default=FeedProviders.FACEBOOK.value
    )
    image = models.URLField(
        _('Feed Image URL'),
        max_length=384,
        blank=True,
        null=True
    )
    description = models.TextField(
        _('Feed Description'),
        blank=True,
        null=True
    )
    timestamp = models.DateTimeField(
        _('Original Feed Updated/Posted Time'),
        blank=True,
        null=True
    )
    content = JSONField(_('content'))
    social_link = models.ForeignKey(
        SocialLink,
        on_delete=models.CASCADE,
        verbose_name=_('Social Link'),
        related_name='contents',
        blank=True, null=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Owner of the Feed'),
        related_name='contents'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('tags'),
        related_name='contents',
        blank=True,
    )
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    class Meta:
        ordering = ('-created_timestamp',)

    def __str__(self):
        return "{id}: owner-{owner}".format(
            id=self.content_id,
            owner=self.owner.id
        )

    def delete(self, *args, **kwargs):
        signals.pre_delete.send(
            sender=self.__class__, instance=self, using=kwargs.get('using', None)
        )

        self.is_deleted = True
        self.save()

        signals.post_delete.send(
            sender=self.__class__, instance=self, using=kwargs.get('using', None)
        )

    @cached_property
    def likes(self):
        if hasattr(self, 'stats'):
            return self.stats.likes
        return 0

    def activate(self):
        self.is_deleted = False
        self.save()


class IgnoredContent(ExperChatBaseModel):
    """
    Model to store the information of the ignored content
    """
    content_id = models.CharField(_('content id'), unique=True, max_length=252)
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        verbose_name=_('expert'),
        related_name='ignored_content_experts'
    )

    def __str__(self):
        return "{id}".format(
            id=self.content_id,
        )


class ContentStats(ExperChatBaseModel):
    """
    Model to store the Information of the stats of User
    """
    content = models.OneToOneField(
        Content,
        on_delete=models.CASCADE,
        verbose_name=_('content'),
        related_name='stats'
    )
    likes = models.PositiveIntegerField(_('likes'), default=0)

    def __str__(self):
        return "{id}: content-{content_id}".format(
            id=self.id,
            content_id=self.content.id
        )


class ContentUserActivity(ExperChatBaseModel):
    """
    Model to store the Activity of User on Content.
    """
    LIKE = 'like'
    FAVORITE = 'favorite'

    USER_ACTIVITY_CHOICES = (
        (LIKE, 'Like Content'),
        (FAVORITE, 'Save Content As Favorite'),
    )

    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        verbose_name=_('content'),
        related_name='user_activity'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name='activity',
    )
    activity_type = models.CharField(_('activity type'), max_length=16, choices=USER_ACTIVITY_CHOICES)

    def __str__(self):
        return '{content_id} {user_id} {activity_type}'.format(
            content_id=self.content.id,
            user_id=self.user.userbase_id,
            activity_type=self.activity_type,
        )
