from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from probes.models import ProbeSample

from .models import ConnectionProfile
from .serializers import ConnectionProfileSerializer
from .services import ProbeResult, probe_health, probe_version


class ConnectionProfileViewSet(viewsets.ModelViewSet):
    queryset = ConnectionProfile.objects.all().order_by('name')
    serializer_class = ConnectionProfileSerializer

    def _store_probe_sample(self, probe_result: ProbeResult) -> ProbeSample:
        return ProbeSample.objects.create(
            method=probe_result.method,
            url=probe_result.url,
            status_code=probe_result.status_code,
            latency_ms=probe_result.latency_ms,
            timed_out=probe_result.timed_out,
            success=probe_result.success,
            error_message=probe_result.error_message,
        )

    def _build_probe_response(
        self,
        connection: ConnectionProfile,
        probe_result: ProbeResult,
        probe_sample: ProbeSample,
    ) -> Response:
        return Response(
            {
                'connection': {
                    'id': connection.id,
                    'name': connection.name,
                    'base_url': connection.base_url,
                },
                'probe': {
                    'id': probe_sample.id,
                    'method': probe_sample.method,
                    'url': probe_sample.url,
                    'status_code': probe_sample.status_code,
                    'latency_ms': probe_sample.latency_ms,
                    'timed_out': probe_sample.timed_out,
                    'success': probe_sample.success,
                    'error_message': probe_sample.error_message,
                    'response_json': probe_result.response_json,
                },
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='test-health',
    )
    def test_health(self, request, pk=None):
        connection = self.get_object()
        probe_result = probe_health(connection)
        probe_sample = self._store_probe_sample(probe_result)

        return self._build_probe_response(
            connection=connection,
            probe_result=probe_result,
            probe_sample=probe_sample,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='test-version',
    )
    def test_version(self, request, pk=None):
        connection = self.get_object()
        probe_result = probe_version(connection)
        probe_sample = self._store_probe_sample(probe_result)

        return self._build_probe_response(
            connection=connection,
            probe_result=probe_result,
            probe_sample=probe_sample,
        )
