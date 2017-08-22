from django.contrib import admin

from feeds.models import Content, ContentStats, ContentUserActivity, IgnoredContent, SocialAccount, SocialLink


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    """
    Admin class for SocialAccount Model
    """
    list_display = ('expert', 'access_token', 'provider', 'name',
                    'user_id', 'refresh_token', 'access_token_expiry_timestamp')
    list_display_links = ('expert', 'provider')
    list_filter = ('expert', 'provider')
    search_fields = ('expert', 'provider')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """
    Admin class for SocialLink model
    """
    list_display = ('account', 'feed_type', 'feed_sub_type', 'detail', 'display_name', )
    list_display_links = ('account', 'feed_type', )
    list_filter = ('account', 'expert_profiles', 'feed_type', 'feed_sub_type', )
    search_fields = ('account', 'expert_profiles', 'feed_type', 'feed_sub_type', )


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Admin class for Content Model
    """
    list_display = ('content_id', 'title', 'get_content_type_display', 'owner', 'is_deleted')
    list_display_links = ('content_id', 'owner',)
    list_filter = ('content_type', 'is_deleted')
    search_fields = ('content_id', 'title', 'owner__email', 'tags__name')


@admin.register(IgnoredContent)
class IgnoredContentAdmin(admin.ModelAdmin):
    """
    Admin class for IgnoredContent Model
    """
    list_display = ('content_id', 'expert')
    list_display_links = ('content_id', 'expert',)
    search_fields = ('content_id', 'expert__display_name')


@admin.register(ContentStats)
class ContentStatsAdmin(admin.ModelAdmin):
    """
    Admin class for ContentStats Model
    """
    list_display = ('content', 'likes')
    list_display_links = ('content',)
    search_fields = ('content__content_id', 'content__title')


@admin.register(ContentUserActivity)
class ContentUserActivityAdmin(admin.ModelAdmin):
    """
    Admin class for ContentUserActivity Model
    """
    list_display = ('id', 'content', 'user', 'activity_type')
    list_display_links = ('content',)
    list_filter = ('activity_type',)
    search_fields = ('content__content_id', 'content__title')
