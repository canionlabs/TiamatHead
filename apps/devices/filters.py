from django_filters import rest_framework as filters

from apps.devices.models import Device


class DeviceFilter(filters.FilterSet):
    project_id = filters.UUIDFilter(method='filter_project_id')
    device_id = filters.UUIDFilter(method='filter_device_id')

    class Meta:
        model = Device
        fields = ('project_id', 'device_id', 'name')

    def filter_project_id(self, queryset, name, value):
        if value:
            queryset = queryset.filter(project__id=value)
        return queryset

    def filter_device_id(self, queryset, name, value):
        if value:
            queryset = queryset.filter(id=value)
        return queryset
