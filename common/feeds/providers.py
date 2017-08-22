import json
from collections import OrderedDict
from urllib.parse import quote

import requests
from django.conf import settings
from django.utils import dateparse, timezone
from requests.exceptions import ConnectionError, HTTPError, Timeout
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.settings import api_settings

from feeds.choices import FeedProviders
from feeds.utils import validate_access_token, validate_feed_data
from feeds.validators import is_valid_feed_url


class ProviderError(APIException):
    status_code = 400
    default_detail = {api_settings.NON_FIELD_ERRORS_KEY: ["ERROR_SOCIAL_LOGIN"]}
    default_code = 'invalid'


class BaseFeedProvider(object):
    """
    Base class for provider
    """
    def __init__(self, provider):
        self.provider = provider

    def build_provider_uri(self):
        raise NotImplementedError('.build_provider_uri() must be implemented')

    def get_access_token_response_data(self, app_code):
        raise NotImplementedError('.get_access_token_response_data() must be implemented')

    def get_pages(self, token):
        raise NotImplementedError('.get_pages() must be implemented')

    def get_uniquie_feed_id(self, key_id, feed_id, social_link):
        return key_id + "{}_".format(social_link.id) + feed_id + "_{}".format(social_link.account.expert.id)

    def get_valid_access_token(self, social_link):
        raise NotImplementedError('.get_valid_access_token() is not implemented')

    def process_response_data(self, response):
        """
        method to process the response data
        Args:
            response (object): Http Respnse
        return:
            processed data
        """
        access_data = json.loads(response.content.decode('utf-8'))
        if response.status_code != status.HTTP_200_OK:
            raise ProviderError
        return access_data

    def process_feeds_response_data(self, response, social_link):
        """
        method to process the response data
        Args:
            response (obj): Http Respnse
            social_link (obj): SocialLink
        return:
            processed data
        """
        access_data = json.loads(response.content.decode('utf-8'))
        if response.status_code != status.HTTP_200_OK:
            self.remove_or_log_error(access_data, social_link)
            access_data = None
        return access_data


