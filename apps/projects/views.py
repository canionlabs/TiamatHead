from rest_framework import permissions
from rest_framework import viewsets

from django_filters import rest_framework as filters
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from apps.projects.filters import ProjectFilter
from apps.projects.permissions import IsOrganizationMember
from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [
        permissions.IsAuthenticated, TokenHasReadWriteScope,
        IsOrganizationMember
    ]
    filter_backends = [filters.DjangoFilterBackend, ]
    filterset_class = ProjectFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Project.objects.all()

        projects_map = map(
            lambda org: org.projects.all(), user.organizations.all())
        projects_map = list(projects_map)

        projects = Project.objects.none()
        org_projects = [projects_query for projects_query in projects_map]
        if org_projects:
            projects = projects | org_projects[0]
        return projects
