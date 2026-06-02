from django.contrib import admin

from .models import ConnectionProfile


@admin.register(ConnectionProfile)
class ConnectionProfileAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'base_url',
        'role_header',
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