class FaceBookProvider(BaseFeedProvider):
    """
    Provider class for facebook
    """
    def __init__(self, provider):
        self.provider = provider
        self.page_type = 'page'
        self.version = "v2.8"
        self.api_url = "https://www.facebook.com/"
        self.token_expiration_error = ['GraphMethodException', 'OAuthException']
        self.login_url = self.api_url + "{}/dialog/oauth?scope=user_posts,manage_pages&client_id={}&redirect_uri={}"
        self.graph_api_url = "https://graph.facebook.com/"
        self.token_api = self.graph_api_url + \
            "{}/oauth/access_token?client_id={}&redirect_uri={}&client_secret={}&code={}"
        self.user_api_url = self.graph_api_url + "{}/me/?access_token={}&fields=id,name,picture"
        self.feed_api_url = self.graph_api_url + \
            "{}/{}/feed/?access_token={}&until={}&fields=" \
            "id,description,created_time,message,picture,updated_time,attachments,story,properties,link,object_id," \
            "comments.summary(true).limit(1),likes.summary(true).limit(1)"
        self.all_page_api_url = self.graph_api_url + "{}/me/accounts/?access_token={}"
        self.page_detail_api_url = self.graph_api_url + "{}/{}?access_token={}"
        self.long_lived_token_api_url = self.graph_api_url + \
            "{}/oauth/access_token?client_id={}&client_secret={}&grant_type=fb_exchange_token&fb_exchange_token={}"

    @property
    def build_provider_uri(self):
        """
        build the uri for the provider
        return:
            url
        """
        return self.login_url.format(
            self.version, settings.FACEBOOK_APP_ID,
            quote(settings.FACEBOOK_REDIRECT_URL, safe='')
        )

    def get_access_token_response_data(self, app_code):
        """
        function to get and return the access_token api response
        Args:
            app_code (str): app_code for the registered app
        Raises:
            ProviderError
        """
        url = self.token_api.format(
            self.version, settings.FACEBOOK_APP_ID,
            quote(settings.FACEBOOK_REDIRECT_URL, safe=''), settings.FACEBOOK_APP_SECRET,
            app_code
        )
        try:
            response = requests.get(url)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError

        return self.process_response_data(response)

    def get_long_lived_access_token_data(self, access_token):
        """
        function to get and return the longed_lived_access api response
        Args:
            access_token (str): access_token for the registered app
        Raises:
            ProviderError
        """
        url = self.long_lived_token_api_url.format(
            self.version, settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_APP_SECRET,
            access_token
        )
        try:
            response = requests.get(url)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_response_data(response)

    def get_user_info_data(self, token):
        """
        function to get and return the user information like id, name and picture
        Args:
            token (str): access_token which is used to exchange the information
        Raises:
            ProviderError
        """
        get_user_api_url = self.user_api_url.format(
            self.version, token
        )
        try:
            response = requests.get(get_user_api_url)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_response_data(response)

    def get_pages(self, token, page_id=None):
        """
        method to implements the get page information for the user
        Args:
            token (str): Access_token
            page_id (str): id of the page
        Raises:
            ProviderError
        """
        if not page_id:
            get_page_info_api_url = self.all_page_api_url.format(
                self.version, token
            )
        else:
            get_page_info_api_url = self.page_detail_api_url.format(
                self.version, page_id, token
            )
        try:
            response = requests.get(get_page_info_api_url)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_response_data(response)

    def process_page_data(self, pages_data):
        """
        Process the page data
        Args:
            pages_data (list): list of page data
        return:
            page_data
        """
        page_data = []
        for page in pages_data['data']:
            page_data.append({'id': page['id'], 'type': self.page_type, 'name': page['name']})
        return page_data

    def process_user_data(self, user_data):
        """
        Format the user data as per need
        Args:
            user_data (dict): user data
        return:
            formatted user data
        """
        return {'id': user_data['id'], 'type': 'user', 'name': user_data['name']}

    def get_feeds_response_data(self, token, social_link, timestamp):
        """
        function to get and return the access_token api response
        Args:
            token (str): access_token which is used to exchange the information
            social_link (obj): SocialLink
            timestamp (time): In Unix format
        Raises:
            ProviderError
        """
        feeds_url = self.feed_api_url.format(
            self.version, social_link.detail, token, timestamp
        )
        try:
            response = requests.get(feeds_url)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_feeds_response_data(response, social_link)

    def remove_or_log_error(self, access_data, social_link):
        """
        This method is used to log the error or remove the link form DB
        Args:
            access_data (dict): response dict
            social_link (obj): Social link
        return:
            None
        """
        if access_data.get('error', {}).get('type') in self.token_expiration_error:
            # TODO LOG THE ERROR
            social_link.delete()
        else:
            # TODO log the error once implementing the logging
            pass

    def parse_feed_data(self, access_token, feeds, key_id, social_link, timestamp):
        """
        Parse the Facebook response data and make dict which needs to be saved
        Args:
            access_token (str): token
            feeds (dict) : feed data
            key_id (str) : prefix unique if like fb_
            social_link (obj): Social link
            timestamp (time): time in unix timestamp
        return:
            formatted dict
        """
        facebook_unify_feeds = []
        for feed in feeds['data']:
            facebook_unify_feeds.append({
                'id': self.get_uniquie_feed_id(key_id, feed['id'], social_link),
                'title': None,
                'content_type': social_link.feed_type,
                'social_link_id': social_link.id,
                'image': feed.get('picture'),
                'description': feed.get('message', feed.get('story')),
                'timestamp': dateparse.parse_datetime(feed['created_time']),
                'content': feed
            })
        return facebook_unify_feeds

    def get_valid_access_token(self, social_link):
        """
        Validate the access_token
        Args:
            social_link (obj): Social Link obj
        return:
            access_token without any processing
        """
        return social_link.account.access_token


