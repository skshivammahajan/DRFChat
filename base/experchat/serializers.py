from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework import serializers

from experchat.enumerations import TagTypes
from experchat.models.appointments import Calendar
from experchat.models.domains import Tag
from experchat.models.ratings import SessionRating
from experchat.models.users import Expert, ExpertProfile, FollowExpert, User, UserMedia
from experchat.utils import combine_slots, filter_slots, get_booked_and_available_slots, split_in_duration


class EmptySerializer(serializers.Serializer):
    pass


class ExpertSerializer(serializers.ModelSerializer):
    """
    Serializes Expert information.
    """
    id = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    profile_photo = serializers.ReadOnlyField(source='userbase.profile_photo')

    class Meta:
        model = Expert
        exclude = ('userbase', 'account_id', 'created_timestamp', 'modified_timestamp')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User information.
    """
    id = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    profile_photo = serializers.ReadOnlyField(source='userbase.profile_photo')

    class Meta:
        model = User
        fields = ('id', 'display_name', 'profile_photo')


class ExpertProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating user profiles.
    """
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.filter(tag_type__in=(TagTypes.PARENT.value, TagTypes.CHILD.value)),
        many=True
    )
    medias = serializers.PrimaryKeyRelatedField(queryset=UserMedia.objects.all(), many=True)
    expert = ExpertSerializer(read_only=True)

    class Meta:
        model = ExpertProfile
        exclude = ('created_timestamp', 'modified_timestamp')
        read_only_fields = ('is_featured', 'review_status', 'profile_submission_timestamp')

    def validate(self, attrs):
        if self.instance is None:
            profile_record = ExpertProfile.objects.filter(expert__userbase=self.context['request'].user).count()
            if profile_record >= settings.NUM_PROFILE_USER_ALLOWED:
                raise serializers.ValidationError('ERROR_MAX_PROFILES')
        return attrs

    def validate_tags(self, value):
        if len(value) > getattr(settings, 'MAX_TAGS_COUNT', 20):
            raise serializers.ValidationError('ERROR_TAG_MAX')
        return value

    def validate_medias(self, value):
        request = self.context.get('request')
        for media in value:  # value is list of user media.
            if media.owner != request.user:  # User is trying to do some hacking.
                raise serializers.ValidationError('ERROR_MEDIA_INVALID')

        if len(value) > settings.ALLOWED_MEDIA_RECORD:
            raise serializers.ValidationError('ERROR_MEDIA_LIMIT_MAX')
        return value

    def validate_my_experience(self, value):
        if len(''.join(strip_tags(value).replace('↵', '').rstrip().splitlines())) > getattr(settings, 'MAX_EXPERIENCE_CHAR', 1000):
            raise serializers.ValidationError('ERROR_MAX_EXPERIENCE_CHARS')
        return value

    def validate_educational_background(self, value):
        if len(''.join(strip_tags(value).replace('↵', '').rstrip().splitlines())) > getattr(settings, 'MAX_EDU_BACK_CHAR', 1000):
            raise serializers.ValidationError('ERROR_MAX_EDUCATIONAL_CHARS')
        return value


class ProfileMediaSerializer(serializers.ModelSerializer):
    """
    Serializes profile media for nesting in expertprofile serializer.
    """
    class Meta:
        model = UserMedia
        exclude = ('owner', 'profile')


