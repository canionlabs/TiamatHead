from django.contrib.auth.models import User

from rest_framework import serializers

from apps.devices.models import Device
from apps.projects.models import Project
from apps.projects.serializers import ProjectMinimalSerializer
from apps.auth_management.serializers import UserMinimalSerializer


class DeviceListSerializer(serializers.ModelSerializer):
    device_id = serializers.UUIDField(source="id", format="hex_verbose", read_only=True)
    project = ProjectMinimalSerializer()

    class Meta:
        model = Device
        fields = ("device_id", "name", "project")


class DeviceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("device_id", "name", "project")

    def create(self, validated_data):
        project = validated_data.pop('project')
        instance = Device.objects.create(project=project, **validated_data)
        if project:
            instance.project = project

        return instance
