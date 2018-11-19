from rest_framework import generics, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from apps.devices.permissions import IsOwnerOrReadOnly, IsOrganizationMember
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
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = DeviceCreateSerializer

    def get_read_serializer_class(self):
        if self.request.method == 'GET':
            return DeviceListSerializer

    def check_params(self):
        formated_params = {}

        # valid_params = {'API Param Name': 'Model Field Reference'}
        valid_params = {
            'project_id': 'project__id'
        }
        query_params = self.request.query_params

        for valid_key, field_ref in valid_params.items():
            param = query_params.get(valid_key, None)
            if param:
                formated_params.update({field_ref: param})
        return formated_params

    def get_queryset(self):
        user = self.request.user
        params = self.check_params()

        if user.is_superuser:
            return Device.objects.filter(**params)

        return Device.objects.filter(
            project__organization__users=user, **params
        )


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
