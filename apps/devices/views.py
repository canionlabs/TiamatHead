from rest_framework import generics, permissions

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django_filters import rest_framework as filters

from apps.devices.permissions import IsOwnerOrReadOnly, IsOrganizationMember
from apps.devices.filters import DeviceFilter
from apps.devices.models import Device
from apps.devices.serializers import (
    DeviceListSerializer, DeviceCreateSerializer)


class DeviceListCreateView(generics.ListCreateAPIView):
    """
    list:
    List related devices

    create:
    Create devices for new projects or existing projects related with the user
    """
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DeviceFilter
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = DeviceCreateSerializer

    def get_read_serializer_class(self):
        if self.request.method == 'GET':
            return DeviceListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Device.objects.all()
        return Device.objects.filter(project__organization__users=user)


class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve devices related with users organization
    """
    permission_classes = [
        permissions.IsAuthenticated, 
        TokenHasReadWriteScope, IsOrganizationMember
    ]
    queryset = Device.objects.all()
    serializer_class = DeviceListSerializer
