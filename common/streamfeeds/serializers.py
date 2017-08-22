from rest_framework import serializers

from experchat.models.users import Expert
from experchat.serializers import ExpertSerializer


class UserAggregatedFeedSerializer(serializers.Serializer):
    expert = serializers.SerializerMethodField()
    activity_count = serializers.IntegerField()
    date_created = serializers.DateField()
    verb = serializers.CharField()

    def get_expert(self, obj):
        expert = Expert.objects.filter(userbase=obj['expert'])
        return ExpertSerializer(expert, many=True).data
