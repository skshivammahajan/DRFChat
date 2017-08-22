import os
import uuid

from django.conf import settings
from django.core.validators import MaxLengthValidator, MaxValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from experchat.enumerations import ExpertProfileReviewStatus
from experchat.models.base import ExperChatBaseModel
from experchat.models.domains import Tag


class Expert(ExperChatBaseModel):
    """
    Store expert's information.
    """
    userbase = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        primary_key=True,
        verbose_name=_('user base'),
    )
    expert_uid = models.CharField(max_length=5, unique=True, null=True)
    account_id = models.IntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    num_rating = models.PositiveIntegerField(default=0)
    display_name = models.CharField(_('display name'), max_length=100, unique=True, null=True)

    class Meta:
        db_table = "users_expert"

    def __str__(self):
        return '{id}: {userbase}'.format(
            id=self.id if self.id else "",
            userbase=self.userbase,
        )

    @property
    def id(self):
        return self.userbase_id


class User(ExperChatBaseModel):
    """
    Store user's information.
    """
    userbase = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        primary_key=True,
        verbose_name=_('user base'),
    )
    display_name = models.CharField(_('display name'), max_length=100, default='')

    class Meta:
        db_table = "users_user"

    def __str__(self):
        return '{id}: {display_name}'.format(
            id=self.id if self.id else "",
            display_name=self.display_name,
        )

    @property
    def id(self):
        return self.userbase_id


class ExpertProfile(ExperChatBaseModel):
    """
    Information about the profile of an Expert .
    """
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        verbose_name=_('expert'),
        related_name='profiles',
    )
    headline = models.CharField(_('profile headline'), max_length=50)
    summary = models.CharField(_('profile summary'), max_length=1000)
    my_experience = models.TextField(_('experience description'))
    year_of_experience = models.PositiveIntegerField(
        _('experience in years'),
        validators=[
            MaxValueValidator(100),
        ],
        null=True,
        blank=True
    )
    educational_background = models.TextField(
        _('educational background'),
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(Tag, related_name='expert_profiles')
    is_featured = models.BooleanField(_('Is featured Expert'), default=False)
    review_status = models.PositiveSmallIntegerField(
        _('profile review status'),
        choices=ExpertProfileReviewStatus.choices(),
        default=ExpertProfileReviewStatus.NOT_SUBMITTED_FOR_REVIEW.value
    )
    profile_submission_timestamp = models.DateTimeField(_('profile submission datetime'), null=True)

    class Meta:
        db_table = "users_expertprofile"

    def __str__(self):
        return '{id}: {email} {headline}'.format(
            id=self.id if self.id else "",
            email=self.expert.userbase.email,
            headline=self.headline[:20],
        )


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('usermedia', filename)


class UserMedia(ExperChatBaseModel):
    """
    User's Media (Images/Videos) Upload information .
    """
    MEDIA_IMAGE = 'image'
    MEDIA_VIDEO = 'video'
    MEDIA_TYPE_CHOICES = (
        (MEDIA_IMAGE, 'Image'),
        (MEDIA_VIDEO, 'Video'),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('owner'),
        related_name='medias',
    )
    profile = models.ForeignKey(
        ExpertProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('profile'),
        related_name='medias',
    )
    media = models.FileField(upload_to=get_file_path)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    title = models.CharField(max_length=100, default='')
    description = models.TextField(null=True, blank=True, validators=[MaxLengthValidator(1000)])
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "users_media"
        verbose_name = "User Media"

    def __str__(self):
        return '{id}: {email} {media_type}'.format(
            id=self.id if self.id else "",
            email=self.owner.email,
            media_type=self.media_type
        )


class FollowExpert(models.Model):
    """
    Model class for following the Expert
    """
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        verbose_name=_('expert'),
        related_name='followers',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='following',
    )

    created_timestamp = models.DateTimeField(_('created timestamp'), auto_now_add=True)

    class Meta:
        unique_together = ('expert', 'user')

    def __str__(self):
        return '{user}: {expert}'.format(
            user=self.user,
            expert=self.expert
        )
