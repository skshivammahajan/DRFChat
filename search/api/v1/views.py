from collections import OrderedDict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request):
    return Response(OrderedDict([
        ("ExpertProfile Search APIs", OrderedDict([
            ("ExpertProfiles", reverse('v1:expert-list', request=request)),
            ("ExpertProfile", reverse('v1:expert-detail', request=request, args=(1,))),
            ("Tag List", reverse('v1:tag-list', request=request,)),
            ("Random Experts List", reverse('v1:random-experts', request=request, )),
        ])),
        ("Stats APIs", OrderedDict([
            ("Tag Stats", reverse('v1:tagstats-list', request=request)),
            ("Expert Stats", reverse('v1:me-stats', request=request)),
        ])),
    ]))
