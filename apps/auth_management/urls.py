from django.urls import path, include

from apps.auth_management.views import UserListView, \
    UserDetailsView, GroupListView


app_name='auth_management'

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', UserListView.as_view(), name='list-users'),
    path('users/<pk>/', UserDetailsView.as_view(), name='detail-users'),
    path('groups/', GroupListView.as_view(), name='list-groups'),
]
