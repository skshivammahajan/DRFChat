from django.contrib import admin

from experchat_sessions.models import Session, SessionEvent


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """
    Admin class for Session Model.
    """
    list_display = ('user', 'expert_id', 'expert_profile_id',
                    'tokbox_session_length', 'scheduled_duration', 'start_timestamp', 'call_status')
    list_display_links = ('user', 'expert_id')
    list_filter = ('call_status',)


@admin.register(SessionEvent)
class SessionEventAdmin(admin.ModelAdmin):
    """
    Admin class for Session Model.
    """
    list_display = ('id', 'event', 'event_reason', 'session_id', 'connection_id')
