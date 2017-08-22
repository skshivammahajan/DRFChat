from celery import shared_task

from notifications.models import Activity
from notifications.utils import Notifier


@shared_task
def send_activity_notification(activity_id, notification_id):
    activity = Activity.objects.get(id=activity_id)
    notify = False

    if activity.email_status in (Activity.PENDING, Activity.FAILURE):
        activity.email_status = Activity.IN_PROGRESS
        notify = True

    if activity.push_status in (Activity.PENDING, Activity.FAILURE):
        activity.push_status = Activity.IN_PROGRESS
        notify = True

    if notify:
        activity.save()
        Notifier.notify(activity, notification_id)
