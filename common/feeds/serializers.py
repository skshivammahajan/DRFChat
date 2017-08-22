import re

from django.conf import settings
from django.utils.html import strip_tags
from rest_framework import serializers

from experchat.models.users import Expert
from experchat.serializers import ExpertSerializer, TagSerializer
from feeds.cache_feeds import CacheFeedData
from feeds.choices import FeedProviders, FeedTypes
from feeds.models import Content, ContentUserActivity, IgnoredContent, SocialAccount, SocialLink
from feeds.providers import get_provider
from feeds.utils import PushFeeds, PushSuperAdminFeeds, get_tag_ids_with_parent, update_content_tags_at_getsream
from feeds.validators import is_valid_feed_url


class AppProviderSericalizer(serializers.Serializer):
    """
    Provider Serializer
    """
    provider = serializers.CharField(required=True)


class SocialAuthAppCodeSerializer(AppProviderSericalizer):
    """
    Serializer class for token which is used to connect to the user on FB
    """
    app_code = serializers.CharField(required=True)

    def create(self, validated_data):
        validated_data.pop('app_code')
        return SocialAccount.objects.create(**validated_data)


class SocialLinkSerializer(serializers.ModelSerializer):
    """
    Model Serializer for LinkFeedModel
    """
    class Meta:
        model = SocialLink
        exclude = ('expert_profiles',)


class SocialAccountSerializer(serializers.ModelSerializer):
    """
    Social Account Serializer
    """
    class Meta:
        model = SocialAccount
        exclude = ()


class SocialLinkUpdateSerializer(serializers.Serializer):
    """
    Social Links Update expert_profile
    """
    social_link_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True
    )

    def validate(self, attrs):
        """
        Validate the provided ids are valid id or not
        Args:
            attrs (dict): request data
        Returns:
            attrs (dict): data dict
        Raise:
            Validation Error
        """
        request = self.context['request']
        social_link_ids = SocialLink.objects.filter(account__expert__userbase=request.user,
                                                    id__in=attrs["social_link_ids"]).values_list('id', flat=True)
        invalid_ids = set(attrs["social_link_ids"]) - set(social_link_ids)

        if invalid_ids:
            raise serializers.ValidationError('ERROR_LINK_HAS_BEEN_REMOVED')
        return attrs


class SocialLinkPostSerializer(serializers.ModelSerializer):
    """
    Model Serializer for LinkFeedModel
    """
    account = SocialAccountSerializer

    class Meta:
        model = SocialLink
        fields = ('feed_type', 'account', 'detail')

    def validate(self, attrs):
        """
        valide the post data and user data and page data
        Attr:
            attrs (dict): dict containing the keys
        return:
            attrs (dict): dict with updated data which needs to be saved in db
        raise:
            validation error if any
        """
        provider = [provider.name for provider in FeedProviders if provider.value == attrs['feed_type']]
        provider_instance = get_provider(provider[0])
        # Calling the API to get user info to verify the validity of user
        user_data = provider_instance.get_user_info_data(attrs['account'].access_token)
        user_data = provider_instance.process_user_data(user_data)
        valid_user_data = attrs['detail'] == user_data['id']
        # calling the API for pages
        try:
            pages_data = provider_instance.get_pages(attrs['account'].access_token)
        except NotImplementedError:
            if not valid_user_data:
                raise serializers.ValidationError(
                    "Requested id={} is not a valid id".format(attrs['detail'])
                )
            attrs.update({'other_data': user_data})
            return attrs
        page_data = provider_instance.process_page_data(pages_data)
        valid_page_data = [page for page in page_data if attrs['detail'] == page['id']]
        if not any([valid_page_data, valid_user_data]):
            raise serializers.ValidationError(
                "Requested id={} is not a valid id".format(attrs['detail'])
            )
        if valid_user_data:
            attrs.update({'other_data': user_data})
        elif valid_page_data:
            attrs.update({'other_data': valid_page_data[0]})
        return attrs

    def validate_feed_type(self, value):
        provider = [provider.name for provider in FeedProviders if provider.value == value]
        if not provider:
            raise serializers.ValidationError('ERROR_INVALID_PROVIDER')
        return value

    def create(self, validated_data):
        """
        Create new instance if not existes otherwise update the existing instance
        Args:
            validated_data (dict): Validated dict
        return:
            social link instance
        """
        # Here using get_or_create since if a social link is deleted then that will be soft deleted in the system
        # and then from the workflow we need to make that available without creating new column
        social_link, created = SocialLink.objects.get_or_create(
            account=validated_data['account'],
            feed_type=validated_data['feed_type'],
            feed_sub_type=getattr(FeedTypes, validated_data['other_data']['type'].upper()).value,
            detail=validated_data['detail'],
            defaults={
                'display_name': validated_data['other_data']['name']
            }
        )
        if not created:
            social_link.detail = validated_data['detail']
            social_link.display_name = validated_data['other_data']['name']
            social_link.is_deleted = False
            social_link.save()

        return social_link


