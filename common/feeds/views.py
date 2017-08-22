import logging

from django.conf import settings
from django.http import Http404
from django.utils import dateparse, timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

from experchat.permissions import IsExpertPermission, IsSuperUser, IsUserPermission
from experchat.serializers import EmptySerializer
from experchat.views import ExperChatAPIView
from feeds.cache_feeds import CacheFeedData
from feeds.choices import FeedProviders
from feeds.models import Content, ContentUserActivity, IgnoredContent, SocialAccount, SocialLink
from feeds.pagination import paginate_content_results
from feeds.permissions import IsFeedOwnerOrReadOnly
from feeds.providers import get_provider
from feeds.serializers import (
    ContentSerializer, IgnoredContentSerializers, RSSLinkSerializer, SocialAuthAppCodeSerializer,
    SocialLinkPostSerializer, SocialLinkSerializer, SuperAdminContentSerializer
)
from feeds.tasks import like_or_unlike_content
from feeds.utils import filter_contents
from streamfeeds.utils import StreamHelper

logger = logging.getLogger(__name__)


class SocialUrlApiView(APIView):
    """
    Social Api view for social app login URLs
    """
    permission_classes = (IsExpertPermission,)

    def get(self, request, provider=None, format=None):
        """
        get API to make the URLs to specific providers
        Args:
            request (obj): Requests
            provider (str): Facebook, instagram or youtube
            format (str): Format type
        Return:
            Response with status code and message
        """
        if not provider or provider.upper() not in settings.ALL_FEED_PROVIDERS:
            raise Http404
        return Response(status=status.HTTP_200_OK, data={'url': get_provider(provider).build_provider_uri})


class SocialUrlGetTokenView(APIView):
    """
    Api view for social to get the access token and save the access_token in database
    """
    permission_classes = (IsExpertPermission,)

    def get(self, request, app_code=None, provider=None, format=None):
        """
        GET api to get the access token form the provider
        Args:
            request (obj): requets
            app_code (str): app_code of provider
            provider (str): provider like facebook, youtube etc
            format (str): restframework format
        Return:
            Response (obj): Response with status code and message
        Raise:
            request exceptions like ConnectionError, HttpEror etc
        """
        if not provider or provider.upper() not in settings.ALL_FEED_PROVIDERS:
            raise Http404
        response_data = []
        provider_instance = get_provider(provider)
        data = {'app_code': app_code, 'provider': provider}
        serializer = SocialAuthAppCodeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # get the access_data
        access_data = provider_instance.get_access_token_response_data(
            app_code)
        # get the User Info
        user_info = provider_instance.get_user_info_data(
            access_data['access_token'])
        user_id = user_info.get('id', user_info.get(
            'sub', user_info.get('data', {}).get('id')))
        # here try to get longed lived access_token in case of Facebook
        if getattr(provider_instance, 'get_long_lived_access_token_data', None):
            access_data = provider_instance.get_long_lived_access_token_data(access_data[
                                                                             'access_token'])
        # here updating the validated data becasue we need to save the
        # access_token for the user
        try:
            access_token_instance = SocialAccount.objects.get(expert=request.user.expert,
                                                              provider=getattr(
                                                                  FeedProviders, provider.upper()).value,
                                                              user_id=user_id)
            access_token_instance.access_token = access_data.get(
                'access_token')
            # here need to call the util method where we will formating actual
            # expiry date
            if access_data.get('expire_in'):
                access_token_instance.access_token_expiry_timestamp = \
                    provider_instance.make_access_token_expiry_timestamp(access_data[
                                                                         'expire_in'])
            access_token_instance.name = user_info.get(
                'name', user_info.get('data', {}).get('username'))
            access_token_instance.user_id = \
                user_info.get('id', user_info.get(
                    'sub', user_info.get('data', {}).get('id')))
            access_token_instance.save()
        except SocialAccount.DoesNotExist:
            serializer.validated_data.update(
                {'access_token': access_data.get('access_token')})
            serializer.validated_data.update(
                {'refresh_token': access_data.get('refresh_token')})
            if access_data.get('expire_in'):
                serializer.validated_data.update({
                    'access_token_expiry_timestamp':
                        provider_instance.make_access_token_expiry_timestamp(access_data[
                                                                             'expire_in'])
                })
            serializer.validated_data.update({
                'name': user_info.get('name', user_info.get('data', {}).get('username'))
            })
            serializer.validated_data.update(
                {'provider': getattr(FeedProviders, provider.upper()).value})
            serializer.validated_data.update({
                'user_id': user_id
            })
            access_token_instance = serializer.save(expert=request.user.expert)

        # Here retrive the page and user
        provider_instance = get_provider(provider)
        # Append the user data into the response data if provider is other than
        # Youtube
        if provider.upper() not in settings.YOUTUBE_FEED_PROVIDER:
            response_data.append({'id': access_token_instance.user_id, 'type': 'user',
                                  'name': access_token_instance.name})
        # this is for handling Instagram User, because instagram will be not
        # having pages.
        try:
            pages_data = provider_instance.get_pages(
                access_token_instance.access_token)
        except NotImplementedError:
            final_data = {'metadata': {'id': access_token_instance.id},
                          'results': response_data}
            return Response(status=status.HTTP_200_OK, data=final_data)
        page_data = provider_instance.process_page_data(pages_data)
        response_data.extend(page_data)
        final_data = {'metadata': {'id': access_token_instance.id},
                      'results': response_data}
        return Response(data=final_data)


