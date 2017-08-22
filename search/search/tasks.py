from __future__ import absolute_import

import datetime

from celery import shared_task
from django.db.models import F, Sum
from django.utils import timezone

from experchat.models.domains import Tag
from experchat.models.stats import DailyExpertStats
from experchat.models.users import Expert
from stats.models import DailyStats, ExpertAnalytics, TagStats


@shared_task
def daily_stats(tag_ids):
    """
    Task to calculate daily stats of tags.
    """
    existing_tag_stats = DailyStats.objects.filter(date=timezone.now(), tag_id__in=tag_ids)

    existing_tag_stats.update(count=F('count')+1)

    existing_tags = existing_tag_stats.values_list('tag_id', flat=True)
    new_tag_ids = set(map(int, tag_ids)) - set(existing_tags)

    new_stats = []
    new_tags = Tag.objects.filter(id__in=new_tag_ids)
    for tag in new_tags:
        new_stats.append(DailyStats(tag=tag))
    DailyStats.objects.bulk_create(new_stats)


@shared_task
def tags_stats():
    """
    Task to calculate Total and last week stats of tags.
    """
    # Update total search count of tag
    yesterday = timezone.now() - timezone.timedelta(days=1)
    yesterdays_tag_stats = DailyStats.objects.filter(date=yesterday)
    for daily_stat in yesterdays_tag_stats:
        tag_stat, created = TagStats.objects.get_or_create(tag=daily_stat.tag)
        tag_stat.total_search_count += daily_stat.count
        tag_stat.save()

    # Reset last week's search count to 0 before adding this week's results
    # As last week's tag might not have been searched this week.
    TagStats.objects.all().update(last_week_search_count=0)

    # Calculate search count in last week for tags
    last_week_date = timezone.now() - timezone.timedelta(days=7)
    last_week_tag_stats = DailyStats.objects.order_by('tag').filter(date__gt=last_week_date). \
        values('tag').annotate(weekely_count=Sum('count'))
    for tag in last_week_tag_stats:
        tag_stat, created = TagStats.objects.get_or_create(tag_id=tag.get('tag', ''))
        tag_stat.last_week_search_count = tag.get('weekely_count', '')
        tag_stat.save()


@shared_task
def calculate_daily_expert_stats(user_id, expert_profile_id):
    """
    Task to Calculate daily Stats for Expertprofile visits for an expert.
    """
    expert = Expert.objects.filter(profiles=expert_profile_id).first()

    # Storing every api hit for expert profile visit in mongodb
    ExpertAnalytics.objects.create(
        user_id=user_id,
        expert_id=expert.id,
        expert_profile_id=expert_profile_id
    )

    # If user is visiting self profile, don't increment count
    if user_id == expert.userbase.id:
        return

    profile_visits = ExpertAnalytics.objects.filter(
        user_id=user_id,
        expert_id=expert.id,
        expert_profile_id=expert_profile_id,
        date=datetime.date.today()
    ).count()

    # Update profile visit count if user visited the expert-profile for first time today.
    if profile_visits == 1:
        expert_stats_obj, created = DailyExpertStats.objects.get_or_create(
            expert=expert,
            date=timezone.now().date(),
            defaults={'profile_visits': 1},
        )
        if not created:
            expert_stats_obj.profile_visits += 1
            expert_stats_obj.save()
