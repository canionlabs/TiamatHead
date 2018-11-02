from rest_framework import generics, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from apps.devices.permissions import IsOwnerOrReadOnly
from apps.devices.models import Device
from apps.devices.serializers import DeviceSerializer


class DeviceListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeviceDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated, TokenHasReadWriteScope, IsOwnerOrReadOnly
    ]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
