from rest_framework import serializers

from apps.projects.models import Project
from apps.auth_management.models import Organization


class ProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.UUIDField(read_only=True)
    organization_id = serializers.UUIDField()

    class Meta:
        model = Project
        fields = ("project_id", "organization_id", "name", "script")
        read_only_fields = ("project_id",)

    def get_project_id(self, obj):
        return obj.id

    def get_organization_id(self, obj):
        return obj.organization.id

    def validate_organization_id(self, value):
        org_query = Organization.objects.filter(id=value)
        if org_query.exists():
            return value
        raise serializers.ValidationError("Must be a valid organization_id.")

    def create(self, validated_data):
        org_id = validated_data.pop('organization_id')
        org_instance = Organization.objects.get(id=org_id)
        instance = Project.objects.create(organization=org_instance, **validated_data)
        return instance


class ProjectMinimalSerializer(serializers.ModelSerializer):
    organization = serializers.CharField()

    class Meta:
        model = Project
        fields = ("id", "organization", "name")

    def get_organization(self, obj):
        return obj.organization.name
