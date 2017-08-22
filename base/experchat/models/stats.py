from django.db import models
from django.utils.translation import ugettext_lazy as _

from experchat.models.base import ExperChatBaseModel
from experchat.models.users import Expert


class DailyExpertStats(ExperChatBaseModel):
    """
    Store the daily count  for the profile visit of an Expert.
    """
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        verbose_name=_('expert'),
        related_name='daily_stats',
    )
    profile_visits = models.PositiveIntegerField(_('profile visits'), default=0)
    sessions_count = models.PositiveIntegerField(_('sessions count'), default=0)
    date = models.DateField(_('Date'), auto_now_add=True)
    revenue = models.FloatField(default=0)

    class Meta:
        ordering = ('-date', 'expert')

    def __str__(self):
        return "({date}) {expert_id}".format(
            date=self.date,
            expert_id=self.expert_id
        )
