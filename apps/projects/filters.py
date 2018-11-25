from django_filters import rest_framework as filters

from apps.projects.models import Project


class ProjectFilter(filters.FilterSet):
    project_id = filters.UUIDFilter(method='filter_project_id')

    class Meta:
        model = Project
        fields = ('project_id', 'name')

    def filter_project_id(self, queryset, name, value):
        if value:
            queryset = queryset.filter(id=value)
        return queryset
