from __future__ import division

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from devices.enumerations import DeviceStatus
from devices.models import Device
from experchat.models.session_pricing import SessionPricing
from experchat.serializers import ExpertSerializer
from experchat_sessions.models import Session
from experchat_sessions.utils import (
    calculate_discount_price, is_already_scheduled, is_valid_promocode, is_valid_scheduled_slot
)
from payments.models import Card

UserBase = get_user_model()


class SessionSerializer(serializers.ModelSerializer):
    """
    Validate data to be used for session initialization.
    """
    class Meta:
        model = Session
        fields = ('id', 'expert_profile', 'expert', 'user_device', 'scheduled_duration')

    def validate(self, attrs):
        expert = attrs['expert']
        expert_profile = attrs.get("expert_profile")
        if expert_profile.expert != expert:
            raise serializers.ValidationError({'expert_profile': 'ERROR_INVALID_EXPERT_PROFILE'})

        user = self.context['request'].user
        user_device = attrs.get("user_device")
        if user_device.user != user:
            raise serializers.ValidationError({'user_device': 'ERROR_INVALID_USER_DEVICE'})

        session_price = SessionPricing.objects.filter(session_length=attrs['scheduled_duration']).first()

        if session_price is None:
            raise serializers.ValidationError({'scheduled_duration': 'ERROR_INVALID_SCHEDULED_DURATION'})

        attrs['estimated_revenue'] = session_price.price
        return attrs


class AcceptSerializer(serializers.ModelSerializer):
    """
    Validate expert device.
    """
    class Meta:
        model = Session
        fields = ('id', 'expert_device')

    def validate(self, attrs):
        expert = self.context['request'].user
        expert_device = attrs.get("expert_device")

        if expert_device.user != expert:
            raise serializers.ValidationError({'expert_device': 'ERROR_INVALID_EXPERT_DEVICE'})
        return attrs


class DelaySerializer(serializers.Serializer):
    """
    Validate delay time.
    """
    delay_time = serializers.IntegerField(required=True)


class DisconnectSerializer(serializers.Serializer):
    """
    Validate tokbox session length.
    """
    tokbox_session_length = serializers.IntegerField(required=True)


class SwitchDeviceSerializer(serializers.Serializer):
    """
    Validate device id passed for switching.
    """
    device_id = serializers.IntegerField(required=True)

    def validate_device_id(self, value):
        devices = Device.objects.filter(
            user=self.context['request'].user,
            id=value,
            status=DeviceStatus.ACTIVE.value
        )

        if not devices.exists():
            raise serializers.ValidationError('ERROR_INVALID_DEVICE_ID')

        return value


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField(source='user.display_name')

    class Meta:
        model = UserBase
        fields = ('id', 'display_name', 'profile_photo')


class ScheduleSessionSerializer(serializers.ModelSerializer):
    """
    Validated data to be used for session scheduling.
    """
    class Meta:
        model = Session
        fields = ('id', 'title', 'details', 'scheduled_datetime', 'expert_profile', 'expert',
                  'user_device', 'scheduled_duration', 'estimated_revenue', 'card', 'promo_code')
        read_only_fields = ('estimated_revenue',)
        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False, 'allow_null': False},
            'scheduled_datetime': {'required': True},
            'scheduled_duration': {'required': True},
        }

    def validate_user_device(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError('ERROR_INVALID_USER_DEVICE')
        return value

    def validate_card(self, value):
        if value is None:
            return settings.TEST_CARD_ID
        user = self.context['request'].user
        if not Card.objects.filter(id=value, customer__user=user).exists():
            raise serializers.ValidationError('ERROR_INVALID_CARD')
        return value

    def validate(self, attrs):
        expert_profile = attrs['expert_profile']
        expert = attrs['expert']
        user = self.context['request'].user

        if expert_profile.expert != expert:
            raise serializers.ValidationError({'expert_profile': 'ERROR_INVALID_EXPERT_PROFILE'})

        session_price = SessionPricing.objects.filter(session_length=attrs['scheduled_duration']).first()

        if session_price is None:
            raise serializers.ValidationError({'scheduled_duration': 'ERROR_INVALID_SCHEDULED_DURATION'})

        attrs['estimated_revenue'] = session_price.price

        if attrs['scheduled_datetime'] < timezone.now():
            raise serializers.ValidationError({'scheduled_datetime': 'ERROR_INVALID_SCHEDULED_DATETIME'})

        if is_already_scheduled(user, attrs['scheduled_datetime'], attrs['scheduled_duration']):
            raise serializers.ValidationError('ERROR_INVALID_SCHEDULED_SLOT')

        if not is_valid_scheduled_slot(expert.id, attrs['scheduled_datetime'], attrs['scheduled_duration']):
            raise serializers.ValidationError('ERROR_INVALID_SCHEDULED_SLOT')

        if not attrs.get('card'):
            attrs['card'] = settings.TEST_CARD_ID

        # Validate the promo code
        if attrs.get('promo_code'):
            is_valid_coupon_code = is_valid_promocode(
                self.context['request'].user.user, attrs['promo_code'], attrs['expert'].id,
                attrs['scheduled_datetime']
            )
            if is_valid_coupon_code is False:
                raise serializers.ValidationError('ERROR_PROMO_CODE_INVALID')

        return attrs


class SessionListSerializer(serializers.ModelSerializer):
    expert_profile_headline = serializers.ReadOnlyField(source='expert_profile.headline')
    user = UserSerializer()
    expert = ExpertSerializer()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Session
        fields = ('id', 'start_timestamp', 'tokbox_session_length', 'scheduled_duration', 'revenue',
                  'expert_profile_headline', 'title', 'details', 'user', 'expert', 'scheduled_datetime', 'status',
                  'estimated_revenue')


class ValidatePromoCodeSerializer(serializers.Serializer):
    """
    Serilizer for validating the promo code
    """
    promo_code = serializers.CharField(required=True)
    expert_id = serializers.IntegerField(required=True)
    session_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    scheduled_datetime = serializers.DateTimeField(required=True)
    discount_price = serializers.SerializerMethodField()

    def validate(self, attrs):
        is_valid_promo_code = is_valid_promocode(
            self.context['request'].user.user, attrs['promo_code'], attrs['expert_id'], attrs['scheduled_datetime']
        )
        if not is_valid_promo_code:
            raise serializers.ValidationError('ERROR_PROMO_CODE_INVALID')

        return attrs

    def get_discount_price(self, obj):
        return calculate_discount_price(obj['promo_code'], obj['session_price'])


class ApplyPromoCodeSerializer(serializers.Serializer):
    """
    Serilizer for Applying the promo code on already scheduled Session
    """
    promo_code = serializers.CharField(required=True)

    def validate(self, attrs):
        session = Session.objects.filter(id=self.context['pk']).first()
        if session.promo_code:
            raise serializers.ValidationError('ERROR_ALREADY_APPLIED_COUPON_CODE')

        is_valid_promo_code = is_valid_promocode(
            self.context['request'].user.user, attrs['promo_code'], session.expert.id, session.scheduled_datetime
        )

        if not is_valid_promo_code:
            raise serializers.ValidationError('ERROR_PROMO_CODE_INVALID')

        return attrs
