from collections import OrderedDict

from rest_framework.response import Response

from experchat.pagination import EcLimitOffsetPagination


class NotificationPagination(EcLimitOffsetPagination):

    def paginate_queryset(self, queryset, request, view=None):
        self.unread_count = queryset.filter(is_read=False).count()
        return super(NotificationPagination, self).paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('metadata', OrderedDict([
                ('count', self.unread_count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
            ])),
            ('results', data)
        ]))
