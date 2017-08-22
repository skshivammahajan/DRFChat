from django.db.models.signals import pre_save
from django.dispatch import receiver

from experchat.models.users import UserMedia


@receiver(pre_save, sender=UserMedia)
def set_primary_media(sender, instance, **kwargs):
    if instance.is_primary:
        UserMedia.objects.filter(owner=instance.owner, is_primary=True).update(is_primary=False)
