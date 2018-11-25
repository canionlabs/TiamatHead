from django.urls import path

from apps.devices.views import DeviceListCreateView, DeviceDetailView


app_name='devices'

urlpatterns = [
    path('devices/', DeviceListCreateView.as_view(), name='list-create-devices'),
    path('devices/<pk>/', DeviceDetailView.as_view(), name='detail-devices')
]
