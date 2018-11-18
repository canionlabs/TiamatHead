from rest_framework import serializers

from apps.projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "creator", "organization", "name", "script")


class ProjectMinimalSerializer(serializers.ModelSerializer):
    organization = serializers.CharField()

    class Meta:
        model = Project
        fields = ("id", "organization", "name")

    def get_organization(self, obj):
        return obj.organization.name
