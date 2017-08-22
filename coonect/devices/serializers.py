from django.conf import settings
from rest_framework import serializers

from devices.models import Device
from publisher.utils import ExperchatPublisher


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializes Device model. Used in Device management API.
    """
    device_type = serializers.ChoiceField(choices=['ios', 'android', 'web'])
    publisher = serializers.SerializerMethodField()

    class Meta:
        model = Device
        exclude = ('user', 'status')

    def get_publisher(self, obj):
        if hasattr(obj.user, 'expert'):
            user_type = 'expert'
        else:
            user_type = 'user'

        publish = ExperchatPublisher()

        device_channel = publish.get_device_channel(obj.id)
        user_channel = publish.get_user_channel(obj.user.id, user_type)
        channels = [user_channel, device_channel]

        return {
            'subscribe_key': settings.PUBNUB_SUBSCRIBE_KEY,
            "channels": channels
        }
