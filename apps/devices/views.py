from rest_framework import generics, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from apps.devices.permissions import IsOwnerOrReadOnly
from apps.devices.models import Device
from apps.devices.serializers import DeviceSerializer


class DeviceListView(generics.ListCreateAPIView):
    """
    List devices related with users projects
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Device.objects.all()
        return Device.objects.filter(project__organization__users=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated, TokenHasReadWriteScope, IsOwnerOrReadOnly
    ]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
