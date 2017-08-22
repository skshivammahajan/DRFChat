from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mongoengine import DateTimeField, Document, IntField

from experchat.models.base import ExperChatBaseModel
from experchat.models.users import Tag


class DailyStats(ExperChatBaseModel):
    """
    Store daily tag stats.
    """
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, verbose_name=_('tag'))
    date = models.DateField(verbose_name=_('date'), auto_now=True)
    count = models.PositiveIntegerField(verbose_name=_('count'), default=1)

    class Meta:
        unique_together = ('tag', 'date')

    def __str__(self):
        return "Tag: {tag}, Count: {count}".format(tag=self.tag, count=self.count)


class TagStats(ExperChatBaseModel):
    """
    Store total search count and last week's search count of a tag.
    """
    tag = models.OneToOneField(Tag, on_delete=models.PROTECT, primary_key=True, related_name='stats',
                               verbose_name=_('tag'))
    total_search_count = models.PositiveIntegerField(verbose_name=_('total search'), default=0)
    last_week_search_count = models.PositiveIntegerField(verbose_name=_('last week search'), default=0)

    class Meta:
        ordering = ('-last_week_search_count',)

    def __str__(self):
        return "Tag id : {tag_id}, Last week count = {last_week_count}".format(
            tag_id=self.tag_id,
            last_week_count=self.last_week_search_count
        )


class ExpertAnalytics(Document):
    """
    Store Every Api Hit for Expert Profile Detail in MongoDB.
    """
    user_id = IntField()
    expert_id = IntField()
    expert_profile_id = IntField()
    date = DateTimeField(default=lambda: timezone.now().date())
