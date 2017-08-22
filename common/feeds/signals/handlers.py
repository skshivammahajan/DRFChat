from django.db.models.signals import pre_delete
from django.dispatch import receiver

from feeds.models import Content
from feeds.tasks import delete_content_from_getstream


@receiver(pre_delete, sender=Content)
def remove_content_feeds_getstream(sender, **kwargs):
    """
    Before deleting Content from DataBase, remove content feeds from Getstream.
    """
    instance = kwargs['instance']
    delete_content_from_getstream.delay(
        owner_id=instance.owner_id,
        content_id=instance.id,
    )
