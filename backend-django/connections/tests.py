from unittest.mock import Mock, patch

from django.test import TestCase

from .models import ConnectionProfile
from .services import probe_health


class ProbeServiceTests(TestCase):
    def test_probe_uses_spaghettichef_role_header(self):
        connection = ConnectionProfile.objects.create(
            name='Local SpaghettiChef',
            base_url='http://localhost:18080',
            role_header='ADMIN',
        )

        response = Mock()
        response.status_code = 200
        response.json.return_value = {'status': 'ok'}

        with patch('connections.services.requests.get', return_value=response) as get:
            result = probe_health(connection)

        self.assertTrue(result.success)
        get.assert_called_once_with(
            'http://localhost:18080/health',
            headers={'X-SpaghettiChef-Role': 'ADMIN'},
            timeout=3.0,
        )
