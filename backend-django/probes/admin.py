from django.contrib import admin

from .models import ProbeSample


@admin.register(ProbeSample)
class ProbeSampleAdmin(admin.ModelAdmin):
    list_display = (
        'probe_type',
        'connection_profile',
        'benchmark_run',
        'method',
        'url',
        'status_code',
        'latency_ms',
        'timed_out',
        'success',
        'created_at',
    )

    list_filter = (
        'probe_type',
        'method',
        'status_code',
        'timed_out',
        'success',
        'created_at',
    )

    search_fields = (
        'url',
        'error_message',
    )

    readonly_fields = (
        'created_at',
    )
