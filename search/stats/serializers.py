from rest_framework import serializers

from experchat.serializers import TagSerializer
from stats.models import TagStats


class TagStatsSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = TagStats
        fields = ('tag', 'last_week_search_count', 'total_search_count', )