class TagSerializer(serializers.ModelSerializer):
    """
    Serializes tag model for nesting in expertprofile serializer.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'tag_type', 'parent')

    def get_fields(self):
        fields = super(TagSerializer, self).get_fields()
        fields['parent'] = TagSerializer()
        return fields


class ExpertProfileListSerializer(serializers.ModelSerializer):
    """
    Expert serializer for list action.
    """
    expert = ExpertSerializer(read_only=True)
    calendars = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    content_count = serializers.ReadOnlyField()

    class Meta:
        model = ExpertProfile

        fields = ('id', 'expert', 'headline', 'calendars', 'following', 'is_featured', 'review_status', 'summary',
                  'content_count', 'profile_submission_timestamp')
        read_only_fields = ('is_featured', 'review_status', 'content_count', 'profile_submission_timestamp')

    def get_calendars(self, obj):
        slots = obj.expert.calendars.all().order_by('start_time')
        available_slots, booked_slots = get_booked_and_available_slots(obj.expert_id)
        filtered_booked_slots = filter_slots(slots, booked_slots)
        # GET the slots with 30 min duration
        final_slots = split_in_duration(filtered_booked_slots, 30)
        combined_slots = combine_slots(final_slots, only_till_next_day=True)
        return combined_slots

    def get_following(self, obj):
        if self.context['request'].user.is_anonymous():
            return False
        return obj.expert.followers.filter(user__userbase=self.context['request'].user).exists()


class ExpertProfileDetailSerializer(ExpertProfileSerializer):
    """
    Expert profile for retrieve action.
    """
    tags = TagSerializer(many=True, read_only=True)
    medias = serializers.SerializerMethodField()
    calendars = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    def get_calendars(self, obj):
        slots = obj.expert.calendars.all().order_by('start_time')
        available_slots, booked_slots = get_booked_and_available_slots(obj.expert_id)
        filtered_booked_slots = filter_slots(slots, booked_slots)
        # GET the slots with 30 min duration
        final_slots = split_in_duration(filtered_booked_slots, 30)
        combined_slots = combine_slots(final_slots)
        return combined_slots

    def get_medias(self, obj):
        medias = obj.medias.order_by('-is_primary')
        return ProfileMediaSerializer(medias, many=True).data

    def get_following(self, obj):
        if self.context['request'].user.is_anonymous():
            return False
        return obj.expert.followers.filter(user__userbase=self.context['request'].user).exists()


class CalendarSerializer(serializers.ModelSerializer):
    """
    Calendar Serializer for list, detail delete action
    """
    class Meta:
        model = Calendar
        exclude = ('expert',)

    def validate(self, attrs):
        start_time = attrs['start_time']
        end_time = attrs['end_time']

        if start_time > end_time:
            raise serializers.ValidationError({'end_time': 'ERROR_INVALID_END_TIME'})

        if any([start_time.second, end_time.second]):
            raise serializers.ValidationError('ERROR_INVALID_TIME')

        time_diff = timezone.timedelta(hours=end_time.hour, minutes=end_time.minute) - \
            timezone.timedelta(hours=start_time.hour, minutes=start_time.minute)

        if time_diff.seconds // 60 < getattr(settings, 'APPOINTMENT_START_END_TIME_INTERVAL', 20):
            raise serializers.ValidationError('ERROR_INVALID_INTERVAL_TIME')
        return attrs

    def validate_start_time(self, value):
        if value.minute % getattr(settings, 'APPOINTMENT_MINUTES_INTERVAL', 5) != 0:
            raise serializers.ValidationError('ERROR_INVALID_START_TIME_MINUTES')
        return value

    def validate_end_time(self, value):
        if value.minute % getattr(settings, 'APPOINTMENT_MINUTES_INTERVAL', 5) != 0:
            raise serializers.ValidationError('ERROR_INVALID_END_TIME_MINUTES')
        return value

    def validate_timezone(self, value):
        if value not in timezone.pytz.all_timezones:
            raise serializers.ValidationError('ERROR_INVALID_TIMEZONE')
        return value


class SessionRatingSerializer(serializers.ModelSerializer):
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = SessionRating
        exclude = ('session',)
        extra_kwargs = {
            'text_review': {
                'allow_blank': True,
            },
        }

    def get_reviewer(self, obj):
        ec_user = None
        if hasattr(obj.session.user, 'user'):
            ec_user = obj.session.user.user

        return UserSerializer(instance=ec_user).data
