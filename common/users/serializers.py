import random
import string
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from experchat.enumerations import ExpertNotificationSettingCodes
from experchat.models.promocodes import PromoCode
from experchat.models.users import Expert, UserMedia
from experchat.serializers import ExpertProfileSerializer
from feeds.models import Content
from registration.models import VerificationToken
from registration.utils import check_verify_notification_spamming
from users.models import ExpertAccount
from users.utils import check_expert_profile_completeness, check_expert_review_status, save_expert_uid, validate_phone

UserBase = get_user_model()


class UserBasicInfoSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='user.display_name', max_length=100)
    is_profile_complete = serializers.SerializerMethodField()

    class Meta:
        model = UserBase
        fields = ('id', 'name', 'email', 'country_code', 'phone_number', 'is_phone_number_verified',
                  'is_profile_complete', 'profile_photo', 'display_name', 'is_superuser',
                  'toc_and_privacy_policy_accepted')
        read_only_fields = ('email', 'profile_photo', 'country_code', 'phone_number', 'is_phone_number_verified',
                            'is_profile_complete', 'is_superuser', 'toc_and_privacy_policy_accepted')

    def get_is_profile_complete(self, obj):
        if hasattr(obj, 'expert'):
            return check_expert_profile_completeness(obj) and check_expert_review_status(obj.expert)
        return check_expert_profile_completeness(obj)

    def update(self, instance, validated_data):
        if 'user' in validated_data:   # key user is not available in case of PATCH method and for expert.
            user = validated_data.pop('user')
            instance.user.display_name = user.get('display_name')
            instance.user.save()

        expert_name = validated_data.get('name')
        if expert_name:
            is_expert_uid = save_expert_uid(expert_name, instance)
            if not is_expert_uid:
                return None

        super(UserBasicInfoSerializer, self).update(instance, validated_data)
        return instance


class ExpertBasicInfoSerializer(UserBasicInfoSerializer):
    display_name = serializers.CharField(source='expert.display_name', allow_blank=False)
    expert_uid = serializers.ReadOnlyField(source='expert.expert_uid')

    class Meta(UserBasicInfoSerializer.Meta):
        fields = ('id', 'name', 'email', 'country_code', 'phone_number', 'is_phone_number_verified',
                  'profile_photo', 'display_name', 'expert_uid', 'toc_and_privacy_policy_accepted',
                  'is_profile_complete')

    def validate_display_name(self, value):
        if self.instance and self.instance.expert.display_name == value:
            return value

        if Expert.objects.filter(display_name=value).exists():
            raise serializers.ValidationError('ERROR_DISPLAY_NAME_ALREADY_USED')
        return value

    def update(self, instance, validated_data):
        if 'expert' in validated_data:
            expert = validated_data.pop('expert')
            instance.expert.display_name = expert.get('display_name')
            instance.expert.save()

        return super(ExpertBasicInfoSerializer, self).update(instance, validated_data)


class PhotoUploadSerializer(serializers.Serializer):
    image = serializers.CharField()


class ProfileMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMedia
        exclude = ('owner', 'profile')


class MediaSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading Images and Videos for user profile.
    """

    class Meta:
        model = UserMedia
        exclude = ('owner', 'profile')
        read_only_fields = ('media_type', 'owner',)

    def validate_media(self, value):
        if not value:
            raise serializers.ValidationError('ERROR_REQUIRED_VALUE')

        # Get content type initial from content's content-type
        # EX: Extract image from image/png, image/jpeg
        # or video from video/mp4
        content_type = value.content_type.split('/')[0]   # File type image /video
        if content_type not in settings.ALLOWED_MEDIA_TYPES:
            raise serializers.ValidationError('ERROR_MEDIA_NOT_ALLOWED')
        # content-type == Image, _size in bytes
        if content_type == settings.MEDIA_TYPE_IMAGE and value._size > settings.MAX_IMG_SIZE:
                raise serializers.ValidationError('ERROR_IMG_SIZE_MAX')
        # content-type == Video, _size in bytes
        elif content_type == settings.MEDIA_TYPE_VIDEO and value._size > settings.MAX_VID_SIZE:
                raise serializers.ValidationError('ERROR_VIDEO_SIZE_MAX')

        return value


class PhoneCodeSendSerializer(serializers.Serializer):
    country_code = serializers.IntegerField()
    mobile = serializers.CharField()

    def validate(self, attrs):
        country_code = attrs["country_code"]
        mobile = attrs["mobile"]
        request = self.context['request']
        entered_phone = "+" + str(country_code) + mobile
        if not validate_phone(entered_phone):
            raise serializers.ValidationError('ERROR_PHONE_INVALID')

        if (request.user.country_code == country_code and request.user.phone_number == mobile
                and request.user.is_phone_number_verified):
            raise serializers.ValidationError('ERROR_VERIFIED_PHONE')

        if check_verify_notification_spamming(request.user, VerificationToken.PHONE_VERIFICATION):
            raise serializers.ValidationError('ERROR_MAX_OTP_REQUEST')

        return attrs


class PhoneVerifySerializer(serializers.Serializer):
    """
    Serializer for email verification for user activation.
    """
    passcode = serializers.CharField()

    def validate(self, attrs):
        verification_code = attrs["passcode"]
        user = self.context['request'].user

        verification_token_obj = VerificationToken.objects.filter(
            user=user,
            purpose=VerificationToken.PHONE_VERIFICATION,
            token=verification_code,
            expired_at__isnull=True,
        ).first()

        if not verification_token_obj:
            raise serializers.ValidationError('ERROR_OTP_NO_MATCH')

        if verification_token_obj.created_timestamp < (
            timezone.now() - timezone.timedelta(minutes=settings.PHONE_VERIFICATION_TOKEN_EXPIRY)
        ):
            raise serializers.ValidationError('ERROR_OTP_EXPIRED')

        attrs['verification_token_obj'] = verification_token_obj
        return attrs


class ResendPhoneCodeSendSerializer(serializers.Serializer):
    """
    Serializer for resend email for verification .
    """
    country_code = serializers.IntegerField()
    mobile = serializers.CharField()

    def validate(self, attrs):
        country_code = attrs["country_code"]
        mobile = attrs["mobile"]
        user = self.context['request'].user

        if check_verify_notification_spamming(user, VerificationToken.PHONE_VERIFICATION):
            raise serializers.ValidationError('ERROR_MAX_OTP_REQUEST')

        if user.phone_number is None:
            raise serializers.ValidationError('ERROR_NO_MOBILE')

        if (user.country_code == country_code and user.phone_number == mobile
                and user.is_phone_number_verified):
            raise serializers.ValidationError('ERROR_VERIFIED_PHONE')

        return attrs


class ConfidentialField(serializers.CharField):

    def run_validation(self, data=None):
        value = super(ConfidentialField, self).run_validation(data)
        return self.stream_cipher(value, settings.CONFIDENTIAL_FIELD_ENCRYPTION_KEY)

    def to_representation(self, value):
        value = self.stream_cipher(value, settings.CONFIDENTIAL_FIELD_ENCRYPTION_KEY, False)
        return 'X'*(len(value)-4) + value[-4:]

    def shift(self, current_position, distance, direction: (0, 1)):
        direction = 1 if direction else -1
        return current_position + direction * distance

    def stream_cipher(self, message, key, do_encrypt=True):
        """
        This function will receive a message, a key, and the
        decision to encrypt or decrypt the message.
        The function uses a stream cipher encryption algorithm
        which replaces each letter in the message with a
        pseudo-random character from a given character set.
        Example:
        >>> stream_cipher("This is a test", 1234)
        'wPwV~#5;:D"905'
        >>> stream_cipher('wPwV~#5;:D"905', 1234, False)
        'This is a test'
        """
        random.seed(key)
        # The character set must be multiplied by 2 so
        # a character shifted beyond the end of the
        # character set will loop back to the beginning.
        characters = 2 * (string.ascii_letters + string.digits + string.punctuation + ' ')
        # I declare this in a variable so the
        # program can work with a variable length character set
        lenchars = len(characters)//2
        # This will replace each character in the message
        # with a pseudo-random character selected from
        # the character set.
        return ''.join([
            characters[
                self.shift(
                    characters.index(message[each_char]),
                    lenchars - int(lenchars * random.random()),
                    do_encrypt
                )
            ] for each_char in range(len(message))
        ])


def validate_account_number(value):
    try:
        int(value)
    except ValueError:
        raise serializers.ValidationError('ERROR_INVALID_ACCOUNT_NUMBER')

    return value


class ExpertAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Expert Account information.
    """
    account_number = ConfidentialField(validators=[validate_account_number])

    class Meta:
        model = ExpertAccount
        exclude = ('expert', 'is_active')

    # NOTE: Instead of writing below method, write a validator instead.
    # def validate_account_number(self, value):

    def validate_routing_number(self, value):
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError('ERROR_INVALID_ROUTING_NUMBER')

        if len(value) != 9:
            raise serializers.ValidationError('ERROR_INVALID_LENGTH_OF_ROUTING_NUMBER')

        return value


class PromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromoCode
        fields = '__all__'
        read_only_fields = ('is_deleted',)

    def validate(self, attrs):
        if attrs['value_type'] == PromoCode.PERCENT_OFFER:
            if attrs['value'] > 100:
                raise serializers.ValidationError('ERROR_INVALID_DISCOUNT')
        return attrs


class ExpertNotificationSettingsSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        for setting_code in ExpertNotificationSettingCodes.__members__.values():
            self.fields.update({setting_code.value: serializers.BooleanField(default=True)})
        super(ExpertNotificationSettingsSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        invalid_fields = set(self.initial_data.keys()) - set(self.fields.keys())
        if invalid_fields:
            raise serializers.ValidationError('ERROR_INVALID_NOTIFICATION_SETTING')
        return attrs


class FeaturedExpertSerializer(ExpertProfileSerializer):
    content_count = serializers.SerializerMethodField()

    def get_content_count(self, obj):
        return Content.objects.filter(
            owner=obj.expert.userbase, is_deleted=False,
            created_timestamp__gte=timezone.now() - timedelta(hours=24)).count()
