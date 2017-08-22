from django.db import models
from django.utils.translation import ugettext_lazy as _

from experchat.models.users import Expert


class WeekDay(models.Model):
    """
    Model class to represent the weekdays
    """
    DAY_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
    )

    day = models.PositiveSmallIntegerField(
        _('Week Days'),
        choices=DAY_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.get_day_display()


class Calendar(models.Model):
    """
    Model class to represent the Appointments
    """
    title = models.CharField(_('title'), max_length=50)
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        verbose_name=_('expert'),
        related_name='calendars'
    )
    start_time = models.TimeField(_('start time'))
    end_time = models.TimeField(_('end time'))
    week_days = models.ManyToManyField(
        WeekDay,
        verbose_name=_('week days'),
    )
    timezone = models.CharField(_('timezone'), max_length=64)

    def __str__(self):
        return "{expert_id}: {title}".format(
            expert_id=self.expert.id,
            title=self.title
        )
