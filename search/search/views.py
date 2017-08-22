import pysolr
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from experchat.models.domains import Tag
from experchat.models.users import ExpertProfile
from experchat.serializers import ExpertProfileDetailSerializer, ExpertProfileListSerializer, TagSerializer
from experchat.views import ExperChatAPIView
from search.pagination import paginate_search_results
from search.tasks import calculate_daily_expert_stats
from search.utils import SolrUtils


class TagView(APIView):
    """
        Allows Tag search on the basis of text.

        **Query Parameters**

           -  `search` -- _search text_
           -  `limit` -- _number of items per page_
           -  `offset` -- _pagination offset_
    """

    def get(self, request, format=None):
        queryset = Tag.objects.all()
        search = request.query_params.get('search', '')
        hide_synonym = request.query_params.get('hide_synonym', '0')
        rows = request.query_params.get('limit', '10')
        start = request.query_params.get('offset', '0')

        if start < '0':
            start = '0'

        solr = pysolr.Solr(settings.SOLR_TAG_COLLECTION_URL)

        query_options = {'rows': rows, 'start': start}
        if hide_synonym == '1' and 'fq' not in query_options:
            query_options['fq'] = []
            query_options['fq'].append('-tag_type:synonym')

        result = solr.search(search, **query_options)

        count = result.raw_response["response"]["numFound"]
        queryset = queryset.filter(id__in=[doc['id'] for doc in result.docs])
        response = TagSerializer(queryset, many=True).data
        return Response(paginate_search_results(request, response, count))


class ExpertProfileView(APIView):
    """
    Allows expertprofile search on the basis of expert_id, text or category id.

    **Query Parameters**

       -  `search` -- _search text_
       -  `expert_id` -- _Id of expert_
       -  `tag_ids` -- _tag ids (ex: tag_ids=1,2,3)_
       -  `limit` -- _number of items per page_
       -  `offset` -- _pagination offset_
       -  `sort_by` -- _sort parameters separated by comma_ (eg: sort_by=num_rating,avg_rating,featured)
       -  `min_num_rating` -- _min no of ratings to search the experts_
       -  `min_avg_rating` -- _min avg rating to search the experts_
    """

    def get(self, request, format=None):
        queryset = ExpertProfile.objects.all().select_related('expert').prefetch_related('tags')

        search = request.query_params.get('search', '')

        solr = pysolr.Solr(settings.SOLR_EXPERT_COLLECTION_URL)

        query_options = SolrUtils().solr_queryoptions(request)

        result = solr.search(search, **query_options)

        id_list, no_of_groups = SolrUtils().solr_parse_raw_data(result)

        queryset = queryset.filter(id__in=id_list)
        objects = dict([(str(obj.id), obj) for obj in queryset])
        sorted_objects = [objects[id] for id in id_list if id in objects]
        response = ExpertProfileListSerializer(sorted_objects, many=True, context={'request': request}).data
        return Response(paginate_search_results(request, response, no_of_groups))


class ExpertProfileDetailView(generics.RetrieveAPIView):
    """
    Detailed view for expert profile.
    """
    queryset = ExpertProfile.objects.all().select_related('expert').prefetch_related('tags', 'medias')
    serializer_class = ExpertProfileDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super(ExpertProfileDetailView, self).retrieve(request, *args, **kwargs)

        # Calculate if no exception is raised, i.e. in case of 404 above statement will raise 404 exception
        user_id = 0 if request.user.is_anonymous() else request.user.id
        calculate_daily_expert_stats.delay(user_id, kwargs['pk'])

        return response


class ExpertRandomListView(ExperChatAPIView):
    """
    API for listing all the Expert randomly based on the avg rating and num rating
    """
    queryset = ExpertProfile.objects.order_by('?')
    serializer_class = ExpertProfileListSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(
            expert__avg_rating__gte=getattr(settings, 'EXPERT_RANDOM_LIST_AVG_RATING_MIN_VALUE', 4.0),
            expert__num_rating__gte=getattr(settings, 'EXPERT_RANDOM_LIST_NUM_RATING_VALUE', 5)
        )[:getattr(settings, 'EXPERT_RANDOM_RESULT_LIMIT', 3)]

        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(paginate_search_results(request, serializer.data, len(serializer.data)))
