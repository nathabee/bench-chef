from django.db import models


class ProbeSample(models.Model):
    method = models.CharField(
        max_length=10,
        default='GET',
    )

    url = models.URLField()

    status_code = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    latency_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    timed_out = models.BooleanField(
        default=False,
    )

    success = models.BooleanField(
        default=False,
    )

    error_message = models.TextField(
        blank=True,
        default='',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.method} {self.url} -> {self.status_code}'