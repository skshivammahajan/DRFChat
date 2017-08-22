import json
from json import JSONDecodeError

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context, TemplateDoesNotExist
from django.template.loader import render_to_string

from notifications.models import Activity, Notification
from notifications.tasks import send_activity_notification


@receiver(post_save, sender=Activity)
def send_notification(sender, instance, created, **kwargs):
    if created:

        context = Context(instance.data)
        try:
            alert = render_to_string("notifications/push/{0}.txt".format(instance.code), context)
            # Alert *must not* contain newlines
            alert = ''.join(alert.splitlines())

            data_str = render_to_string("notifications/push/{0}.json".format(instance.code), context)
            data = json.loads(data_str)
        except (TemplateDoesNotExist, JSONDecodeError):
            send_activity_notification.delay(instance.id, None)
            return

        notification = Notification.objects.create(
            user=instance.notify_to,
            code=instance.code,
            message=alert,
            data=data,
        )
        send_activity_notification.delay(instance.id, notification.id)
