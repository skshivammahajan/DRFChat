import json
from copy import deepcopy
from json.decoder import JSONDecodeError

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, TemplateDoesNotExist
from django.template.loader import render_to_string

from experchat.models.notification_setting import ExpertNotificationSettings
from notifications.models import Activity
from publisher.utils import ExperchatPublisher


class Notifier:
    """
    This class provides the implementation of notification methods.
    """

    @classmethod
    def notify(cls, activity, notification_id):

        # Check if user has decided not to receive notification
        if hasattr(activity.notify_to, 'expert'):
            notification_setting = ExpertNotificationSettings.objects.filter(
                userbase=activity.notify_to, code=activity.code).first()
            if notification_setting and not notification_setting.status:
                activity.push_status = Activity.SUCCESS
                activity.email_status = Activity.SUCCESS
                activity.save()
                return

        if activity.push_status == Activity.IN_PROGRESS:
            cls.send_activity_push(activity, notification_id)

        if activity.email_status == Activity.IN_PROGRESS:
            cls.send_activity_email(activity)

    @classmethod
    def send_activity_push(cls, activity, notification_id):
        context = Context(activity.data)

        if hasattr(activity.notify_to, 'expert'):
            user_type = 'expert'
        elif hasattr(activity.notify_to, 'user'):
            user_type = 'user'
        else:
            activity.push_status = Activity.SUCCESS
            activity.save()
            return

        try:
            alert = render_to_string("notifications/push/{0}.txt".format(activity.code), context)
            # Alert *must not* contain newlines
            alert = ''.join(alert.splitlines())

            data_str = render_to_string("notifications/push/{0}.json".format(activity.code), context)
            data = json.loads(data_str)
        except (TemplateDoesNotExist, JSONDecodeError):
            activity.push_status = Activity.SUCCESS
            activity.save()
            return

        message = cls.get_push_message(activity.code, alert, data, notification_id)

        try:
            ExperchatPublisher().publish_message_on_user_devices(activity.notify_to.id, user_type, message)
            activity.push_status = Activity.SUCCESS
        except Exception:
            activity.push_status = Activity.FAILURE

        activity.save()

    @classmethod
    def send_activity_email(cls, activity):
        context = Context(activity.data)
        try:
            subject = render_to_string("notifications/email/{0}_subject.txt".format(activity.code), context)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            message_txt = render_to_string("notifications/email/{0}.txt".format(activity.code), context)
        except TemplateDoesNotExist:
            activity.email_status = Activity.SUCCESS
            activity.save()
            return

        email_message = EmailMultiAlternatives(
            subject,
            message_txt,
            settings.DEFAULT_FROM_EMAIL,
            [activity.notify_to.email]
        )

        try:
            message_html = render_to_string("notifications/email/{0}.html".format(activity.code), context)
            email_message.attach_alternative(message_html, 'text/html')
        except TemplateDoesNotExist:
            pass

        try:
            if "attachments" in activity.data:
                for attachment in activity.data['attachments']:
                    email_message.attach_file(attachment)

            email_message.send()
            activity.email_status = Activity.SUCCESS
        except Exception:
            activity.email_status = Activity.FAILURE

        activity.save()

    @classmethod
    def get_push_message(cls, code, alert, data, notification_id):
        gcm_push_data = deepcopy(data)
        gcm_push_data.update(code=code, message=alert, push_type='notification', notification_id=notification_id)

        return {
            "pn_apns": {
                "aps": {
                    "alert": alert,
                    "badge": 1,
                    "sound": "default",
                    "content-available": 1
                },
                "code": code,
                "data": data,
                "push_type": 'notification',
                "notification_id": notification_id,
            },
            "pn_gcm": {
                "data": gcm_push_data,
            },
        }