class InstaGramProvider(BaseFeedProvider):
    """
    Provider class for Instagram
    """
    def __init__(self, provider):
        self.provider = provider
        self.token_expiration_error = 'OAuthAccessTokenException'
        self.version = "v1"
        self.api_url = "https://api.instagram.com/"
        self.user_info_uri = self.api_url + '{}/users/self/?access_token={}'
        self.auth_url = self.api_url + "oauth/authorize/?client_id={}&redirect_uri={}&response_type=code"
        self.token_api_url = self.api_url + "oauth/access_token"
        self.user_api_url = self.api_url + "{}/users/self/?access_token={}"
        self.media_api_url = self.api_url + "{}/users/{}/media/recent/?access_token={}&COUNT=200"

    @property
    def build_provider_uri(self):
        """
        build the uri for the provider
        return:
            url
        """
        return self.auth_url.format(
            settings.INSTAGRAM_CLIENT_ID,
            quote(settings.INSTAGRAM_REDIRECT_URL, safe=''),
            access_type='offline'
        )

    def get_access_token_response_data(self, app_code):
        """
        function to get and return the access_token api response
        Args:
            app_code (str): app_code for the registered app
        Raises:
            ProviderError
        """
        payload = {
            'client_id': settings.INSTAGRAM_CLIENT_ID,
            'client_secret': settings.INSTAGRAM_SECRET_CODE,
            'redirect_uri': settings.INSTAGRAM_REDIRECT_URL,
            'grant_type': 'authorization_code',
            'code': app_code
        }
        try:
            response = requests.post(url=self.token_api_url, data=payload)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_response_data(response)

    def get_user_info_data(self, token):
        """
        :param token:
        :return:
        """
        url = self.user_info_uri.format(self.version, token)
        try:
            response = requests.get(url)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_response_data(response)

    def process_user_data(self, user_data):
        """
        Format the user data as per need
        :param user_data:
        :return:
        """
        return {'id': user_data.get('data', {}).get('id'), 'type': 'user',
                'name': user_data.get('data', {}).get('username')}

    def get_feeds_response_data(self, token, social_link, timestamp):
        """
        function to get and return the access_token api response
        Args:
            token (str): access_token which is used to exchange the information
            social_link (obj): SocialLink
            timestamp (time): In Unix format
        Raises:
            ProviderError
        """
        get_user_feeds_url = self.media_api_url.format(
            self.version, social_link.detail, token
        )
        try:
            response = requests.get(get_user_feeds_url)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_feeds_response_data(response, social_link)

    def remove_or_log_error(self, access_data, social_link):
        """
        This method is used to log the error or remove the link form DB
        Args:
            access_data (dict): response dict
            social_link (obj): Social link
        return:
            None
        """
        if access_data.get('meta', {}).get('error_type') == self.token_expiration_error:
            # TODO log the error
            social_link.delete()
        else:
            # TODO log the error
            pass

    def parse_feed_data(self, access_token, feeds, key_id, social_link, timestamp):
        """
        Parse the Facebook response data and make dict which needs to be saved
        Args:
            access_token (str): token
            feeds (dict) : feed data
            key_id (str) : prefix unique if like in_
            social_link (obj): Social link
            timestamp (time): In Unix format
        return:
            formatted dict
        """
        instagram_unify_feeds = []
        for feed in feeds['data']:
            if timestamp >= feed['created_time']:
                if feed.get('type') == 'image':
                    url = feed.get('images', {}).get('standard_resolution', {}).get('url')
                else:
                    url = feed.get('videos', {}).get('standard_resolution', {}).get('url')
                title = feed.get('caption', {}).get('text') if feed.get('caption') else feed.get('caption')
                instagram_unify_feeds.append({
                    'id': self.get_uniquie_feed_id(key_id, feed['id'], social_link),
                    'title': title,
                    'content_type': social_link.feed_type,
                    'social_link_id': social_link.id,
                    'image': url,
                    'description': title,
                    'timestamp': timezone.datetime.fromtimestamp(float(feed['created_time']), dateparse.utc),
                    'content': feed
                })
        return instagram_unify_feeds

    def get_valid_access_token(self, social_link):
        """
        Validate the access_token
        Args:
            social_link (obj): Social Link obj
        return:
            access_token without any processing
        """
        return social_link.account.access_token


