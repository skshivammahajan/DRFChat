from django.utils import timezone

from experchat.enumerations import TagTypes
from experchat.models.domains import Tag
from feeds.models import Content, IgnoredContent
from feeds.tasks import modify_tags_on_getstream
from streamfeeds.utils import StreamHelper


def validate_access_token(db_time, expire_time):
    """
    this method is used to validate the access_token, based on the current time and actual expiration time of
    the access_token
    Args:
        db_time (obj): Saved time
        expire_time (time): seconds
    Return:
        Boolean True or False
    """
    try:
        # this is cheked to compare the two times, if one is not having
        # timezone, then we can't compare
        db_time.tzinfo
    except AttributeError:
        return False
    current_time = timezone.now()
    time_difference = current_time - db_time
    difference_in_second = time_difference.total_seconds()
    if difference_in_second < 0 or round(difference_in_second) < expire_time:
        return True
    return False


class PushFeeds(object):
    """
    This class will have methods which will be publishing the feeds to stramfeeds
    """

    def __init__(self, social_link_obj):
        self.social_link = social_link_obj

    def push_feeds_to_streamfeed(self, content):
        """
        Method which will be used to call the util method of stream feed
        Args:
            content (obj): instance of content
        return:
        """
        tags = content.tags.all()

        tag_ids = list(get_tag_ids_with_parent(tags))

        expert_user_id = self.social_link.account.expert.userbase.id
        stream_feed_helper = StreamHelper()
        stream_feed_helper.expert_publish_content(
            expert_user_id, content.id, expert_profile_ids=None, tag_ids=tag_ids
        )

    def tag_objs(self):
        """
        will get the list of all tags associated with the expert
        return:
            tag_objs (list): list of tag objects
        """
        # tags = Tag.objects.filter(expert_profiles__social_links=self.social_link.id).distinct()
        tags = Tag.objects.filter(expert_profiles__expert=self.social_link.account.expert).distinct()
        return [tag for tag in tags]


class PushSuperAdminFeeds(object):
    """
    This class will be used to push super admin published feeds and tags to streamfeed
    """

    def __init__(self, userbase):
        self.userbase = userbase

    def push_super_admin_feeds(self, content, tag_ids, super_admin=False):
        """
        push the super admin feeds tags to streamfeed
        Args:
            content (obj): instance of content
            tag_ids (list): list of tag ids
            super_admin (Boolean): False or true, by default False
        return:
        """
        result = StreamHelper().expert_publish_content(
            self.userbase.id, content.id, [], tag_ids, super_admin
        )
        return result


def validate_feed_data(feed):
    """
    Util method to check if the provided feed is a valid feed as per unify_feeds
    Args:
        feed (dict) : feed data
    return:
        Boolean: True or False
    """
    return (
        all([feed.get('id'), feed.get('title'), feed.get('link')]) and
        any([feed.get('updated_parsed'), feed.get(
            'created_parsed'), feed.get('published_parsed')])
    )


def validate_feed_list_data(feeds):
    """
    Util method to check if the provided feed is a valid feed as per unify_feeds
    Args:
        feeds (dict) : list of feed data
    return:
        Boolean: True or False
    """
    for feed in feeds:
        if not all([feed.get('id'), feed.get('title'), feed.get('link')]):
            return False

    return True


def update_content_tags_at_getsream(content_id, tag_ids):
    """
    Util method to add and delete the feeds on Getstream on the basis of Tag
    associated with Content .
    Args:
        content_id  : Id of content
        tag_ids : List of ids of Tags associated with Content .
    return:
        None
    """
    content_obj = Content.objects.get(id=content_id)

    # Take the existing tags
    existing_tags = content_obj.tags.all()
    existing_tags_ids = list(get_tag_ids_with_parent(existing_tags))

    modify_tags_on_getstream.delay(
        content_obj.owner_id, tag_ids, existing_tags_ids, content_obj.id)

    content_obj.tags = tag_ids
    content_obj.save()


def filter_contents(expert, content_list):
    """
    Remove ignored and published contents from content_list.

    Args:
        content_list: List of contents to filter.
    """
    content_ids = [content['id'] for content in content_list]

    ignored_content_ids = list(
        IgnoredContent.objects.filter(
            expert=expert,
            content_id__in=content_ids
        ).values_list('content_id', flat=True)
    )

    published_content_ids = list(
        Content.objects.filter(
            owner=expert.userbase,
            content_id__in=content_ids,
            is_deleted=False,
        ).values_list('content_id', flat=True)
    )

    content_ids_to_filter = ignored_content_ids + published_content_ids

    return [content for content in content_list if content['id'] not in content_ids_to_filter]


def get_tag_ids_with_parent(tags):
    tag_ids = []
    for tag in tags:
        if tag.tag_type == TagTypes.CHILD.value and tag.parent_id not in tag_ids:
            tag_ids.extend([tag.parent_id, tag.id])
        else:
            tag_ids.append(tag.id)
    return tag_ids
