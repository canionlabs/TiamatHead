from django.contrib import admin

from apps.devices.models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'updated_at')
