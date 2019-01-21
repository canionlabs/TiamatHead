from rest_framework import permissions


class IsOrganizationMember(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method == 'POST':
            org_id = request.data.get('organization_id')
            org_query = request.user.organizations.filter(id=org_id)
            return org_query.exists()
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.organization in request.user.organizations.all()
