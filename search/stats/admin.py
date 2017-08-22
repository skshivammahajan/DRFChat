from django.contrib import admin

from stats.models import DailyStats, TagStats


@admin.register(TagStats)
class TagStatsAdmin(admin.ModelAdmin):
    """
    Admin class for TagStats model.
    """
    list_display = ('tag_id', 'total_search_count', 'last_week_search_count')
    list_display_links = ('tag_id',)
    # list_filter = ('device_type', 'device_os', 'status')


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    """
    Admin class for TagStats model.
    """
    list_display = ('tag_id', 'date', 'count')
    list_display_links = ('tag_id',)
