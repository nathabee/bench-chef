from django.db import models


class ReportRecord(models.Model):
    class ReportType(models.TextChoices):
        BENCHMARK = 'BENCHMARK', 'Benchmark'
        PROBE = 'PROBE', 'Probe'
        SYSTEM = 'SYSTEM', 'System'
        SUMMARY = 'SUMMARY', 'Summary'

    class Status(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        GENERATING = 'GENERATING', 'Generating'
        READY = 'READY', 'Ready'
        FAILED = 'FAILED', 'Failed'

    class OutputFormat(models.TextChoices):
        JSON = 'JSON', 'JSON'
        CSV = 'CSV', 'CSV'
        MARKDOWN = 'MARKDOWN', 'Markdown'
        HTML = 'HTML', 'HTML'

    title = models.CharField(
        max_length=200,
    )

    report_type = models.CharField(
        max_length=30,
        choices=ReportType.choices,
        default=ReportType.BENCHMARK,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.CREATED,
    )

    output_format = models.CharField(
        max_length=30,
        choices=OutputFormat.choices,
        default=OutputFormat.JSON,
    )

    file_path = models.CharField(
        max_length=500,
        blank=True,
        default='',
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
        return f'{self.title} [{self.status}]'