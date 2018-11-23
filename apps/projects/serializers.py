from rest_framework import serializers

from apps.projects.models import Project


class ProjectListSerializer(serializers.ModelSerializer):
    project_id = serializers.UUIDField()

    class Meta:
        model = Project
        fields = ("project_id", "organization", "name", "script")

    def get_project_id(self, obj):
        return obj.id


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "organization", "name", "script")

# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ("id", "organization", "name", "script")


class ProjectMinimalSerializer(serializers.ModelSerializer):
    organization = serializers.CharField()

    class Meta:
        model = Project
        fields = ("id", "organization", "name")

    def get_organization(self, obj):
        return obj.organization.name