class YoutubeProvider(BaseFeedProvider):
    """
    Provider for Youtube
    """
    def __init__(self, provider):
        self.provider = provider
        self.page_type = 'channel'
        self.version = "v3"
        self.token_expiration_error = 'Invalid Credentials'
        self.default_expire_time = 3600
        self.api_user_info = "https://www.googleapis.com/oauth2/{}/userinfo?access_token={}"
        self.api_scope_url = "https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/userinfo.profile"
        self.auth_server_api_url = "https://accounts.google.com/o/oauth2/auth"
        self.token_api_url = "https://accounts.google.com/o/oauth2/token"
        self.server_api_url = self.auth_server_api_url + \
            "?client_id={}&redirect_uri={}&scope={}&response_type=code&access_type=offline"
        self.search_list_url = 'https://www.googleapis.com/youtube/'
        self.video_api_url = self.search_list_url + \
            "{}/search/?publishedBefore={}&part=snippet&access_token={}&key={}&channelId={}&type=video&maxResults=50"
        self.user_feed_api_url = self.search_list_url + \
            "{}/search/?publishedBefore={}&part=snippet&miken={}&access_token={}&key={}&type=video&maxResults=50"
        self.channel_api_url = self.search_list_url + "{}/channels?access_token={}&part=snippet&mine=true"
        self.videos_statistics_api_url = "https://www.googleapis.com/youtube/v3/videos/?" \
                                         "part=statistics&id={}&access_token={}"

    @property
    def build_provider_uri(self):
        """
        build the uri for the provider
        return:
             url
        """
        return self.server_api_url.format(
            settings.GOOGLE_APP_CLIENT_ID,
            quote(settings.YOUTUBE_REDIRECT_URL, safe=''),
            quote(self.api_scope_url, safe='')
        )

    def make_access_token_expiry_timestamp(self, expire_in):
        """
        method to make the timestamp for expiry of access_token
        Args:
            expire_in (time): in second returned from API
        return:
            timestamp for expiry of token
        """
        return timezone.now() + timezone.timedelta(seconds=expire_in) - timezone.timedelta(seconds=60)

    def get_refresh_token_response(self, refresh_token):
        """
        function to get and return the access_token api response
        Args:
            refresh_token (str): refresh_token of the registered app
        Raises:
            ProviderError
        """
        payload = {
            'client_id': settings.GOOGLE_APP_CLIENT_ID,
            'client_secret': settings.GOOGLE_SECRET_KEY,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }
        try:
            response = requests.post(url=self.token_api_url, data=payload)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        response_data = json.loads(response.content.decode('utf-8'))
        if response.status_code != status.HTTP_200_OK:
            return []
        return response_data

    def get_access_token_response_data(self, app_code):
        """
        function to get and return the access_token api response
        Args:
            app_code (str): app_code for the registered app
        Raises:
            ProviderError
        """
        payload = {
            'client_id': settings.GOOGLE_APP_CLIENT_ID,
            'client_secret': settings.GOOGLE_SECRET_KEY,
            'redirect_uri': settings.YOUTUBE_REDIRECT_URL,
            'grant_type': 'authorization_code',
            'code': app_code
        }
        try:
            response = requests.post(url=self.token_api_url, data=payload)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_response_data(response)

    def get_user_info_data(self, token):
        """
        :param token:
        :return:
        """
        url = self.api_user_info.format(self.version, token)
        try:
            response = requests.get(url)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_response_data(response)

    def process_user_data(self, user_data):
        """
        Format the user data as per need
        :param user_data:
        :return:
        """
        return {'id': user_data['sub'], 'type': 'user', 'name': user_data['name']}

    def process_page_data(self, page_data):
        channel_data = []
        for channel in page_data['items']:
            channel_data.append({'id': channel['id'], 'type': self.page_type,
                                 'name': channel.get('snippet', {}).get('title')})
        return channel_data

    def get_pages(self, token, page_id=None):
        """
        method to implements the get channel information for the user
        Args:
            token (str): Access_token
            page_id (str): id of the page
        Raises:
            ProviderError
        """
        if not page_id:
            get_page_info = self.channel_api_url.format(
                self.version, token
            )
        else:
            get_page_info = self.page_detail_api_url.format(
                self.version, page_id, token
            )
        try:
            response = requests.get(get_page_info)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_response_data(response)

    def get_feeds_response_data(self, token, social_link, timestamp):
        """
        function to get and return the access_token api response
        Args:
            token (str): access_token which is used to exchange the information
            social_link (obj): SocialLink
            timestamp (time): In Unix format
        Raises:
            ProviderError
        """
        formated_timestamp = timezone.datetime.fromtimestamp(float(timestamp), dateparse.utc)
        formated_timestamp = serializers.DateTimeField().to_representation(formated_timestamp)
        if int(social_link.feed_sub_type) == settings.USER_FEED_TYPE:
            youtube_serach_list_url = self.user_feed_api_url.format(
                self.version, formated_timestamp, settings.YOUTUBE_SEARCH_LIST_API_MINE_FLAG,
                token, settings.GOOGLE_APP_API_KEY, social_link.detail
            )
        else:
            youtube_serach_list_url = self.video_api_url.format(
                self.version, formated_timestamp,
                token, settings.GOOGLE_APP_API_KEY, social_link.detail
            )
        try:
            response = requests.get(youtube_serach_list_url)
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        return self.process_feeds_response_data(response, social_link)

    def remove_or_log_error(self, access_data, social_link):
        """
        This method is used to log the error or remove the link form DB
        Args:
            access_data (dict): response dict
            social_link (obj): Social link
        return:
            None
        """
        if access_data.get('error', {}).get('message') == self.token_expiration_error:
            # TODO log the error
            social_link.delete()
        else:
            # TODO log the error
            pass

    def get_statistics_data(self, access_token, feed_ids, feeds):
        """
        Get the likes and comment statistics
        Args:
            access_token (str): token
            feed_ids (list): list if feed ids
            feeds (list): list of feeds
        returns:
            feeds (list): updated list with key as statistics in the content
        """
        # call the Videos API to get the likes and comments
        try:
            stats_response = requests.get(self.videos_statistics_api_url.format(','.join(feed_ids), access_token))
        except (ConnectionError, HTTPError, Timeout):
            raise ProviderError
        if stats_response.status_code != status.HTTP_200_OK:
            # TODO log the error message
            return feeds
        statistics = OrderedDict()
        response_data = json.loads(stats_response.content.decode('utf-8'))
        for item in response_data['items']:
            statistics.update({
                item['id']: item['statistics']
            })
        for feed in feeds:
            feed['content'].update({'statistics': statistics.get(feed['content']['id'].get('videoId'))})
        return feeds

    def parse_feed_data(self, access_token, feeds, key_id, social_link, timestamp):
        """
        Parse the Facebook response data and make dict which needs to be saved
        Args:
            access_token (str): token
            feeds (dict) : feed data
            key_id (str) : prefix unique if like yt_
            timestamp (time): time in unix timestamp
            social_link (obj) : Social link object
        return:
            formatted dict
        """
        youtube_unify_feeds = []
        feed_ids = []
        for feed in feeds['items']:
            feed_id = feed['id'].get('videoId')
            timestamp = dateparse.parse_datetime(feed['snippet']['publishedAt'])
            description = feed.get('snippet', {}).get('description')
            title = feed.get('snippet', {}).get('title')
            image = feed.get('snippet', {}).get('thumbnails', {}).get('high', {}).get('url')
            if feed_id:
                feed_ids.append(feed_id)
                youtube_unify_feeds.append({
                    'id': self.get_uniquie_feed_id(key_id, feed_id, social_link),
                    'title': title,
                    'content_type': social_link.feed_type,
                    'social_link_id': social_link.id,
                    'image': image,
                    'description': description,
                    'timestamp': timestamp,
                    'content': feed
                })

        return self.get_statistics_data(access_token, feed_ids, youtube_unify_feeds)

    def get_valid_access_token(self, social_link):
        """
        Validate the access_token
        Args:
            social_link (obj): Social Link obj
        return:
            Updated access_token if refresh token is returned from Youtube else none
        """
        # check if access_token is expired
        access_token = social_link.account.access_token
        if social_link.account.refresh_token:
            is_valid_access_token = validate_access_token(social_link.account.access_token_expiry_timestamp,
                                                          self.default_expire_time)
            if not is_valid_access_token:
                token_response = self.get_refresh_token_response(social_link.account.refresh_token)
                if token_response:
                    access_token = token_response['access_token']
                else:
                    access_token = None
        return access_token


