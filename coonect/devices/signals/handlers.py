from django.db.models import Q
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from devices.enumerations import DeviceStatus
from devices.models import Device
from publisher.utils import ExperchatPublisher


@receiver(post_save, sender=Device)
def add_push_device_to_publisher(sender, **kwargs):
    """
    Added devices to publisher to send notification.
    """
    if not kwargs.get('created'):
        return

    instance = kwargs['instance']
    user = kwargs['instance'].user
    device_type = kwargs['instance'].device_type

    if device_type is 'web':
        return

    if hasattr(user, 'expert'):
        user_type = 'expert'
    else:
        user_type = 'user'

    ExperchatPublisher().add_push_device(
        instance.user_id,
        user_type,
        instance.id,
        instance.device_token,
        str(instance.device_type).lower()
    )


@receiver(pre_save, sender=Device)
def remove_push_device_before_add(sender, **kwargs):
    """
    Check if device is already registered and remove if true.
    """
    instance = kwargs['instance']
    if hasattr(instance, 'id') and instance.id:
        return

    existing_devices = Device.objects.filter(
        Q(device_token=instance.device_token) | (Q(device_id=instance.device_id) & Q(device_id__isnull=False)),
        device_type=instance.device_type, status=DeviceStatus.ACTIVE.value,
    )

    for device in existing_devices:
        device.delete()


@receiver(pre_delete, sender=Device)
def remove_push_device_from_publisher(sender, **kwargs):
    """
    Before deleting device from DataBase, remove push device from publisher.
    """
    instance = kwargs['instance']
    user = kwargs['instance'].user
    device_type = kwargs['instance'].device_type

    if device_type is 'web':
        return

    if hasattr(user, 'expert'):
        user_type = 'expert'
    else:
        user_type = 'user'

    ExperchatPublisher().remove_push_device(
        user_id=instance.user_id,
        user_type=user_type,
        device_id=instance.id,
        device_token=instance.device_token,
        device_type=str(instance.device_type).lower()
    )
