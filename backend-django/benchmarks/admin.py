from django.contrib import admin

from .models import BenchmarkRun


@admin.register(BenchmarkRun)
class BenchmarkRunAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'scenario_name',
        'status',
        'target_base_url',
        'started_at',
        'finished_at',
        'created_at',
    )

    list_filter = (
        'status',
        'scenario_name',
        'created_at',
    )

    search_fields = (
        'name',
        'scenario_name',
        'target_base_url',
        'message',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )