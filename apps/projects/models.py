from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from apps.common.models import DefaultModel
from apps.auth_management.models import Organization

import uuid


class Project(DefaultModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name='Project ID'
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='projects_father'
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='projects'
    )
    name = models.CharField(max_length=175)
    script = JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.id}'
