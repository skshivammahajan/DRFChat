from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateField
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from experchat.exceptions import InvalidDateFormat
from experchat.models.stats import DailyExpertStats
from experchat.permissions import IsExpertPermission
from stats.models import TagStats
from stats.serializers import TagStatsSerializer


class TagStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Allow user to manage daily stats.
    """
    serializer_class = TagStatsSerializer
    queryset = TagStats.objects.all().select_related("tag")
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('last_week_search_count', 'total_search_count')

    def filter_queryset(self, queryset):
        queryset = super(TagStatsViewSet, self).filter_queryset(queryset)

        limit = self.request.query_params.get('limit', '10')
        if not limit.isdigit():
            limit = 10

        return queryset[:int(limit)]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailyExpertStatsView(APIView):
    """
    API for Daily Stats for experts.

    **Query Parameters**

    - `from_date`: _date_, start date (default to one week before to_date)
    - `to_date`: _date_, end date (default to today's date)
    - `stats`: 'profile_visits', 'sessions_count', 'revenue'

    Example:

        ?from_date=2017-03-21&to_date=2017-03-24&stats=profile_visits&stats=sessions_count
    """
    permission_classes = (IsExpertPermission,)

    def get(self, request, *args, **kwargs):
        """
        Return response in below format:

        {
            "results": {
                "sessions_count": {
                    "summary": [
                        {
                            "count": 2,
                            "date": "2017-03-18"
                        },
                        {
                            "count": 0,
                            "date": "2017-03-20"
                        }
                    ],
                    "total": 2
                },
                "profile_visits": {
                    "summary": [
                        {
                            "count": 5,
                            "date": "2017-03-18"
                        },
                        {
                            "count": 2,
                            "date": "2017-03-20"
                        }
                    ],
                    "total": 7
                },
                "revenue": {
                    "total": 30.0,
                    "summary": [
                        {
                            "count": 30.0,
                            "date": "2017-04-11"
                        }
                    ]
                }
            }
        }
        """
        queryset = DailyExpertStats.objects.order_by('-date').filter(expert=request.user.expert)

        from_date = None
        try:  # if user passes invalid format date, raise exception
            to_date = DateField().to_internal_value(self.request.query_params.get('to_date', timezone.now().date()))
            if self.request.query_params.get('from_date'):
                from_date = DateField().to_internal_value(self.request.query_params.get('from_date'))
        except ValidationError:
            raise InvalidDateFormat

        queryset = queryset.filter(date__lte=to_date)
        if from_date:
            queryset = queryset.filter(date__gte=from_date)

        valid_stats = ['profile_visits', 'sessions_count', 'revenue']
        stats = [stat for stat in self.request.query_params.getlist('stats') if stat in valid_stats]
        if not stats:
            stats = valid_stats

        response = dict([(stat, {'total': 0, 'summary': []}) for stat in stats])

        for stat_obj in reversed(queryset.values()[:settings.DEFAULT_EXPERT_STATS_TENURE]):
            for stat in stats:  # stats in ['profile_visits', 'sessions_count']
                # response['profile_visits']['total'] = {
                #     'date': <date>,
                #     'profile_visits': <count>
                # }['profile_visits']
                if stat_obj[stat]:
                    response[stat]['total'] += stat_obj[stat]
                    response[stat]['summary'].append({'date': stat_obj['date'], 'count': stat_obj[stat]})

        if not self.request.query_params.get('from_date'):
            for stat in stats:
                response[stat]['total'] = queryset.aggregate(Sum(stat)).get('%s__sum' % stat)
        return Response(response)
