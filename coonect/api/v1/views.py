from collections import OrderedDict

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request):
    if not settings.ENABLE_API_ROOT:
        return Response({"version": "v1"})

    return Response(OrderedDict([
        ("Sessions and Actions APIs", OrderedDict([
            ("Session Schedule", reverse('v1:session-schedule', request=request)),
            ("Session Cancel", reverse('v1:session-cancel', request=request, args=(1,))),
            ("Sessions", reverse('v1:session-list', request=request)),
            ("Session Initialize", reverse('v1:session-initialize', request=request, args=(1,))),
            ("Session Accept", reverse('v1:session-accept', request=request, args=(1,))),
            ("Session Decline", reverse('v1:session-decline', request=request, args=(1,))),
            ("Session Disconnect", reverse('v1:session-disconnect', request=request, args=(1,))),
            ("Session Switch Device", reverse('v1:session-switch-device', request=request, args=(1,))),
            ("Session Extend", reverse('v1:session-extend-session', request=request, args=(1,))),
            ("Session Reconnect", reverse('v1:session-reconnect', request=request, args=(1,))),
            ("Session validate Promo code", reverse('v1:validate-promo-code', request=request)),
        ])),
        ("Session Listing APIs", OrderedDict([
            ("Past Sessions", reverse('v1:session-listing', request=request, kwargs={'session_type': 'past'})),
            ("Future Sessions", reverse('v1:session-listing', request=request, kwargs={'session_type': 'future'})),
        ])),
        ("Session Info APIs", OrderedDict([
            ("Session Pricing", reverse('v1:session-pricing', request=request)),
            ("Session Rating", reverse('v1:session-review', request=request, kwargs={'pk': 1})),
        ])),
        ("Devices APIs", OrderedDict([
            ("Devices", reverse('v1:device-list', request=request)),
        ])),
        ("Notification APIs", OrderedDict([
            ("Notifications", reverse('v1:notification-list', request=request)),
            ("Mark notification as read", reverse('v1:notification-mark-read', request=request, kwargs={'pk': 1})),
        ])),
        ("Payments APIs", OrderedDict([
            ("Cards", reverse('v1:card-list', request=request)),
            ("Get Client Token", reverse('v1:get-client-token', request=request)),
        ])),
    ]))
