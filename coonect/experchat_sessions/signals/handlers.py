from django.db.models.signals import post_save
from django.dispatch import receiver

from experchat.enumerations import CallStatus
from experchat_sessions.models import Session


@receiver(post_save, sender=Session)
def session_publisher(sender, **kwargs):
    """
    Push notification on expert device if the session is initialized.
    """
    if not kwargs.get('created', False):
        return

    # Do not send push for scheduled sessions
    if kwargs['instance'].call_status != CallStatus.INITIATED.value:
        return

    kwargs['instance'].initialize()
