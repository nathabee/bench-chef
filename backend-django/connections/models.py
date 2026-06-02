from django.db import models


class ConnectionProfile(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    base_url = models.URLField()

    role_header = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )

    enabled = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.name} ({self.base_url})'