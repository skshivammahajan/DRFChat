from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    data = serializers.ReadOnlyField()

    class Meta:
        model = Notification
        exclude = ('user',)
