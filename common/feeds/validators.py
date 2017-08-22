import feedparser
import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout
from rest_framework import status
from rest_framework.exceptions import ValidationError

from feeds.utils import validate_feed_list_data


def is_valid_rss_feed_data(data):
    """
    This will validate the provided data is a valid rss feed data or not
    Args:
        data (byte): data which is returned after calling the given uri with requests
    Return:
        parse_data (dict): valid rss feed data with key value pair
    Raise:
        ValidationError
    """
    parse_data = feedparser.parse(data)
    if not parse_data['items'] or not validate_feed_list_data(parse_data['items']):
        raise ValidationError('ERROR_RSS_FEED_INVALID')
    return parse_data


def is_valid_feed_url(url):
    """
    This will validate the provided url is a valid rss feed url or not
    Args:
        url (str): url like https://staff.tumblr.com/rss
    Return:
        parse_data (dict): All rss feed data dict
    Raise:
        ValidationError if url is not a valid rss feed url
    """
    try:
        response = requests.get(url, timeout=10)
    except (ConnectionError, HTTPError, Timeout):
        raise ValidationError('ERROR_RSS_FEED_INVALID')
    if response.status_code != status.HTTP_200_OK:
        raise ValidationError('ERROR_RSS_FEED_INVALID')

    return is_valid_rss_feed_data(response.content)