class RssFeedProvider(BaseFeedProvider):
    """
    Rss feed app provider
    """
    def __init__(self, provider):
        self.provider = provider

    def get_feeds_response_data(self, token, social_link, timestamp):
        """
        function to get and return the access_token api response
        Args:
            token (str): access_token which is used to exchange the information
            social_link (obj): SocialLink
            timestamp (time): In Unix format
        Raises:
            ProviderError
        """
        return is_valid_feed_url(token)

    def parse_feed_data(self, access_token, feeds, key_id, social_link, timestamp):
        """
        Parse the Facebook response data and make dict which needs to be saved
        Args:
            access_token (str): token
            feeds (dict) : feed data
            key_id (str) : prefix unique if like fb_
            social_link (object): SocialLink
            timestamp (int): Unix timestamp
        return:
            formatted dict
        """
        rss_unify_feeds = []
        for feed in feeds['items']:
            if not validate_feed_data(feed):
                continue
            updated_at = feed.get('updated_parsed') or feed.get('created_parsed') or feed.get('published_parsed')
            updated_at = timezone.make_aware(
                timezone.datetime(*updated_at[:-3]),
                dateparse.utc
            )
            image_url = feed.get('media_thumbnail')[0].get('url', '') if feed.get('media_thumbnail') else ''
            if timezone.datetime.fromtimestamp(float(timestamp), dateparse.utc) >= updated_at:
                rss_unify_feeds.append({
                    'id': self.get_uniquie_feed_id(key_id, feed['id'], social_link),
                    'title': feed['title'],
                    'content_type': social_link.feed_type,
                    'social_link_id': social_link.id,
                    'image': image_url,
                    'description': feed.get('summary'),
                    'timestamp': updated_at,
                    'content': feed
                })
        return rss_unify_feeds

    def get_valid_access_token(self, social_link):
        """
        Validate the access_token
        Args:
            social_link (obj): Social Link obj
        return:
            access_token without any processing
        """
        return social_link.account.access_token


