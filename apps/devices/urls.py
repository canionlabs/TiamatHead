from django.urls import path, include

from apps.devices.views import DeviceListView, DeviceDetailView


app_name='devices'

urlpatterns = [
    path('devices/', DeviceListView.as_view(), name='list-devices'),
    path('devices/<pk>/', DeviceDetailView.as_view(), name='detail-devices')
]