class RSSLinkSerializer(serializers.Serializer):
    """
    Validate User provided RSS Link.
    """
    url = serializers.URLField(required=True)

    def validate(self, attrs):
        url = attrs.pop('url')
        parse_data = is_valid_feed_url(url)
        attrs['name'] = parse_data.feed.title
        attrs['provider'] = getattr(FeedProviders, 'RSS').value
        attrs['access_token'] = url
        attrs['user_id'] = ""
        attrs['feed_sub_type'] = getattr(FeedTypes, 'FEED').value
        return attrs

    def create(self, validated_data):
        """
        method which will be creating the instance data
        Args:
            validated_data (dict): Validated post data
        return:
            Social link instance
        """
        account, created = SocialAccount.objects.get_or_create(
            expert=validated_data['expert'],
            access_token=validated_data['access_token'],
            provider=validated_data['provider'],
            defaults={
                'name': validated_data['name'],
                'user_id': validated_data['user_id']
            }
        )
        if not created:
            account.name = validated_data['name']
            account.user_id = validated_data['user_id']
            account.save()

        social_link, created = SocialLink.objects.get_or_create(
            account=account,
            feed_type=validated_data['provider'],
            feed_sub_type=validated_data['feed_sub_type'],
            defaults={
                'detail': validated_data['access_token'],
                'display_name': validated_data['name']
            }
        )
        if not created:
            social_link.detail = validated_data['access_token']
            social_link.display_name = validated_data['name']
            social_link.is_deleted = False
            social_link.save()
        return social_link


