from django_filters import rest_framework as filters

from apps.auth_management.models import Organization


class OrganizationFilter(filters.FilterSet):
    organization_id = filters.UUIDFilter(method='filter_organization_id')

    class Meta:
        model = Organization
        fields = ('organization_id', 'name')

    def filter_organization_id(self, queryset, name, value):
        if value:
            queryset = queryset.filter(id=value)
        return queryset
