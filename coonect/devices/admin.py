from django.contrib import admin

from devices.models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin class for Device Model.
    """
    list_display = ('user', 'device_name', 'device_type', 'device_sub_type',
                    'device_id', 'device_os', 'status', 'device_token')
    list_display_links = ('user',)
    list_filter = ('device_type', 'device_os', 'status')