class ContentSerializer(serializers.ModelSerializer):
    """
    Content model Serializer
    """
    owner = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    likes = serializers.ReadOnlyField()
    liked_by_current_user = serializers.SerializerMethodField()
    saved_by_current_user = serializers.SerializerMethodField()
    description_text = serializers.SerializerMethodField()
    description_image = serializers.SerializerMethodField()
    content = serializers.ReadOnlyField()

    class Meta:
        model = Content
        exclude = ('social_link', )
        read_only_fields = ('title', 'content_type', 'image', 'description',
                            'timestamp', 'owner', 'content_stats', 'is_deleted')
        # this is used to overide the default validation for unique content_id
        extra_kwargs = {
            'content_id': {
                "validators": []
            }
        }

    def get_liked_by_current_user(self, obj):
        request = self.context['request']
        if hasattr(request.user, 'user'):
            return obj.user_activity.filter(user=request.user.user, activity_type=ContentUserActivity.LIKE).exists()
        return False

    def get_saved_by_current_user(self, obj):
        request = self.context['request']
        if hasattr(request.user, 'user'):
            return obj.user_activity.filter(user=request.user.user, activity_type=ContentUserActivity.FAVORITE).exists()
        return False

    def get_description_text(self, obj):
        if obj.description is None:
            return ""

        description_text = strip_tags(obj.description)
        if len(description_text) == obj.description:
            return ""

        return description_text

    def get_description_image(self, obj):
        if obj.description is None:
            return ""

        match = re.search(r'src="(.*?)"', obj.description)

        if match is not None:
            return match.group(1)

        return ""

    def get_owner(self, obj):
        if hasattr(obj.owner, 'expert'):
            return ExpertSerializer(obj.owner.expert).data

        return {
            "id": obj.owner.id,
            "display_name": obj.owner.user.display_name if hasattr(obj.owner, 'user')
            else settings.EC_ADMIN_DISPLAY_NAME,
            "profile_photo": obj.owner.profile_photo,
            "expert_uid": "",
            "avg_rating": 0.0,
            "num_rating": 0.0
        }

    def validate(self, attrs):
        """
        validate the posted data
        Args:
            attrs (dict): request data
        Returns:
            attrs (dict): data dict
        Raise:
            Validation Error
        """
        expert = self.context['request'].user
        content_id = attrs['content_id']
        cached_feed = CacheFeedData(expert.id)
        try:
            if int(content_id.rsplit('_', 1)[-1]) != expert.id:
                raise serializers.ValidationError('ERROR_CONTENT_NOT_EXIST')
        except ValueError:
            raise serializers.ValidationError('ERROR_CONTENT_NOT_EXIST')
        feed = cached_feed.get_feeds_by_content_id(content_id)
        if not feed:
            raise serializers.ValidationError('ERROR_CONTENT_HAS_BEEN_REMOVED')
        try:
            content = Content.objects.get(content_id=content_id)
            if not content.is_deleted:
                raise serializers.ValidationError('ERROR_CONTENT_ALREADY_PUBLISHED')
        except Content.DoesNotExist:
            social_link = SocialLink.objects.get(id=feed['social_link_id'])
            attrs['title'] = feed['title']
            attrs['content_type'] = social_link.feed_type
            attrs['image'] = feed['image']
            attrs['description'] = feed['description']
            attrs['timestamp'] = feed['timestamp']
            attrs['content'] = feed.get('content')
            attrs['social_link'] = social_link
            attrs['owner'] = expert
        return attrs

    def create(self, validated_data):
        """
        method which will be creating the or updating the Content Model and call the util
        method to push the feed on stream feed
        Args:
            validated_data (dict): Validated post data
        return:
            Content Model instance
        """
        content_id = validated_data.pop('content_id')
        instance, created = Content.objects.get_or_create(content_id=content_id, defaults=validated_data)
        if not created:
            instance.is_deleted = False
            instance.save()

        push_feeds = PushFeeds(instance.social_link)
        tags = push_feeds.tag_objs()
        instance.tags.add(*tags)
        push_feeds.push_feeds_to_streamfeed(instance)
        return instance


class IgnoredContentSerializers(serializers.ModelSerializer):
    """
    IgnoredContent model Serializer
    """
    class Meta:
        model = IgnoredContent
        fields = ('id', 'content_id',)

    def validate(self, attrs):
        """
        validate the posted data
        Args:
            attrs (dict): request data
        Returns:
            attrs (dict): data dict
        Raise:
            Validation Error
        """
        expert = self.context['request'].user.expert
        content_id = attrs['content_id']
        cached_feed = CacheFeedData(expert.id)
        try:
            expert_id = int(content_id.split('_')[-1])
        except ValueError:
            raise serializers.ValidationError('ERROR_CONTENT_NOT_EXIST')
        if expert_id != expert.id:
            raise serializers.ValidationError('ERROR_CONTENT_NOT_EXIST')
        feed = cached_feed.get_feeds_by_content_id(content_id)
        if not feed:
            raise serializers.ValidationError('ERROR_CONTENT_HAS_BEEN_REMOVED')
        try:
            IgnoredContent.objects.get(content_id=content_id)
            raise serializers.ValidationError('ERROR_CONTENT_ALREADY_IGNORED')
        except IgnoredContent.DoesNotExist:
            attrs['expert'] = expert
        return attrs

    def create(self, validated_data):
        """
        method which will be creating IgnoredContent
        Args:
            validated_data (dict): Validated post data
        return:
            IgnoredContent Model instance
        """
        return IgnoredContent.objects.create(**validated_data)


