from datetime import timedelta
from unittest import mock
from unittest.mock import MagicMock

import pytest
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from experchat.models.domains import Tag
from experchat.models.users import Expert, ExpertProfile, User
from feeds import test_data
from feeds.cache_feeds import CacheFeedData
from feeds.models import Content, SocialAccount, SocialLink
from feeds.providers import get_provider, sort_feeds_data
from feeds.tasks import modify_tags_on_getstream
from feeds.utils import PushFeeds, PushSuperAdminFeeds, update_content_tags_at_getsream
from feeds.validators import is_valid_rss_feed_data
from streamfeeds.utils import StreamHelper


class TestRssFeedData:
    """
    Test case for valid rss feed url
    """
    def test_valid_feed_data(self):
        is_valid_rss_feed_data(test_data.VALID_RSS_FEED_DATA)
        assert True

    def test_invalid_feed_data(self):
        with pytest.raises(ValidationError):
            is_valid_rss_feed_data(test_data.INVALID_RSS_FEED_DATA)


class TestPushFeeds(TestCase):
    """
    Test case for PushFeeds
    """
    def setUp(self):
        """
        SetUp method for test case
        """
        self.distinct_tags = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3)]
        self.profiles = [MagicMock(tags=MagicMock(), id=2), MagicMock(tags=MagicMock(), id=3)]
        self.social_link = MagicMock(
            spec=SocialLink, account=MagicMock(
                spec=SocialAccount, expert=MagicMock(
                    spec=Expert, userbase=MagicMock(id=1),
                    id=1)
            ),
            expert_profiles=MagicMock(
                spec=ExpertProfile,
                all=MagicMock(return_value=self.profiles)
            )
        )
        self.push_feeds = PushFeeds(self.social_link)
        self.push_feeds.expert_profiles = self.profiles
        self.expert_profile_ids = [2]
        self.tag_ids = [1, 2, 3, 4]
        self.Tags = MagicMock(
            spec=Tag, values_list=MagicMock(return_value=self.tag_ids)
        )
        self.content = MagicMock(spec=Content, id=1,
                                 tags=MagicMock(
                                     spec=Tag,
                                     all=MagicMock(return_value=self.Tags)
                                 ))

    @mock.patch('feeds.utils.get_tag_ids_with_parent')
    @mock.patch.object(StreamHelper, 'expert_publish_content')
    def test_push_feeds_to_streamfeed(self, mock_expert_publish_content, mock_parent_tags):
        """
        test case for method push_feeds_to_streamfeed
        """
        # call the actual method
        mock_parent_tags.return_value = self.tag_ids
        self.push_feeds.push_feeds_to_streamfeed(self.content)
        mock_expert_publish_content.assert_called_once_with(
            1, self.content.id, expert_profile_ids=None, tag_ids=self.tag_ids
        )

    @mock.patch.object(Tag, 'objects')
    def test_get_tag_objs_valid(self, mock_tags):
        """
        test case for method tag_objs valid
        """
        # Assign the return Value for the mocked obj
        mock_tags.filter.return_value.distinct.return_value = self.distinct_tags
        # call the actual method
        tag_obj_list = self.push_feeds.tag_objs()
        assert tag_obj_list == self.distinct_tags
        # assert the mocked method are called with provided args
        mock_tags.filter.assert_called_once_with(expert_profiles__expert=self.social_link.account.expert)

    @mock.patch.object(Tag, 'objects')
    def test_get_tag_objs_invalid(self, mock_tags):
        """
        test case for method get_tag_objs invalid
        """
        # Assign the return Value for the mocked obj
        mock_tags.filter.return_value.distinct.return_value = self.distinct_tags
        # call the actual method
        tag_obj_list = self.push_feeds.tag_objs()
        self.assertNotEqual(tag_obj_list, self.Tags)
        # assert the mocked method are called with provided args
        mock_tags.filter.assert_called_once_with(expert_profiles__expert=self.social_link.account.expert)


class TestCacheFeedData(TestCase):
    """
    Test cases for CacheFeedData
    """
    def setUp(self):
        self.expert = MagicMock(spec=Expert, id=1)
        self.expert_id = self.expert.id
        self.timestamp = '1486731859'
        self.cache_feed = CacheFeedData(self.expert_id)

    def test_feeds_key_valid(self):
        """
        test case for feeds_key method with valid data
        :return:
        """
        assert self.cache_feed.feeds_key(self.timestamp) == \
            settings.FEED_CACHE_KEY_PREFIX + "_{}_{}".format(self.expert_id, self.timestamp)

    def test_feeds_key_invalid(self):
        """
        test case for feeds_key method with invalid data
        :return:
        """
        assert self.cache_feed.feeds_key('6736736736') != \
            settings.FEED_CACHE_KEY_PREFIX + "_{}_{}".format(self.expert_id, self.timestamp)


