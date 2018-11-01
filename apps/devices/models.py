from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    name = models.CharField(max_length=75, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='devices'
    )
    device_id = models.CharField(max_length=275, verbose_name='Device ID')
    token = models.CharField(max_length=275)

    def __str__(self): 
        return f'{self.device_id or self.name}'