def get_provider(provider):
    """
    function to return the specific provider
    Args:
        provider (str): provider like facebook, youtube etc
    return:
        specific provider class
    """
    if provider.upper() in settings.FACEBOOK_FEED_PROVIDER:
        return FaceBookProvider(provider)
    elif provider.upper() in settings.INSTAGRAM_FEED_PROVIDER:
        return InstaGramProvider(provider)
    elif provider.upper() in settings.YOUTUBE_FEED_PROVIDER:
        return YoutubeProvider(provider)
    else:
        return RssFeedProvider(provider)


def sort_feeds_data(feeds, timestamp):
    """
    Sort the feeds data
    :param feeds:
    :param timestamp:
    :return:
    """
    return sorted(feeds, key=lambda k: k['timestamp'], reverse=True)


def build_feeds_data(social_links, timestamp):
    """
    Build the feeds_data by calling the APIS
    Args:
        social_links (obj): Social Link Object
        timestamp (time): time in unix timestamp
    return:
        all_feeds (list): merged list of feed dict
    """
    providers = {provider.value: provider.name for provider in FeedProviders}
    all_feeds = []
    for social_link in social_links:
        provider = providers.get(int(social_link.feed_type))
        if not provider:
            continue
        provider_object = get_provider(provider)
        access_token = provider_object.get_valid_access_token(social_link)
        if not access_token:
            continue
        try:
            access_data = provider_object.get_feeds_response_data(
                access_token, social_link, timestamp
            )
        except (HTTPError, Timeout, ConnectionError, ValidationError):
            continue
        if not access_data:
            continue

        all_feeds.extend(provider_object.parse_feed_data(access_token, access_data,
                                                         settings.SOCIAL_KEY_MAPPING.get(provider),
                                                         social_link, timestamp))

    return sort_feeds_data(all_feeds, timestamp)
