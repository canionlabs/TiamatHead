from rest_framework import serializers

from apps.devices.models import Device
from django.contrib.auth.models import User


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "id")


class DeviceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    device_id = serializers.UUIDField(format="hex_verbose", read_only=True)

    class Meta:
        model = Device
        fields = ("name", "user", "device_id")

    def get_user(self, obj):
        return UserMinimalSerializer(obj.user).data