class SocialAuthGetFeed(APIView):
    """
    Social Api view for getting the feeds for a user
    """
    permission_classes = (IsExpertPermission,)

    def get(self, request, timestamp=None, format=None):
        """
        Api to get the feeds from provider
        Args:
            request (obj): requets
            timestamp (int): timestamp
            format (str): restframework format
        Return:
            Response (obj): Response with status code and message
        """
        expert = request.user.expert
        social_links = SocialLink.objects.filter(
            account__expert=expert, is_deleted=False)
        # Here validating if timestamp is not valid
        try:
            timezone.datetime.fromtimestamp(float(timestamp), dateparse.utc)
        except ValueError:
            raise Http404

        cache_feed_ins = CacheFeedData(expert.id)
        feeds = cache_feed_ins.get_cache_feeds(timestamp, social_links)
        # Remove ignored and published contents from content_list.
        feeds = filter_contents(expert, feeds)
        return Response(data=paginate_content_results(request, feeds))


class SocialLinkViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and deleting the LinkFeed Model
    """
    queryset = SocialLink.objects.all()
    permission_classes = (IsExpertPermission,)
    serializer_class = SocialLinkSerializer
    http_method_names = ['get', 'delete', 'post']

    def get_serializer_class(self):
        serializer_class = super(
            SocialLinkViewSet, self).get_serializer_class()
        if self.request.method == 'POST':
            serializer_class = SocialLinkPostSerializer
        return serializer_class

    def get_queryset(self):
        queryset = super(SocialLinkViewSet, self).get_queryset()
        queryset = queryset.filter(account__expert=self.request.user.expert,
                                   is_deleted=False)
        return queryset


class RSSLinkView(ExperChatAPIView):
    """
    Viewset for creating the Social Account and Social Link for RSS/feed
    """
    permission_classes = (IsExpertPermission, )
    serializer_class = RSSLinkSerializer

    def post(self, request, *args, **kwargs):
        """
        post method for validating and returning the created rss/feed content data
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        social_link = serializer.save(expert=request.user.expert)
        return Response(data={'message': "Successfull", "id": social_link.id})


class ContentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, adding and deleting the Content Model Data.

    For listing like Content : {?activity-type=like}
    For listing favorite content : {?activity-type=favorite}
    """
    queryset = Content.objects.filter(is_deleted=False).order_by('id')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsFeedOwnerOrReadOnly,)
    serializer_class = ContentSerializer
    http_method_names = ['get', 'delete', 'post']

    def get_queryset(self):
        queryset = super(ContentViewSet, self).get_queryset()
        if hasattr(self.request.user, 'expert'):
            queryset = queryset.filter(owner=self.request.user)
        if self.request.query_params.get('activity-type') == 'like':
            queryset = queryset.filter(
                user_activity__user__userbase=self.request.user,
                user_activity__activity_type=ContentUserActivity.LIKE
            )
        if self.request.query_params.get('activity-type') == 'favorite':
            queryset = queryset.filter(
                user_activity__user__userbase=self.request.user,
                user_activity__activity_type=ContentUserActivity.FAVORITE
            )
        return queryset

    @detail_route(methods=['POST'], permission_classes=(IsUserPermission,), serializer_class=EmptySerializer)
    def like(self, request, pk=None, **kwargs):
        content = self.get_object()

        instance, created = ContentUserActivity.objects.get_or_create(
            content=content,
            user=request.user.user,
            activity_type=ContentUserActivity.LIKE
        )
        if created:
            like_or_unlike_content.delay(content.id, 'like')

        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['POST'], permission_classes=(IsUserPermission,), serializer_class=EmptySerializer)
    def dislike(self, request, pk=None, **kwargs):
        content = self.get_object()

        number_of_deleted_content, instance = ContentUserActivity.objects.filter(
            content=content,
            user=request.user.user,
            activity_type=ContentUserActivity.LIKE
        ).delete()
        if number_of_deleted_content:
            like_or_unlike_content.delay(content.id, 'dislike')

        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['POST'], permission_classes=(IsUserPermission,), serializer_class=EmptySerializer)
    def favorite(self, request, pk=None, **kwargs):
        content = self.get_object()

        instance, created = ContentUserActivity.objects.get_or_create(
            content=content,
            user=request.user.user,
            activity_type=ContentUserActivity.FAVORITE
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['POST'], permission_classes=(IsUserPermission,), serializer_class=EmptySerializer)
    def remove_favorite(self, request, pk=None, **kwargs):
        content = self.get_object()

        ContentUserActivity.objects.filter(
            content=content,
            user=request.user.user,
            activity_type=ContentUserActivity.FAVORITE
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class IgnoredContentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, deleting Ignored Contents
    """
    queryset = IgnoredContent.objects.all()
    permission_classes = (IsExpertPermission,)
    serializer_class = IgnoredContentSerializers
    http_method_names = ['get', 'delete', 'post']

    def get_queryset(self):
        queryset = super(IgnoredContentViewSet, self).get_queryset()
        queryset = queryset.filter(expert=self.request.user.expert)
        return queryset


class SuperAdminContentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, adding and deleting the Content Model Data
    """
    queryset = Content.objects.all()
    permission_classes = (IsSuperUser, )
    serializer_class = ContentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('content_type', 'is_deleted')

    def get_serializer_class(self):
        serializer_class = super(SuperAdminContentViewSet, self).get_serializer_class()
        if self.action not in ['list', 'retrieve']:
            serializer_class = SuperAdminContentSerializer
        return serializer_class

    def get_queryset(self):
        queryset = super(SuperAdminContentViewSet, self).get_queryset()
        if self.request.query_params.get('is_deleted') is None:
            queryset = queryset.filter(is_deleted=False)
        return queryset

    @detail_route(methods=['GET'])
    def unhide(self, request, pk=None, **kwargs):
        content = Content.objects.get(id=pk)
        content.activate()

        tags_ids = list(content.tags.all().values_list('id', flat=True))

        if content.social_link:
            profile_ids = list(
                content.social_link.expert_profiles.all().values_list('id', flat=True))
        else:
            profile_ids = []

        StreamHelper().expert_publish_content(
            content.owner_id,
            content.id,
            expert_profile_ids=profile_ids,
            tag_ids=tags_ids,
            super_admin=int(content.content_type) == FeedProviders.EXPERT_CHAT.value
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
