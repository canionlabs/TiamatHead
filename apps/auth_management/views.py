from django.contrib.auth.models import User, Group

from rest_framework.response import Response
from rest_framework import generics, permissions, status
from django_filters import rest_framework as filters
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from apps.auth_management.models import Organization
from apps.auth_management.serializers import UserSerializer, \
    GroupSerializer, OrganizationSerializer, OrganizationUserSerializer


class UserListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser, TokenHasReadWriteScope]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class OrganizationAddUsersView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = OrganizationUserSerializer


class OrganizationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = OrganizationSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Organization.objects.all()
        return user.organizations.all()
