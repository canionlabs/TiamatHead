from django.contrib.auth.models import User, Group

from rest_framework import serializers

from apps.auth_management.models import Organization


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "id")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )


class OrganizationSerializer(serializers.ModelSerializer):
    users = UserMinimalSerializer()

    class Meta:
        model = Organization
        fields = ('name', 'users')
