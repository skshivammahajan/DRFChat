from django.conf import settings
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from experchat.models.users import Expert, ExpertProfile
from experchat.permissions import IsUserPermission
from feeds.models import Content
from feeds.serializers import ContentSerializer
from streamfeeds.serializers import UserAggregatedFeedSerializer
from streamfeeds.utils import StreamHelper, paginate_stream_result, read_content_feeds_getstream
from users.models import FollowTags


class ContentMapMixin(object):
    """
    Mixin class for mapping the stream feeds with content model
    """
    def get_feed_limits(self, request):
        # Check for the defualt limit and offset to be passed to streamfeed
        try:
            offset = int(request.query_params.get('offset', 0))
        except ValueError:
            offset = 0

        try:
            limit = int(request.query_params.get('limit', settings.STREAM_READ_LIMIT))
        except ValueError:
            limit = settings.STREAM_READ_LIMIT

        if limit > settings.STREAM_READ_LIMIT:
            limit = settings.STREAM_READ_LIMIT

        return limit, offset

    def map_to_content_model(self, request, stream_feeds, limit, offset):
        """
        Method to map the Stream feed ids with Content model
        Args:
            request (obj): Requests
            stream_feeds (id): stream_feeds ids
            stream_feed_key (str): stream_feed where we are adding the feeds defind in settings
        Return:
            Serialized data with Content Models
        """
        sorted_objects = read_content_feeds_getstream(stream_feeds)
        response = ContentSerializer(sorted_objects, many=True, context={'request': request}).data
        return paginate_stream_result(request, response, limit, offset)


class ExpertFeedView(APIView, ContentMapMixin):

    def get(self, request, expert_id):
        try:
            expert = Expert.objects.get(userbase_id=expert_id)
        except Expert.DoesNotExist:
            raise Http404

        # Get the offset and limit for pagination
        limit, offset = self.get_feed_limits(request)

        expert_feeds = StreamHelper().get_expert_feed(expert.userbase_id, limit=limit, offset=offset)
        paginated_response = self.map_to_content_model(request, expert_feeds, limit, offset)
        return Response(paginated_response)


class TagFeedFeedView(APIView, ContentMapMixin):

    def get(self, request, tag_id):
        # Get the offset and limit
        limit, offset = self.get_feed_limits(request)
        tag_feeds = StreamHelper().get_tag_feeds(tag_id, limit=limit, offset=offset)
        paginated_response = self.map_to_content_model(request, tag_feeds, limit, offset)
        return Response(paginated_response)


class ExpertProfileFeedView(APIView, ContentMapMixin):

    def get(self, request, expert_profile_id):
        try:
            expert_id = ExpertProfile.objects.get(id=expert_profile_id).expert.userbase_id
        except ExpertProfile.DoesNotExist:
            raise Http404
        # Get the offset and limit
        limit, offset = self.get_feed_limits(request)
        profile_feeds = StreamHelper().get_expert_feed(expert_id, limit=limit, offset=offset)
        paginated_response = self.map_to_content_model(request, profile_feeds, limit, offset)
        return Response(paginated_response)


class SuperAdminFeedView(APIView, ContentMapMixin):
    """
    Api to return the list of SuperAdmin feeds
    """
    def get(self, request):
        # Get the offset and limit
        limit, offset = self.get_feed_limits(request)
        # List of Tag Ids being Followed by the User .
        if hasattr(self.request.user, 'user'):
            followed_tag_ids = FollowTags.objects.filter(user=request.user.user).values_list('tag', flat=True)
            if followed_tag_ids:
                super_admin_feeds = Content.objects.filter(tags__in=followed_tag_ids).values_list('id', flat=True)
            else:
                # If User is not following any Tags , showing the default super-admin feeds
                super_admin_feeds = StreamHelper().get_super_admin_feed(limit=limit, offset=offset)
        else:
            # For Experts or SuperAdmin who don't follow any Tags
            super_admin_feeds = StreamHelper().get_super_admin_feed(limit=limit, offset=offset)
        paginated_response = self.map_to_content_model(request, super_admin_feeds, limit, offset)
        return Response(paginated_response)


class GlobalUserFeedView(APIView, ContentMapMixin):
    """
    Api to return the list of Global User feeds
    """
    def get(self, request):
        # Get the offset and limit
        limit, offset = self.get_feed_limits(request)
        user_global_feeds = StreamHelper().get_user_global_feed(limit=limit, offset=offset)
        paginated_response = self.map_to_content_model(request, user_global_feeds, limit, offset)
        return Response(paginated_response)


class FollowingExpertFeeds(APIView, ContentMapMixin):
    """
    Api to return the list of feeds of Expert followed by User
    """
    permission_classes = (IsUserPermission,)

    def get(self, request, *args, **kwargs):
        # Get the offset and limit
        limit, offset = self.get_feed_limits(request)
        user_expert_followed_feeds = StreamHelper().get_user_expert_followed_feeds(
            request.user.user, limit=limit, offset=offset
        )
        paginated_response = self.map_to_content_model(request, user_expert_followed_feeds, limit, offset)
        return Response(paginated_response)


class FollowingTagFeeds(APIView, ContentMapMixin):
    """
    Api to return the list of feeds for Tag followed by User
    """
    permission_classes = (IsUserPermission,)

    def get(self, request, *args, **kwargs):
        # Get the offset and limit
        limit, offset = self.get_feed_limits(request)
        user_tag_followed_feeds = StreamHelper().get_user_tag_followed_feeds(
            request.user.user, limit=limit, offset=offset
        )
        paginated_response = self.map_to_content_model(request, user_tag_followed_feeds, limit, offset)
        return Response(paginated_response)


class UserAggregatedTimelineFeeds(APIView):
    """
    Api to return the list of feeds for Tag followed by User
    """
    permission_classes = (IsUserPermission,)

    def get(self, request, *args, **kwargs):
        # Check for the defualt limit and offset to be passed to streamfeed
        try:
            offset = int(request.query_params.get('offset', 0))
        except ValueError:
            offset = 0

        try:
            limit = int(request.query_params.get('limit', settings.STREAM_READ_LIMIT))
        except ValueError:
            limit = settings.STREAM_READ_LIMIT

        if limit > settings.STREAM_READ_LIMIT:
            limit = settings.STREAM_READ_LIMIT
        aggregated_timeline_feeds = StreamHelper().get_user_aggregated_timeline_feeds(
            request.user.user, limit=limit, offset=offset
        )
        response = UserAggregatedFeedSerializer(aggregated_timeline_feeds, many=True).data
        return Response(paginate_stream_result(request, response, limit, offset))
