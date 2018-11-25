from rest_framework import generics, permissions

from django_filters import rest_framework as filters
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from apps.projects.serializers import ProjectSerializer
from apps.projects.filters import ProjectFilter
from apps.projects.models import Project


class ProjectListCreateView(generics.ListCreateAPIView):
    """
    list:
    List related projects.

    create:
    Create a project for a related organization.
    """
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Project.objects.all()
        return user.projects.all()
