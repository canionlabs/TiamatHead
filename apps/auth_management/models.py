from django.db import models
from django.contrib.auth.models import User

from apps.common.models import DefaultModel

import uuid


class Organization(DefaultModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False, verbose_name='Organization ID'
    )
    name = models.CharField(max_length=175)
    users = models.ManyToManyField(User, related_name='organizations')

    def __str__(self):
        return f'{self.name}'

    @property
    def organization_id(self):
        return self.id
