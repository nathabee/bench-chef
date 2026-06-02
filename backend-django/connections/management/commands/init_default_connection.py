from django.core.management.base import BaseCommand

from connections.models import ConnectionProfile


class Command(BaseCommand):
    help = 'Create or update the default local SpaghettiChef connection profile.'

    def handle(self, *args, **options):
        profile, created = ConnectionProfile.objects.update_or_create(
            name='Local SpaghettiChef',
            defaults={
                'base_url': 'http://localhost:18080',
                'role_header': 'ADMIN',
                'enabled': True,
                'health_path': '/health',
                'version_path': '/version',
                'monitoring_path': '/monitoring',
                'dashboard_index_path': '/dashboard/index.html',
                'request_timeout_ms': 3000,
            },
        )

        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(
                f'{action} connection profile: {profile.name}'
            )
        )