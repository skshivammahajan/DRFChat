from collections import OrderedDict

import stream
from django.conf import settings

from feeds.models import Content


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class StreamHelper(metaclass=Singleton):
    """
    This class provides the implementation of Getstream for publishing expert feeds.
    """

    client = None

    def __init__(self):
        self.client = stream.connect(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)

    def get_user_timeline(self, user, time_line_name):
        """
        Method to initaiate the client timeline
        Args:
            user (object): user object who is going to follow unfollow
            time_line_name (str): tag or expert for which timeline will be initiated
        return:
            get_stream_timeline_obj
        Example:
            get_stream_timeline_obj will be created for bellow keys
            "timeline:1_tag" and timline:1_expert"
        """
        return self.client.feed(
            settings.STREAM_FEEDS_USER,
            "{user_id}_{timeline}".format(user_id=user.id, timeline=time_line_name)
        )

    def get_aggregated_timeline(self, user, time_line_name):
        """
        Method to initaiate the client timeline
        Args:
            user (object): user object who is going to follow unfollow
            time_line_name (str): tag or expert for which timeline will be initiated
        return:
            get_stream_timeline_obj
        Example:
            get_stream_timeline_obj will be created for bellow keys
            "timeline:1_tag" and timline:1_expert"
        """
        return self.client.feed(
            settings.USER_AGGREGATED_TIMELINE_FEED,
            "{user_id}_{timeline}".format(user_id=user.id, timeline=time_line_name)
        )

    def expert_publish_content(self, expert_user, content, expert_profile_ids=None,
                               tag_ids=None, super_admin=False):
        """
        Post the feed on Getstream.
        Args:
            expert_user : The id of expert logged in.
            content : id of content type
            expert_profile_ids: IDs of profiles associated with expert.
            tag_ids (list): IDs of tags associated with expert profiles.
            super_admin (boolean): Flag for Super Admin
        """
        expert_feed = self.client.feed(settings.STREAM_FEEDS_EXPERTS, expert_user)

        to_stream = self.get_streams(expert_profile_ids, tag_ids, super_admin)

        activity = {
            'actor': expert_user,
            'verb': settings.STREAM_VERBS_POST,
            'object': content,
            'foreign_id': content,
            'to': to_stream
        }
        return expert_feed.add_activity(activity)

    def get_streams(self, expert_profile_ids, tag_ids, super_admin):
        """
        Provide list for Getstream to copy feeds.

        Args:
            expert_profile_ids: IDs of profiles associated with expert.
            tag_ids: IDs of tags associated with expert profiles.
            super_admin (boolean) : Boolean Flag for Superadmin.

        Returns:
            Feed List
        """
        # to_expertprofiles = self.get_expert_profiles(expert_profile_ids)
        to_expertprofiles = []
        to_global_user = []
        to_tags = self.get_tags(tag_ids)
        to_super_admin = self.get_super_admin(super_admin)
        if super_admin is False:
            to_global_user = self.get_user_global()

        return to_expertprofiles + to_tags + to_super_admin + to_global_user

    def get_expert_profiles(self, expert_profile_ids):
        """
        Provide Expert Profile list for Getstream.

        Args:
            expert_profile_ids: IDs of profiles associated with expert.

        Returns:
            Expert Profile list.
        """
        if expert_profile_ids is None:
            return []

        feed_name = settings.STREAM_FEEDS_EXPERT_PROFILE

        expert_profiles = []
        for expert_profile_id in expert_profile_ids:
            expert_profiles.append(feed_name + ':' + str(expert_profile_id))

        return expert_profiles

    def get_tags(self, tag_ids=None):
        """
        Provide Tag list for Getstream.

        Args:
            tag_ids: IDs of tags associated with expert profiles.

        Returns:
            Tag List.
        """
        if tag_ids is None:
            return []

        feed_name = settings.STREAM_FEEDS_TAG

        tags = []
        for tag_id in tag_ids:
            tags.append(feed_name + ':' + str(tag_id))

        return tags

    def get_super_admin(self, super_admin):
        """
        Provide Super admin list for Getstream.

        Args:
            super_admin: IDs of super_admin associated with expert profiles.

        Returns:
            Tag List.
        """
        if not super_admin:
            return []

        feed_name = settings.STREAM_FEEDS_USER
        # formating with static int for adding all expert feeds to this feed
        super_admin = feed_name + ':{}'.format(settings.STREAM_STATIC_SUPERADMIN_FEED)
        return [super_admin]

    def get_user_global(self):
        """
        Provide user list of GetStrem
        Returns:
            user List.
        """
        global_feed = settings.STREAM_FEEDS_USER
        # formating with static int for adding all expert feeds to this feed
        return [global_feed + ':{}'.format(settings.STREAM_STATIC_GLOBAL_FEED)]

    def follow_tags(self, followed_tags, user):
        """
        Method for following the tags
        Args:
            followed_tags (object): FollowTags Object
            user (obj): user who is following the tags
        return:
            None
        """
        tags_timeline = self.get_user_timeline(user, settings.STREAM_FEEDS_TAG)
        for followed_tag in followed_tags:
            tags_timeline.follow(settings.STREAM_FEEDS_TAG, followed_tag.tag_id, activity_copy_limit=1000)

    def unfollow_tags(self, tag_ids, user):
        """
        Method for unfollowing the tags
        Args:
            tag_ids (list): tag ids
            user (obj): user who is following the tags
        return:
            None
        """
        tags_timeline = self.get_user_timeline(user, settings.STREAM_FEEDS_TAG)
        for tag_id in tag_ids:
            tags_timeline.unfollow(settings.STREAM_FEEDS_TAG, tag_id)

    def follow_experts(self, expert_id, user):
        """
        Method for following the experts
        Args:
            expert_id (integer): expert id
            user (obj): user who is following the expert
        return:
            None
        """
        expert_timeline = self.get_user_timeline(user, settings.STREAM_FEEDS_EXPERTS)
        aggregated_time_line = self.get_aggregated_timeline(user, settings.STREAM_FEEDS_EXPERTS)
        expert_timeline.follow(settings.STREAM_FEEDS_EXPERTS, expert_id, activity_copy_limit=1000)
        aggregated_time_line.follow(settings.STREAM_FEEDS_EXPERTS, expert_id, activity_copy_limit=1000)

    def unfollow_expert(self, expert_id, user):
        """
        Method for following the experts
        Args:
            expert_id (integer): expert id
            user (obj): user who is following the expert
        return:
            None
        """
        expert_timeline = self.get_user_timeline(user, settings.STREAM_FEEDS_EXPERTS)
        aggregated_time_line = self.get_aggregated_timeline(user, settings.STREAM_FEEDS_EXPERTS)
        expert_timeline.unfollow(settings.STREAM_FEEDS_EXPERTS, expert_id)
        aggregated_time_line.unfollow(settings.STREAM_FEEDS_EXPERTS, expert_id)

    # By default it will give 25 feeds if no limit defined
    def get_expert_feed(self, expert_user_id, limit=settings.STREAM_READ_LIMIT, offset=0):
        feed_type = settings.STREAM_FEEDS_EXPERTS
        return self.get_feed_from_stream(feed_type, expert_user_id, limit, offset)

    def get_tag_feeds(self, tag_id, limit=settings.STREAM_READ_LIMIT, offset=0):
        feed_type = settings.STREAM_FEEDS_TAG
        return self.get_feed_from_stream(feed_type, tag_id, limit, offset)

    def get_expert_profile_feed(self, expert_profile_id, limit=settings.STREAM_READ_LIMIT, offset=0):
        feed_type = settings.STREAM_FEEDS_EXPERT_PROFILE
        return self.get_feed_from_stream(feed_type, expert_profile_id, limit, offset)

    def get_super_admin_feed(self, limit=settings.STREAM_READ_LIMIT, offset=0):
        feed_type = settings.STREAM_FEEDS_USER
        return self.get_feed_from_stream(feed_type, settings.STREAM_STATIC_SUPERADMIN_FEED, limit, offset)

    def get_feed_from_stream(self, feed_type, feed_key_id, limit=settings.STREAM_READ_LIMIT, offset=0):
        stream_feed = self.client.feed(feed_type, feed_key_id)
        activities = stream_feed.get(limit=limit, offset=offset)['results']
        return [activity['object'] for activity in activities]

    def get_aggregated_feeds_from_stream(self, feed_type, feed_key_id, limit=settings.STREAM_READ_LIMIT, offset=0):
        stream_feed = self.client.feed(feed_type, feed_key_id)
        activities = stream_feed.get(limit=limit, offset=offset)['results']
        aggregated_feeds_list = []
        for activity in activities:
            expert_id, date = activity['group'].split('_')
            aggregated_feeds_list.append({
                'activity_count': activity['activity_count'],
                'expert': expert_id,
                'date_created': date,
                'verb': activity['verb']
            })
        return aggregated_feeds_list

    def remove_content_tag_feeds(self, content_id, tag_id):
        feed_type = settings.STREAM_FEEDS_TAG
        return self.remove_feed_from_stream(feed_type, tag_id, content_id)

    def remove_content_feeds(self, owner_id, content_id):
        feed_type = settings.STREAM_FEEDS_EXPERTS
        return self.remove_feed_from_stream(feed_type, owner_id, content_id)

    def remove_feed_from_stream(self, feed_type, feed_key_id, foreign_id):
        stream_feed = self.client.feed(feed_type, feed_key_id)
        stream_feed.remove_activity(foreign_id=foreign_id)

    def get_user_global_feed(self, limit=settings.STREAM_READ_LIMIT, offset=0):
        feed_type = settings.STREAM_FEEDS_USER
        return self.get_feed_from_stream(feed_type, settings.STREAM_STATIC_GLOBAL_FEED, limit, offset)

    def get_user_expert_followed_feeds(self, user, limit=settings.STREAM_READ_LIMIT, offset=0):
        feed_type = settings.STREAM_FEEDS_USER
        feed_key = "{}_{}".format(user.id, settings.STREAM_FEEDS_EXPERTS)
        return self.get_feed_from_stream(feed_type, feed_key, limit, offset)

    def get_user_tag_followed_feeds(self, user, limit=settings.STREAM_READ_LIMIT, offset=0):
        feed_type = settings.STREAM_FEEDS_USER
        feed_key = "{}_{}".format(user.id, settings.STREAM_FEEDS_TAG)
        return self.get_feed_from_stream(feed_type, feed_key, limit, offset)

    def get_user_aggregated_timeline_feeds(self, user, limit=settings.STREAM_READ_LIMIT, offset=0):
        feed_type = settings.USER_AGGREGATED_TIMELINE_FEED
        feed_key = "{}_{}".format(user.id, settings.STREAM_FEEDS_EXPERTS)
        return self.get_aggregated_feeds_from_stream(feed_type, feed_key, limit, offset)


def paginate_stream_result(request, data, limit, offset):
    """
    Util method to make the pagination data
    Args:
        request (obj): Requests
        data (dict): Data which needs to be rendered in Response
    Returns:
        dict with next, previous link and data count
    """
    return OrderedDict([
        ('metadata', OrderedDict([
         ('count', len(data)),
         ('next', _get_next_link(request, offset, limit, data)),
         ('previous', _get_previous_link(request, offset, limit)),
         ('offset', offset)
         ])),
        ('results', data)
        ])


def _make_url(request):
    http_path = 'https' if request._request.is_secure() else 'http'
    url = "{}://{}{}".format(http_path, request.META['HTTP_HOST'], request.path)
    return url


def _get_next_link(request, offset, limit, data):
    url = _make_url(request)
    next_offset = offset + limit
    if len(data) < limit:
        return None

    return url + "?offset={}&limit={}".format(next_offset, limit)


def _get_previous_link(request, offset, limit):
    url = _make_url(request)
    if offset == 0:
        return None
    previous_offset = offset - limit
    if previous_offset < 0:
        previous_offset = 0
    return url + "?offset={}&limit={}".format(previous_offset, limit)


def read_content_feeds_getstream(feed_ids):
    queryset = Content.objects.filter(id__in=feed_ids)
    objects = dict([(str(obj.content_id), obj) for obj in queryset])
    expert_feeds_ids = [str(obj.content_id) for obj in queryset]
    sorted_objects = [objects[feed_id] for feed_id in expert_feeds_ids]
    return sorted_objects


class DummyStreamHelper(StreamHelper):

    def __init__(self):
        return

    def expert_publish_content(self, expert_user, content, expert_profile_ids=None,
                               tag_ids=None, super_admin=False):
        return {}

    def get_expert_feed(self, expert_user_id, limit=settings.STREAM_READ_LIMIT, offset=0):
        return []

    def get_tag_feeds(self, tag_id, limit=settings.STREAM_READ_LIMIT, offset=0):
        return []

    def get_super_admin_feed(self, limit=settings.STREAM_READ_LIMIT, offset=0):
        return []

    def get_user_global_feed(self, limit=settings.STREAM_READ_LIMIT, offset=0):
        return []

    def get_user_expert_followed_feeds(self, user_id, limit=settings.STREAM_READ_LIMIT, offset=0):
        return []

    def get_user_tag_followed_feeds(self, user_id, limit=settings.STREAM_READ_LIMIT, offset=0):
        return []


if settings.TEST_MODE:
    StreamHelper = DummyStreamHelper