class SuperAdminContentSerializer(serializers.ModelSerializer):
    """
    Serializer class for Content Model which is used by SuperAdmin
    """
    likes = serializers.ReadOnlyField()
    content = serializers.ReadOnlyField()
    to_expert = serializers.IntegerField(required=False, label="Post To Expert")

    class Meta:
        model = Content
        exclude = ('social_link',)
        read_only_fields = ('content_type', 'is_deleted', 'timestamp',
                            'owner', 'content_stats', 'liked_by_current_user',
                            'saved_by_current_user')

    def validate(self, attrs):
        """
        validate the posted data and construct the fields value which needs to be saved
        Args:
            attrs (dict): dict
        return:
            attrs
        raise:
            ValidationError
        """
        # check if content exists then make the expert to the owner of content
        if self.instance:
            if (self.context['request']._request.method in ['PUT', 'PATCH'] and
                    int(self.instance.content_type) != FeedProviders.EXPERT_CHAT.value):
                raise serializers.ValidationError('ERROR_SOCIAL_LOGIN')

            expert = self.instance.owner
        else:
            # check if Super admin is posting content on behalf of Expert then make the expert as owner
            if attrs.get('to_expert'):
                try:
                    expert = Expert.objects.get(userbase=attrs.get('to_expert')).userbase
                except Expert.DoesNotExist:
                    raise serializers.ValidationError('ERROR_SOCIAL_LOGIN')
            else:
                expert = self.context['request'].user

        key_id = settings.SOCIAL_KEY_MAPPING.get(FeedProviders['EXPERT_CHAT'].name)
        if not key_id:
            raise serializers.ValidationError('ERROR_SOCIAL_LOGIN')

        if attrs.get('content_id') is None:
            return attrs

        content_id_list = attrs['content_id'].split('_')
        try:
            # check if the content id posted is already exists
            if len(content_id_list) > 2 and (content_id_list[0] + '_') == key_id and \
                    int(content_id_list[-1]) == expert.id:
                new_content_id = attrs['content_id']
            else:
                new_content_id = key_id + attrs['content_id'] + "_{}".format(expert.id)
        except ValueError:
            new_content_id = key_id + attrs['content_id'] + "_{}".format(expert.id)
        try:
            content = Content.objects.get(content_id=new_content_id)
            if self.context['request']._request.method not in ['PUT', 'PATCH'] or self.instance != content:
                raise serializers.ValidationError('ERROR_CONTENT_ALREADY_PUBLISHED')
        except Content.DoesNotExist:
            attrs['content_type'] = FeedProviders['EXPERT_CHAT'].value
            attrs['owner'] = expert

        attrs['content_id'] = new_content_id
        return attrs

    def create(self, validated_data):
        """
        method which will be creating Content Model and call the util method to push the feeds on streamfeeds
        method to push the feed on stream feed
        Args:
            validated_data (dict): Validated post data
        return:
            Content Model instance
        """
        tags = validated_data.pop('tags')
        validated_data.pop('to_expert', None)
        instance = Content.objects.create(**validated_data)
        # add the tags to content
        instance.tags.add(*tags)

        super_admin_push_feeds = PushSuperAdminFeeds(validated_data['owner'])
        tag_ids = get_tag_ids_with_parent(tags)
        # push to stream feeds
        super_admin_push_feeds.push_super_admin_feeds(instance, tag_ids, super_admin=True)
        return instance

    def update(self, instance, validated_data):
        """
        Method to update the Content model instance, and call the utill method to update the tags from stremfeeds
        Args:
            instance (obj): Content model Instance
            validated_data (dict): Validated data
        return:
            updated instance of Content model
        """
        tags = validated_data.pop('tags', [])
        tag_ids = get_tag_ids_with_parent(tags)
        update_content_tags_at_getsream(instance.id, tag_ids)
        return super(SuperAdminContentSerializer, self).update(instance, validated_data)
