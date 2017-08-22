from collections import OrderedDict

from django.conf import settings


def paginate_content_results(request, data):
    """
    Util method to make the pagination data
    Args:
        request (obj): Requests
        data (dict): Data which needs to be rendered in Response
    Returns:
        dict with next, previous link and data count
    """
    try:
        offset = int(request.query_params.get('offset', 0))
    except ValueError:
        offset = 0

    try:
        limit = int(request.query_params.get('limit', settings.FEEDS_OFFSET_LIMIT))
    except ValueError:
        limit = settings.FEEDS_OFFSET_LIMIT

    if limit > settings.FEEDS_OFFSET_LIMIT:
        limit = settings.FEEDS_OFFSET_LIMIT

    timestamp = int(request.parser_context['kwargs']['timestamp']) if \
        request.parser_context['kwargs'].get('timestamp') else None

    def _make_url(request):
        http_path = 'https' if request._request.is_secure() else 'http'
        url = "{}://{}{}".format(http_path, request.META['HTTP_HOST'], request.path)
        return url

    def _get_next_link(offset, limit):
        url = _make_url(request)
        next_offset = limit + offset
        return url + "?offset={}&limit={}".format(next_offset, limit)

    def _get_previous_link(offset, limit):
        url = _make_url(request)
        if offset == 0:
            return None
        previous_offset = offset - limit
        if previous_offset < 0:
            previous_offset = 0
        return url + "?offset={}&limit={}".format(previous_offset, limit)

    resulted_data = data[offset: offset + limit]
    return OrderedDict([
        ('metadata', OrderedDict([
            ('count', len(data)),
            ('next', _get_next_link(offset, limit)),
            ('previous', _get_previous_link(offset, limit)),
            ('timestamp', timestamp),
            ('offset', offset)
        ])),
        ('results', resulted_data)
    ])
