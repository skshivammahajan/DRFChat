from django.conf import settings

from experchat.patterns import Singleton
from search import tasks


class SolrUtils(metaclass=Singleton):
    """
    Utility class to search results in solr.
    """
    def solr_parse_raw_data(self, result):
        """
        Parse search data received from solr.
        """
        id_list = []
        no_of_groups = ''
        grouped = result.raw_response.get("grouped")
        if grouped:
            expert_id_groups = grouped.get("expert_id")
            if expert_id_groups:
                no_of_groups = expert_id_groups.get("ngroups")
                groups = expert_id_groups.get("groups")
                for data in groups:
                    doclist = data.get("doclist").get("docs")
                    id_list.append(doclist[0].get("id"))
        return id_list, no_of_groups

    def solr_queryoptions(self, request):
        """
        Utility function to parse query parameters from request and return formatted query options.
        """
        sort_params = {'num_rating': 'num_rating desc', 'avg_rating': 'avg_rating desc', 'featured': 'is_featured desc'}
        expert_id = request.query_params.get('expert_id', '')
        tag_ids = request.query_params.get('tag_ids', '')
        sort_by = request.query_params.get('sort_by', '')

        try:
            min_num_rating = int(request.query_params.get('min_num_rating', settings.MIN_NUM_RATINGS))
            min_avg_rating = float(request.query_params.get('min_avg_rating', settings.MIN_AVG_RATINGS))
        except ValueError:
            min_num_rating = settings.MIN_NUM_RATINGS
            min_avg_rating = settings.MIN_AVG_RATINGS

        sort_by = sort_by.replace(' ', '')
        sort_by = sort_by.split(',')

        try:
            start = int(request.query_params.get('offset', 0))
        except ValueError:
            start = 0

        try:
            rows = int(request.query_params.get('limit', settings.SEARCH_RESULTS_LIMIT))
        except ValueError:
            rows = settings.SEARCH_RESULTS_LIMIT
        if rows > settings.SEARCH_RESULTS_LIMIT:
            rows = settings.SEARCH_RESULTS_LIMIT

        # Create query options for solr search
        query_options = {'rows': rows, 'start': start}

        if sort_by:
            query_options['sort'] = ''
            for sort_value in sort_by:
                if sort_params.get(sort_value):
                    query_options['sort'] += ','+sort_params.get(sort_value)
            query_options['sort'] = query_options['sort'][1:]

        if 'fq' not in query_options:
            query_options['fq'] = []
        query_options['fq'].append('avg_rating:['+str(min_avg_rating)+' TO *]')
        query_options['fq'].append('num_rating:['+str(min_num_rating)+' TO *]')

        if expert_id:
            query_options['fq'].append('expert_id:' + expert_id)

        if tag_ids:
            tag_list = tag_ids.split(",")
            if all([x.isdigit() for x in tag_list]):
                tasks.daily_stats.delay(tag_list)  # Call celery task to track expert search via tag_id
                tag_ids = tag_ids.replace(",", " ")
                query_options['fq'].append('((tag_ids:({})) OR (1_up_ids:({})) OR (2_up_ids:({})))'.format(tag_ids,
                                                                                                           tag_ids,
                                                                                                           tag_ids)
                                           )

        query_options['group'] = 'true'
        query_options['group.field'] = 'expert_id'
        query_options['group.ngroups'] = 'true'
        query_options['fl'] = "*"

        return query_options
