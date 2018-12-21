from django.contrib import admin
from apps.auth_management.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass
