from django.contrib import admin

from .models import ProbeSample


@admin.register(ProbeSample)
class ProbeSampleAdmin(admin.ModelAdmin):
    list_display = (
        'method',
        'url',
        'status_code',
        'latency_ms',
        'timed_out',
        'success',
        'created_at',
    )

    list_filter = (
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
