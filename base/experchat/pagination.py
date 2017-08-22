from collections import OrderedDict

from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class EcPageNumberPagination(PageNumberPagination):
    """
    Override format of response. Include pagination information in metadata.
    """

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('metadata', OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
            ])),
            ('results', data)
        ]))


class EcLimitOffsetPagination(LimitOffsetPagination):
    """
    Override format of response. Include pagination information in metadata.
    """
    max_limit = getattr(settings, 'MAX_PAGINATION_LIMIT', 50)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('metadata', OrderedDict([
                ('count', self.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
            ])),
            ('results', data)
        ]))
