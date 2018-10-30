from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from apps.auth_management.serializers import UserSerializer, GroupSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer