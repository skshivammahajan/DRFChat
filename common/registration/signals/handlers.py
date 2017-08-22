from django.db.models.signals import post_save
from django.dispatch import receiver

from experchat.models.users import Expert, ExpertProfile


@receiver(post_save, sender=Expert)
def create_expert_profile(sender, **kwargs):
    """
    After creating expert, create expert profile.
    """
    if kwargs['created']:
        ExpertProfile.objects.create(expert=kwargs['instance'])