class TestParseFeedData(TestCase):
    """
    Test case for parse_feed_data method
    """
    def setUp(self):
        self.timestamp = '1487339528'
        self.access_token = 'jkjkd78784784'
        self.instagram_feeds = test_data.INSTAGRAM_USER_FEEDS_DATA
        self.facebook_user_data = test_data.FACEBOOK_USER_FEEDS_DATA
        self.facebook_page_data = test_data.FACEBOOK_PAGE_FEEDS_DATA
        self.youtube_user_data = test_data.YOUTUBE_USER_FEEDS_DATA
        self.youtube_channel_data = test_data.YOUTUBE_CHANEL_FEEDS_DATA
        self.rss_feed_data = test_data.RSS_FEED_RESPONSE_DATA
        self.unsorted_data = test_data.UNSORTED_FEED_LIST

        self.expected_unified_keys_valid = {
            'content_type': 1, 'description': 'Some test', 'title': 'Some test', 'timestamp': 'timestamp',
            'image': 'some url', 'social_link_id': 2, 'id': 'some id', 'content': 'some content'
        }
        self.expected_unified_keys_invalid = {
            'content_type': 1, 'description': 'Some test', 'title': 'Some test', 'timestamp': 'timestamp',
            'image': 'some url', 'social_link_id': 2, 'id': 'some id', 'content': 'some content',
            'other': None
        }
        self.social_links_facebook = MagicMock(
            spec=SocialLink, feed_type=1,
            id=3,
            account=MagicMock(
                spec=SocialAccount,
                expert=MagicMock(
                    spec=Expert,
                    id=2
                )
            )
        )
        self.social_links_instagram = MagicMock(
            spec=SocialLink,
            id=3,
            feed_type=2,
            account=MagicMock(
                spec=SocialAccount,
                expert=MagicMock(
                    spec=Expert,
                    id=2
                )
            )
        )
        self.social_links_youtube = MagicMock(
            spec=SocialLink,
            id=3,
            feed_type=3,
            account=MagicMock(
                spec=SocialAccount,
                expert=MagicMock(
                    spec=Expert,
                    id=2
                )
            )
        )
        self.social_links_rss_feed = MagicMock(
            spec=SocialLink,
            id=3,
            feed_type=4,
            account=MagicMock(
                spec=SocialAccount,
                expert=MagicMock(
                    spec=Expert,
                    id=2
                )
            )
        )

    def test_parse_feed_data_instagram_valid(self):
        """
        Test case for parse_feed_data instagram valid result
        """
        provider = get_provider(settings.INSTAGRAM_FEED_PROVIDER[0])
        result = provider.parse_feed_data(
            self.access_token,
            self.instagram_feeds, settings.SOCIAL_KEY_MAPPING.get(settings.INSTAGRAM_FEED_PROVIDER[0]),
            self.social_links_instagram, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_instagram.id)
            self.assertEqual(feed.keys(), self.expected_unified_keys_valid.keys())

    def test_parse_feed_data_instagram_invalid(self):
        """
        Test case for parse_feed_data instagram invalid result
        """
        provider = get_provider(settings.INSTAGRAM_FEED_PROVIDER[0])
        result = provider.parse_feed_data(
            self.access_token,
            self.instagram_feeds, settings.SOCIAL_KEY_MAPPING.get(settings.INSTAGRAM_FEED_PROVIDER[0]),
            self.social_links_instagram, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_instagram.id)
            self.assertNotEqual(feed.keys(), self.expected_unified_keys_invalid.keys())

    def test_parse_feed_data_facebook_valid_page_feed(self):
        """
        Test case for parse_feed_data facebook valid result for page data
        """
        provider = get_provider(settings.FACEBOOK_FEED_PROVIDER[1])
        result = provider.parse_feed_data(
            self.access_token,
            self.facebook_page_data, settings.SOCIAL_KEY_MAPPING.get(settings.FACEBOOK_FEED_PROVIDER[1]),
            self.social_links_facebook, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_facebook.id)
            self.assertEqual(feed.keys(), self.expected_unified_keys_valid.keys())

    def test_parse_feed_data_facebook_invalid_page_feed(self):
        """
        Test case for parse_feed_data facebook valid result for page data
        """
        provider = get_provider(settings.FACEBOOK_FEED_PROVIDER[1])
        result = provider.parse_feed_data(
            self.access_token,
            self.facebook_page_data, settings.SOCIAL_KEY_MAPPING.get(settings.FACEBOOK_FEED_PROVIDER[1]),
            self.social_links_facebook, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_facebook.id)
            self.assertNotEqual(feed.keys(), self.expected_unified_keys_invalid.keys())

    def test_parse_feed_data_facebook_valid_user_feed(self):
        """
        Test case for parse_feed_data facebook valid result for user data
        """
        provider = get_provider(settings.FACEBOOK_FEED_PROVIDER[1])
        result = provider.parse_feed_data(
            self.access_token,
            self.facebook_page_data, settings.SOCIAL_KEY_MAPPING.get(settings.FACEBOOK_FEED_PROVIDER[1]),
            self.social_links_facebook, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_facebook.id)
            self.assertEqual(feed.keys(), self.expected_unified_keys_valid.keys())

    def test_parse_feed_data_facebook_invalid_user_feed(self):
        """
        Test case for parse_feed_data facebook valid result for user data
        """
        provider = get_provider(settings.FACEBOOK_FEED_PROVIDER[1])
        result = provider.parse_feed_data(
            self.access_token,
            self.facebook_page_data, settings.SOCIAL_KEY_MAPPING.get(settings.FACEBOOK_FEED_PROVIDER[1]),
            self.social_links_facebook, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_facebook.id)
            self.assertNotEqual(feed.keys(), self.expected_unified_keys_invalid.keys())

    def test_parse_feed_data_youtube_valid_user_feed(self):
        """
        Test case for parse_feed_data youtube valid result for user data
        """
        provider = get_provider(settings.YOUTUBE_FEED_PROVIDER[0])
        result = provider.parse_feed_data(
            self.access_token,
            self.youtube_user_data, settings.SOCIAL_KEY_MAPPING.get(settings.YOUTUBE_FEED_PROVIDER[0]),
            self.social_links_youtube, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_youtube.id)
            self.assertEqual(feed.keys(), self.expected_unified_keys_valid.keys())

    def test_parse_feed_data_youtube_invalid_user_feed(self):
        """
        Test case for parse_feed_data youtube valid result for user data
        """
        provider = get_provider(settings.YOUTUBE_FEED_PROVIDER[0])
        result = provider.parse_feed_data(
            self.access_token,
            self.youtube_user_data, settings.SOCIAL_KEY_MAPPING.get(settings.YOUTUBE_FEED_PROVIDER[0]),
            self.social_links_youtube, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_youtube.id)
            self.assertNotEqual(feed.keys(), self.expected_unified_keys_invalid.keys())

    def test_parse_feed_data_youtube_valid_channel_feed(self):
        """
        Test case for parse_feed_data youtube valid result for channel data
        """
        provider = get_provider(settings.YOUTUBE_FEED_PROVIDER[0])
        result = provider.parse_feed_data(
            self.access_token,
            self.youtube_channel_data, settings.SOCIAL_KEY_MAPPING.get(settings.YOUTUBE_FEED_PROVIDER[0]),
            self.social_links_youtube, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_youtube.id)
            self.assertEqual(feed.keys(), self.expected_unified_keys_valid.keys())

    def test_parse_feed_data_youtube_invalid_channel_feed(self):
        """
        Test case for parse_feed_data youtube valid result for channel data
        """
        provider = get_provider(settings.YOUTUBE_FEED_PROVIDER[0])
        result = provider.parse_feed_data(
            self.access_token,
            self.youtube_channel_data, settings.SOCIAL_KEY_MAPPING.get(settings.YOUTUBE_FEED_PROVIDER[0]),
            self.social_links_youtube, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_youtube.id)
            self.assertNotEqual(feed.keys(), self.expected_unified_keys_invalid.keys())

    def test_parse_feed_data_rss_valid_feed(self):
        """
        Test case for parse_feed_data rss valid result
        """
        provider = get_provider('RSS')
        result = provider.parse_feed_data(
            self.access_token,
            self.rss_feed_data, settings.SOCIAL_KEY_MAPPING.get('RSS'),
            self.social_links_rss_feed, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_rss_feed.id)
            self.assertEqual(feed.keys(), self.expected_unified_keys_valid.keys())

    def test_parse_feed_data_rss_invalid_feed(self):
        """
        Test case for parse_feed_data rss valid result
        """
        provider = get_provider('RSS')
        result = provider.parse_feed_data(
            self.access_token,
            self.rss_feed_data, settings.SOCIAL_KEY_MAPPING.get('RSS'),
            self.social_links_rss_feed, self.timestamp
        )
        for feed in result:
            self.assertEqual(feed['social_link_id'], self.social_links_rss_feed.id)
            self.assertNotEqual(feed.keys(), self.expected_unified_keys_invalid.keys())

    def test_sort_feeds_data_valid(self):
        """
        Test case for sort_feeds_data
        """
        expected_result = [self.unsorted_data[2],
                           self.unsorted_data[0],
                           self.unsorted_data[1]]
        result = sort_feeds_data(self.unsorted_data, self.timestamp)
        self.assertEqual(result, expected_result)

    def test_sort_feeds_data_invalid(self):
        """
        Test case for sort_feeds_data
        """
        expected_result = [{
            'timestamp': timezone.now() - timedelta(days=14),
            'title': 'First title'
        }, {
            'timestamp': timezone.now() - timedelta(days=6),
            'title': 'Alan Walker - Alone'
        }, {
            'timestamp': timezone.now() - timedelta(days=2),
            'title': 'Second title - Alone'
        }]
        result = sort_feeds_data(self.unsorted_data, self.timestamp)
        self.assertNotEqual(result, expected_result)


class TestCeleryTaskGetstream(TestCase):
    """
    Test case for Celery Task for adding and removing feeds from Getstream .
    """

    def setUp(self):
        self.user = MagicMock(spec=User, id=1)
        self.new_tag_ids = [1, 2, 3, 4]
        self.existing_tags_ids = [2, 4, 6, 8]
        self.content = MagicMock(spec=Content, id=1)

    @mock.patch.object(StreamHelper, 'expert_publish_content')
    @mock.patch.object(StreamHelper, 'remove_content_tag_feeds')
    def test_getstream(self, mock_expert_publish_content, mock_remove_content_tag_feeds):
        mock_expert_publish_content.return_value = {
            'actor': '1',
            'id': '03955b90-fa5c-11e6-8080-80001ece3378',
            'foreign_id': '4',
            'to': [
                ['tag:1', 'Bi2QpCWTBvuT-m9b1YWpL4SvS_g'],
                ['tag:4', 'CuhfVuvDMsXoOKWERqne-oA3GWQ']
            ],
            'origin': None,
            'time': timezone.now(),
            'duration': '53ms',
            'object': '4',
            'target': None,
            'verb': 'post'
        }
        mock_remove_content_tag_feeds.return_value = None
        result = modify_tags_on_getstream(user_id=self.user.id, new_tag_ids=self.new_tag_ids,
                                          existing_tags_ids=self.existing_tags_ids,
                                          content_id=self.content.id)
        assert result is None


class TestPushSuperAdminFeeds(TestCase):
    """
    Test case for PushFeeds
    """
    def setUp(self):
        """
        SetUp method for test case
        """
        self.expert = MagicMock(
            spec=Expert, userbase=MagicMock(id=1)
        )
        # since super admin will be not having any profiles, that why setting it to empty list
        self.expert.profiles.all.return_value = []
        self.content = MagicMock(spec=Content, id=1)
        self.push_admin_feeds = PushSuperAdminFeeds(self.expert.userbase)
        self.expert_profile_ids = [2]
        self.tag_ids = [1, 2, 3, 4]

    @mock.patch.object(StreamHelper, 'expert_publish_content')
    def test_push_super_admin_feeds(self, mock_expert_publish_content):
        """
        test case for testing the mocked method is getting called with exact arguments
        """
        result = self.push_admin_feeds.push_super_admin_feeds(self.content, self.tag_ids, super_admin=True)
        assert result
        mock_expert_publish_content.assert_called_once_with(
            self.expert.userbase.id, self.content.id, self.expert.profiles.all.return_value, self.tag_ids,
            True
        )


class TestStreamFeedsUtils(TestCase):
    """
    Test case for PushFeeds
    """
    def setUp(self):
        """
        SetUp method for test case
        """
        self.existing_tags_ids = [1, 2, 3, 4]
        self.content_id = 1
        self.tag_ids = [1, 5, 7]
        # setting up the value for content_obj.tags.all().values_list('id', flat=True)
        self.content = MagicMock(
            spec=Content, id=self.content_id, owner_id=21,
            tags=(MagicMock(
                spec=Tag, all=MagicMock(
                    return_value=MagicMock(
                        values_list=MagicMock(
                            return_value=self.existing_tags_ids)
                    )))))

    @mock.patch('feeds.utils.get_tag_ids_with_parent')
    @mock.patch('feeds.utils.modify_tags_on_getstream.delay')
    @mock.patch.object(Content, 'objects')
    def test_update_content_tags_at_getsream(self, mock_objects, mock_delay, mock_parent_ids):
        """
        test case for testing the update_content_tags_at_getsream
        """
        mock_objects.get.return_value = self.content
        mock_parent_ids.return_value = self.existing_tags_ids
        result = update_content_tags_at_getsream(self.content_id, self.tag_ids)
        assert result is None
        assert self.content.tags == self.tag_ids
        mock_delay.assert_called_once_with(self.content.owner_id, self.tag_ids, self.existing_tags_ids, self.content.id)
