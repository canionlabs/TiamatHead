from django.contrib.auth.models import User

from rest_framework import serializers

from apps.devices.models import Device
from apps.projects.serializers import ProjectMinimalSerializer
from apps.auth_management.serializers import UserMinimalSerializer


class DeviceSerializer(serializers.ModelSerializer):
    device_id = serializers.UUIDField(source="id", format="hex_verbose", read_only=True)
    project = ProjectMinimalSerializer()

    class Meta:
        model = Device
        fields = ("device_id", "name", "project")
