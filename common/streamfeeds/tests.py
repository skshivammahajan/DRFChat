from django.conf import settings
from django.test import TestCase

from streamfeeds.utils import StreamHelper


class TestFeed(TestCase):
    """
    Test Feed for Getstream.
    """
    valid_data = [1, 2, 3]

    def setUp(self):
        self.stream_helper = StreamHelper()
        self.super_admin = 1

    def test_valid_expert_profiles_feed(self):
        result = self.stream_helper.get_expert_profiles(self.valid_data)
        assert result == ['expertprofile:1', 'expertprofile:2', 'expertprofile:3']

    def test_valid_tags_feed(self):
        result = self.stream_helper.get_tags(self.valid_data)
        assert result == ['tag:1', 'tag:2', 'tag:3']

    def test_get_super_admin_feed(self):
        result = self.stream_helper.get_super_admin(self.super_admin)
        assert result == [settings.STREAM_FEEDS_USER + ':{}'.format(settings.STREAM_STATIC_SUPERADMIN_FEED)]

    def test_get_super_admin_feed_withod_id(self):
        result = self.stream_helper.get_super_admin(False)
        assert result == []

    def test_get_user_global_feed(self):
        result = self.stream_helper.get_user_global()
        assert result == [settings.STREAM_FEEDS_USER + ':{}'.format(settings.STREAM_STATIC_GLOBAL_FEED)]
