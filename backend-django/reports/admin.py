from django.contrib import admin

from .models import ReportRecord


@admin.register(ReportRecord)
class ReportRecordAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'report_type',
        'status',
        'output_format',
        'file_path',
        'created_at',
    )

    list_filter = (
        'report_type',
        'status',
        'output_format',
        'created_at',
    )

    search_fields = (
        'title',
        'file_path',
        'message',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )