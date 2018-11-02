from django.db import models
from django.contrib.auth.models import User

import uuid


class Device(models.Model):
    device_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False, verbose_name='Device ID'
    )
    name = models.CharField(max_length=75, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='devices'
    )

    def __str__(self):
        return f'{self.device_id}'