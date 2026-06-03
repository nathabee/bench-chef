from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from probes.models import ProbeSample

from .models import ConnectionProfile
from .serializers import ConnectionProfileSerializer
from .services import (
    ProbeResult,
    probe_camera_active_job,
    probe_camera_job_progress,
    probe_camera_job_timeline,
    probe_dashboard_index,
    probe_health,
    probe_monitoring,
    probe_version,
)


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

    def _probe_payload(
        self,
        probe_result: ProbeResult,
        probe_sample: ProbeSample,
    ) -> dict:
        return {
            'id': probe_sample.id,
            'method': probe_sample.method,
            'url': probe_sample.url,
            'status_code': probe_sample.status_code,
            'latency_ms': probe_sample.latency_ms,
            'timed_out': probe_sample.timed_out,
            'success': probe_sample.success,
            'error_message': probe_sample.error_message,
            'response_json': probe_result.response_json,
        }

    def _connection_payload(self, connection: ConnectionProfile) -> dict:
        return {
            'id': connection.id,
            'name': connection.name,
            'base_url': connection.base_url,
        }

    def _build_probe_response(
        self,
        connection: ConnectionProfile,
        probe_result: ProbeResult,
        probe_sample: ProbeSample,
    ) -> Response:
        return Response(
            {
                'connection': self._connection_payload(connection),
                'probe': self._probe_payload(
                    probe_result=probe_result,
                    probe_sample=probe_sample,
                ),
            },
            status=status.HTTP_200_OK,
        )

    def _run_and_store_probe(
        self,
        probe_function,
        connection: ConnectionProfile,
    ) -> tuple[ProbeResult, ProbeSample]:
        probe_result = probe_function(connection)
        probe_sample = self._store_probe_sample(probe_result)

        return probe_result, probe_sample

    def _missing_field_response(self, field_name: str) -> Response:
        return Response(
            {
                'error': f'Missing required field: {field_name}',
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _diagnostic_status(self, probe_results: list[ProbeResult]) -> str:
        success_count = sum(1 for result in probe_results if result.success)

        if success_count == len(probe_results):
            return 'ONLINE'

        if success_count == 0:
            return 'OFFLINE'

        return 'DEGRADED'

    @action(
        detail=True,
        methods=['post'],
        url_path='test-health',
    )
    def test_health(self, request, pk=None):
        connection = self.get_object()
        probe_result, probe_sample = self._run_and_store_probe(
            probe_function=probe_health,
            connection=connection,
        )

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
        probe_result, probe_sample = self._run_and_store_probe(
            probe_function=probe_version,
            connection=connection,
        )

        return self._build_probe_response(
            connection=connection,
            probe_result=probe_result,
            probe_sample=probe_sample,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='test-monitoring',
    )
    def test_monitoring(self, request, pk=None):
        connection = self.get_object()
        probe_result, probe_sample = self._run_and_store_probe(
            probe_function=probe_monitoring,
            connection=connection,
        )

        return self._build_probe_response(
            connection=connection,
            probe_result=probe_result,
            probe_sample=probe_sample,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='test-dashboard-index',
    )
    def test_dashboard_index(self, request, pk=None):
        connection = self.get_object()
        probe_result, probe_sample = self._run_and_store_probe(
            probe_function=probe_dashboard_index,
            connection=connection,
        )

        return self._build_probe_response(
            connection=connection,
            probe_result=probe_result,
            probe_sample=probe_sample,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='diagnostics',
    )
    def diagnostics(self, request, pk=None):
        connection = self.get_object()

        probe_definitions = (
            ('health', probe_health),
            ('version', probe_version),
            ('monitoring', probe_monitoring),
            ('dashboard_index', probe_dashboard_index),
        )

        probe_results = []
        probe_payloads = {}

        for probe_name, probe_function in probe_definitions:
            probe_result, probe_sample = self._run_and_store_probe(
                probe_function=probe_function,
                connection=connection,
            )
            probe_results.append(probe_result)
            probe_payloads[probe_name] = self._probe_payload(
                probe_result=probe_result,
                probe_sample=probe_sample,
            )

        return Response(
            {
                'connection': self._connection_payload(connection),
                'diagnostic_status': self._diagnostic_status(probe_results),
                'probes': probe_payloads,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='test-camera-active-job',
    )
    def test_camera_active_job(self, request, pk=None):
        printer_id = request.data.get('printer_id')
        if not printer_id:
            return self._missing_field_response('printer_id')

        connection = self.get_object()
        probe_result = probe_camera_active_job(
            connection=connection,
            printer_id=printer_id,
        )
        probe_sample = self._store_probe_sample(probe_result)

        return self._build_probe_response(
            connection=connection,
            probe_result=probe_result,
            probe_sample=probe_sample,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='test-camera-job-progress',
    )
    def test_camera_job_progress(self, request, pk=None):
        printer_id = request.data.get('printer_id')
        camera_job_id = request.data.get('camera_job_id')

        if not printer_id:
            return self._missing_field_response('printer_id')

        if not camera_job_id:
            return self._missing_field_response('camera_job_id')

        connection = self.get_object()
        probe_result = probe_camera_job_progress(
            connection=connection,
            printer_id=printer_id,
            camera_job_id=camera_job_id,
        )
        probe_sample = self._store_probe_sample(probe_result)

        return self._build_probe_response(
            connection=connection,
            probe_result=probe_result,
            probe_sample=probe_sample,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='test-camera-job-timeline',
    )
    def test_camera_job_timeline(self, request, pk=None):
        printer_id = request.data.get('printer_id')
        camera_job_id = request.data.get('camera_job_id')

        if not printer_id:
            return self._missing_field_response('printer_id')

        if not camera_job_id:
            return self._missing_field_response('camera_job_id')

        connection = self.get_object()
        probe_result = probe_camera_job_timeline(
            connection=connection,
            printer_id=printer_id,
            camera_job_id=camera_job_id,
        )
        probe_sample = self._store_probe_sample(probe_result)

        return self._build_probe_response(
            connection=connection,
            probe_result=probe_result,
            probe_sample=probe_sample,
        )
