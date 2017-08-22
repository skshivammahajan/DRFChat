from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from feeds.providers import build_feeds_data

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CacheFeedData(object):
    """
    class to represent the methods used for getting and caching the data in redis
    """
    def __init__(self, expert_id):
        self.expert_id = expert_id

    def feeds_key(self, timestamp):
        """
        make the key for caching
        Args:
            timestamp (int): Unix timestamp
        return:
            key which needs to be cached
        """
        return settings.FEED_CACHE_KEY_PREFIX + "_{}_{}".format(self.expert_id, timestamp)

    def cache_feeds(self, feed_data, timestamp):
        """
        This will cache the feed data in redis cache
        Args:
            feed_data (list): List of dict
            timestamp (int): Unix timestamp
        Return:
            filtered data for the given request if a valid request
        """
        cache.set(self.feeds_key(timestamp), feed_data, CACHE_TTL)
        for feed in feed_data:
            cache.set(feed['id'], feed, CACHE_TTL)

    def get_cache_feeds(self, timestamp, social_links):
        """
        Get the list of all feeds with the specified timestamp
        Args:
            timestamp (int): Unix timestamp
            social_links (obj) : Social Link
        Returns:
            all the list of feeds which are filtered
        """
        feeds_data = cache.get(self.feeds_key(timestamp))
        if feeds_data:
            return feeds_data
        feeds = build_feeds_data(social_links, timestamp)
        self.cache_feeds(feeds, timestamp)
        return feeds

    def get_feeds_by_content_id(self, content_id):
        """
        Get the exact feed with content id
        Args:
            content_id (str) : content id of the feed
        Returns:
            feed
        """
        feed = cache.get(content_id)
        if not feed:
            return
        return feed
