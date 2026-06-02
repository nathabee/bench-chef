from django.db import models


class BenchmarkRun(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        QUEUED = 'QUEUED', 'Queued'
        RUNNING = 'RUNNING', 'Running'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    name = models.CharField(
        max_length=150,
    )

    scenario_name = models.CharField(
        max_length=150,
        blank=True,
        default='',
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )

    target_base_url = models.URLField(
        blank=True,
        default='',
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    message = models.TextField(
        blank=True,
        default='',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} [{self.status}]'