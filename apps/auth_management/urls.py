from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.auth_management.views import UserListView, \
    UserDetailsView, GroupListView, OrganizationAddUsersView, \
    OrganizationRemoveUsersView, OrganizationViewSet


app_name = 'auth_management'
router = DefaultRouter()
router.register('organizations', OrganizationViewSet, 'organization')

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', UserListView.as_view(), name='list-users'),
    path('users/<pk>/', UserDetailsView.as_view(), name='detail-users'),
    path('groups/', GroupListView.as_view(), name='list-groups'),

    # path(
    #     'organizations/',
    #     OrganizationListCreateView.as_view(), name='list-create-organizations'
    # ),
    # path(
    #     'organizations/<pk>/users/',
    #     OrganizationAddUsersView.as_view(),
    #     name='create-organization-users'
    # ),
    # path(
    #     'organizations/<pk>/users/<user-pk>/',
    #     OrganizationRemoveUsersView.as_view(),
    #     name='remove-organization-users'
    # ),
]

urlpatterns += router.urls
