from django.contrib import admin

from users.models import ExpertAccount, FollowTags


@admin.register(ExpertAccount)
class ExpertAccountAdmin(admin.ModelAdmin):
    """
    Admin class for Expert's Bank Account
    """
    list_display = ('expert', 'account_name', 'account_number', 'routing_number', 'is_active')
    list_display_links = ('expert',)
    list_filter = ('expert', 'is_active')


@admin.register(FollowTags)
class FollowTagsAdmin(admin.ModelAdmin):
    """
    Admin class for Tags followed by User
    """
    list_display = ('user', 'tag')
    list_display_links = ('tag',)
    list_filter = ('user', 'tag')
