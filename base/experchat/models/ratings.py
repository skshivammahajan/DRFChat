from django.db import models
from django.utils.translation import ugettext_lazy as _

from experchat.enumerations import RatingValue
from experchat.models.sessions import EcSession


class SessionRating(models.Model):
    session = models.OneToOneField(
        EcSession,
        on_delete=models.PROTECT,
        verbose_name=_('session'),
        null=False,
    )
    overall_rating = models.PositiveSmallIntegerField(_('overall rating'), choices=RatingValue.choices())
    knowledge_rating = models.PositiveSmallIntegerField(
        _('knowledge rating'),
        choices=RatingValue.choices(),
        null=True,
        blank=True
    )
    communication_rating = models.PositiveSmallIntegerField(
        _('communication rating'),
        choices=RatingValue.choices(),
        null=True,
        blank=True,
    )
    professionalism_rating = models.PositiveSmallIntegerField(
        _('professionalism rating'),
        choices=RatingValue.choices(),
        null=True,
        blank=True,
    )
    text_review = models.TextField(
        _('text review'),
        default='',
        max_length=1000,
    )
    created_timestamp = models.DateTimeField(_('created timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['-created_timestamp']

    def __str__(self):
        return '{session_id}: {overall_rating}'.format(
            session_id=self.session,
            overall_rating=self.overall_rating
        )
