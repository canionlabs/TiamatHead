from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True

        return obj.user == request.user


class IsOrganizationMember(permissions.BasePermission):
    """
    Object-level permission to only allow organization members of an object to edit it.
    Assumes the model instance has an `project` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.project.organization in request.user.organizations.all()
