from django.contrib import admin

from .models import ConnectionProfile


@admin.register(ConnectionProfile)
class ConnectionProfileAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'base_url',
        'role_header',
        'health_path',
        'version_path',
        'monitoring_path',
        'dashboard_index_path',
        'request_timeout_ms',
        'enabled',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'enabled',
    )

    search_fields = (
        'name',
        'base_url',
    )

    fieldsets = (
        (
            'Connection',
            {
                'fields': (
                    'name',
                    'base_url',
                    'role_header',
                    'enabled',
                ),
            },
        ),
        (
            'Probe paths',
            {
                'fields': (
                    'health_path',
                    'version_path',
                    'monitoring_path',
                    'dashboard_index_path',
                ),
            },
        ),
        (
            'Timeout',
            {
                'fields': (
                    'request_timeout_ms',
                ),
            },
        ),
        (
            'Timestamps',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                ),
            },
        ),
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )