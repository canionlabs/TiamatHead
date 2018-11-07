from django.db import models
from django.contrib.auth.models import User

from apps.common.models import DefaultModel
from apps.projects.models import Project

import uuid


class Device(DefaultModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False, verbose_name='Device ID'
    )
    name = models.CharField(max_length=75, null=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='devices'
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='devices'
    )

    def __str__(self):
        return f'{self.id}'