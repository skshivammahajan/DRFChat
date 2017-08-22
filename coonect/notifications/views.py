from django.conf import settings
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response

from experchat.serializers import EmptySerializer
from notifications.models import Notification
from notifications.pagination import NotificationPagination
from notifications.serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Notification listing API.
    """
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_read',)
    pagination_class = NotificationPagination

    def filter_queryset(self, queryset):
        queryset = super(NotificationViewSet, self).filter_queryset(queryset)
        queryset = queryset.filter(user=self.request.user,
                                   created_timestamp__gt=timezone.now()-timezone.timedelta(settings.NOTIFICATION_DAYS))
        return queryset

    @detail_route(methods=['put'], permission_classes=(permissions.IsAuthenticated,), serializer_class=EmptySerializer)
    def mark_read(self, request, pk=None):
        obj = self.get_object()
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['put'], permission_classes=(permissions.IsAuthenticated,), serializer_class=EmptySerializer)
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
