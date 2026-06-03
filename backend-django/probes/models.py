from django.db import models


class ProbeSample(models.Model):
    class ProbeType(models.TextChoices):
        HEALTH_PROBE = 'HEALTH_PROBE', 'Health probe'
        VERSION_PROBE = 'VERSION_PROBE', 'Version probe'
        MONITORING_PROBE = 'MONITORING_PROBE', 'Monitoring probe'
        DASHBOARD_ASSET_PROBE = 'DASHBOARD_ASSET_PROBE', 'Dashboard asset probe'
        CAMERA_JOB_ACTIVE_PROBE = 'CAMERA_JOB_ACTIVE_PROBE', 'Camera active job probe'
        CAMERA_JOB_PROGRESS_PROBE = 'CAMERA_JOB_PROGRESS_PROBE', 'Camera job progress probe'
        CAMERA_JOB_TIMELINE_PROBE = 'CAMERA_JOB_TIMELINE_PROBE', 'Camera job timeline probe'

    probe_type = models.CharField(
        max_length=50,
        choices=ProbeType.choices,
        default=ProbeType.HEALTH_PROBE,
    )

    connection_profile = models.ForeignKey(
        'connections.ConnectionProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='probe_samples',
    )

    benchmark_run = models.ForeignKey(
        'benchmarks.BenchmarkRun',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='probe_samples',
    )

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

    response_json = models.JSONField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.probe_type}: {self.method} {self.url} -> {self.status_code}'
