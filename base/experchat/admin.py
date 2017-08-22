from django.contrib import admin

from experchat.models.appointments import Calendar
from experchat.models.domains import Domain, Tag
from experchat.models.promocodes import PromoCode
from experchat.models.ratings import SessionRating
from experchat.models.session_pricing import SessionPricing
from experchat.models.sessions import EcDevice, EcSession
from experchat.models.stats import DailyExpertStats
from experchat.models.users import Expert, ExpertProfile, FollowExpert, User, UserMedia


@admin.register(SessionPricing)
class SessionPricingAdmin(admin.ModelAdmin):
    """
    Admin class for Session Pricing Model.
    """
    list_display = ('id', 'session_length', 'price')


@admin.register(SessionRating)
class SessionRatingAdmin(admin.ModelAdmin):
    """
    Admin class for Session Rating Model.
    """
    list_display = ('session', 'overall_rating', 'knowledge_rating', 'communication_rating',
                    'professionalism_rating')
    list_display_links = ('session',)
    list_filter = ('overall_rating',)


@admin.register(EcDevice)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin class for EcDevice Model.
    """
    list_display = ('user', 'device_type', 'device_id', 'device_os', 'status')
    list_filter = ('device_type', 'device_sub_type', 'device_os', 'status')


@admin.register(EcSession)
class SessionAdmin(admin.ModelAdmin):
    """
    Admin class for EcSession Model.
    """
    list_display = ('user', 'expert', 'expert_profile', 'call_status')
    list_filter = ('call_status',)


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    """
    Admin class for Calendar Model.
    """
    list_display = ('expert', 'title', 'start_time', 'end_time')
    list_filter = ('expert', 'week_days')
    list_display_links = ('expert',)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """
    Admin class for Domain Model.
    """
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin class for Tag Model.
    """
    list_display = ('name', 'domain')
    list_filter = ('domain',)
    list_display_links = ('domain',)


@admin.register(DailyExpertStats)
class DailyExpertStatsAdmin(admin.ModelAdmin):
    """
    Admin class for DailyExpertStats Model.
    """
    list_display = ('expert', 'profile_visits', 'sessions_count', 'date')
    list_filter = ('expert', 'date')
    list_display_links = ('expert',)


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    """
    Admin class for Expert Model.
    """
    list_display = ('userbase', 'expert_uid', 'account_id', 'avg_rating', 'num_rating')
    list_display_links = ('userbase',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin class for User's Display Name Model.
    """
    list_display = ('userbase', 'display_name')
    list_display_links = ('userbase',)


@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    """
    Admin class for ExpertProfile Model.
    """
    list_display = ('expert', 'headline', 'year_of_experience')
    list_filter = ('year_of_experience',)
    list_display_links = ('expert',)


@admin.register(UserMedia)
class UserMediaAdmin(admin.ModelAdmin):
    """
    Admin class for UserMedia Model.
    """
    list_display = ('owner', 'profile', 'media_type', 'is_primary')
    list_filter = ('owner', 'profile', 'media_type', 'is_primary')
    list_display_links = ('owner', 'profile')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    """
    Admin class for PromoCode Model.
    """
    list_display = ('coupon_code', 'description', 'start_datetime', 'expiry_datetime',)
    list_filter = ('promo_code_type', 'value_type', 'start_datetime', 'expiry_datetime', 'usage_limit', 'status',
                   'is_deleted')


@admin.register(FollowExpert)
class FollowExpertAdmin(admin.ModelAdmin):
    """
    Admin class for FollowExpert Model.
    """
    list_display = ('expert', 'user', 'created_timestamp')
    list_filter = ('expert', 'user',)
    list_display_links = ('expert', 'user')
