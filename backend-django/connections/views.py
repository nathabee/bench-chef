import time

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from benchmarks.models import BenchmarkRun
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

    def _store_probe_sample(
        self,
        connection: ConnectionProfile,
        probe_result: ProbeResult,
        probe_type: str,
        benchmark_run: BenchmarkRun | None = None,
    ) -> ProbeSample:
        return ProbeSample.objects.create(
            probe_type=probe_type,
            connection_profile=connection,
            benchmark_run=benchmark_run,
            method=probe_result.method,
            url=probe_result.url,
            status_code=probe_result.status_code,
            latency_ms=probe_result.latency_ms,
            timed_out=probe_result.timed_out,
            success=probe_result.success,
            error_message=probe_result.error_message,
            response_json=probe_result.response_json,
        )

    def _probe_payload(
        self,
        probe_result: ProbeResult,
        probe_sample: ProbeSample,
    ) -> dict:
        return {
            'id': probe_sample.id,
            'probe_type': probe_sample.probe_type,
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

    def _probe_function_for_type(self, probe_type: str):
        mapping = {
            ProbeSample.ProbeType.HEALTH_PROBE: probe_health,
            ProbeSample.ProbeType.VERSION_PROBE: probe_version,
            ProbeSample.ProbeType.MONITORING_PROBE: probe_monitoring,
            ProbeSample.ProbeType.DASHBOARD_ASSET_PROBE: probe_dashboard_index,
        }

        return mapping.get(probe_type)

    def _latency_summary(self, samples: list[ProbeSample]) -> dict:
        values = [
            sample.latency_ms
            for sample in samples
            if sample.latency_ms is not None
        ]

        if not values:
            return {
                'count': len(samples),
                'min_latency_ms': None,
                'max_latency_ms': None,
                'average_latency_ms': None,
            }

        return {
            'count': len(samples),
            'min_latency_ms': min(values),
            'max_latency_ms': max(values),
            'average_latency_ms': round(sum(values) / len(values), 2),
        }

    @action(
        detail=True,
        methods=['post'],
        url_path='test-health',
    )
    def test_health(self, request, pk=None):
        connection = self.get_object()
        probe_result = probe_health(connection)
        probe_sample = self._store_probe_sample(
            connection=connection,
            probe_result=probe_result,
            probe_type=ProbeSample.ProbeType.HEALTH_PROBE,
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
        probe_result = probe_version(connection)
        probe_sample = self._store_probe_sample(
            connection=connection,
            probe_result=probe_result,
            probe_type=ProbeSample.ProbeType.VERSION_PROBE,
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
        probe_result = probe_monitoring(connection)
        probe_sample = self._store_probe_sample(
            connection=connection,
            probe_result=probe_result,
            probe_type=ProbeSample.ProbeType.MONITORING_PROBE,
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
        probe_result = probe_dashboard_index(connection)
        probe_sample = self._store_probe_sample(
            connection=connection,
            probe_result=probe_result,
            probe_type=ProbeSample.ProbeType.DASHBOARD_ASSET_PROBE,
        )

        return self._build_probe_response(
            connection=connection,
            probe_result=probe_result,
            probe_sample=probe_sample,
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
        probe_sample = self._store_probe_sample(
            connection=connection,
            probe_result=probe_result,
            probe_type=ProbeSample.ProbeType.CAMERA_JOB_ACTIVE_PROBE,
        )

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
        probe_sample = self._store_probe_sample(
            connection=connection,
            probe_result=probe_result,
            probe_type=ProbeSample.ProbeType.CAMERA_JOB_PROGRESS_PROBE,
        )

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
        probe_sample = self._store_probe_sample(
            connection=connection,
            probe_result=probe_result,
            probe_type=ProbeSample.ProbeType.CAMERA_JOB_TIMELINE_PROBE,
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
            ('health', ProbeSample.ProbeType.HEALTH_PROBE, probe_health),
            ('version', ProbeSample.ProbeType.VERSION_PROBE, probe_version),
            ('monitoring', ProbeSample.ProbeType.MONITORING_PROBE, probe_monitoring),
            ('dashboard_index', ProbeSample.ProbeType.DASHBOARD_ASSET_PROBE, probe_dashboard_index),
        )

        probe_results = []
        probe_payloads = {}

        for probe_name, probe_type, probe_function in probe_definitions:
            probe_result = probe_function(connection)
            probe_sample = self._store_probe_sample(
                connection=connection,
                probe_result=probe_result,
                probe_type=probe_type,
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
        url_path='repeat-probe',
    )
    def repeat_probe(self, request, pk=None):
        connection = self.get_object()

        probe_type = request.data.get('probe_type')
        repeat_count = int(request.data.get('repeat_count', 5))
        delay_ms = int(request.data.get('delay_ms', 0))

        if repeat_count < 1:
            return Response(
                {'error': 'repeat_count must be >= 1'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        probe_function = self._probe_function_for_type(probe_type)
        if probe_function is None:
            return Response(
                {
                    'error': 'Unsupported probe_type for repeat-probe',
                    'supported_probe_types': [
                        ProbeSample.ProbeType.HEALTH_PROBE,
                        ProbeSample.ProbeType.VERSION_PROBE,
                        ProbeSample.ProbeType.MONITORING_PROBE,
                        ProbeSample.ProbeType.DASHBOARD_ASSET_PROBE,
                    ],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        samples = []
        payloads = []

        for index in range(repeat_count):
            if index > 0 and delay_ms > 0:
                time.sleep(delay_ms / 1000)

            probe_result = probe_function(connection)
            probe_sample = self._store_probe_sample(
                connection=connection,
                probe_result=probe_result,
                probe_type=probe_type,
            )
            samples.append(probe_sample)
            payloads.append(
                self._probe_payload(
                    probe_result=probe_result,
                    probe_sample=probe_sample,
                )
            )

        success_count = sum(1 for sample in samples if sample.success)
        failure_count = len(samples) - success_count

        return Response(
            {
                'connection': self._connection_payload(connection),
                'probe_type': probe_type,
                'repeat_count': repeat_count,
                'delay_ms': delay_ms,
                'success_count': success_count,
                'failure_count': failure_count,
                'latency': self._latency_summary(samples),
                'samples': payloads,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='diagnostics-history',
    )
    def diagnostics_history(self, request, pk=None):
        connection = self.get_object()

        repeat_count = int(request.data.get('repeat_count', 3))
        delay_ms = int(request.data.get('delay_ms', 0))

        if repeat_count < 1:
            return Response(
                {'error': 'repeat_count must be >= 1'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        benchmark_run = BenchmarkRun.objects.create(
            name=f'Diagnostics history for {connection.name}',
            scenario_name='DIAGNOSTICS_HISTORY',
            status=BenchmarkRun.Status.COMPLETED,
            target_base_url=connection.base_url,
            message='Diagnostics history run created by BenchChef.',
        )

        status_counts = {
            'ONLINE': 0,
            'DEGRADED': 0,
            'OFFLINE': 0,
        }

        all_samples = []

        for iteration in range(repeat_count):
            if iteration > 0 and delay_ms > 0:
                time.sleep(delay_ms / 1000)

            probe_definitions = (
                (ProbeSample.ProbeType.HEALTH_PROBE, probe_health),
                (ProbeSample.ProbeType.VERSION_PROBE, probe_version),
                (ProbeSample.ProbeType.MONITORING_PROBE, probe_monitoring),
                (ProbeSample.ProbeType.DASHBOARD_ASSET_PROBE, probe_dashboard_index),
            )

            probe_results = []

            for probe_type, probe_function in probe_definitions:
                probe_result = probe_function(connection)
                probe_sample = self._store_probe_sample(
                    connection=connection,
                    probe_result=probe_result,
                    probe_type=probe_type,
                    benchmark_run=benchmark_run,
                )
                probe_results.append(probe_result)
                all_samples.append(probe_sample)

            diagnostic_status = self._diagnostic_status(probe_results)
            status_counts[diagnostic_status] += 1

        return Response(
            {
                'connection': self._connection_payload(connection),
                'benchmark_run': {
                    'id': benchmark_run.id,
                    'name': benchmark_run.name,
                    'scenario_name': benchmark_run.scenario_name,
                    'status': benchmark_run.status,
                },
                'repeat_count': repeat_count,
                'delay_ms': delay_ms,
                'diagnostic_status_counts': status_counts,
                'latency': self._latency_summary(all_samples),
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='dashboard-responsiveness',
    )
    def dashboard_responsiveness(self, request, pk=None):
        connection = self.get_object()

        repeat_count = int(request.data.get('repeat_count', 10))
        delay_ms = int(request.data.get('delay_ms', 0))

        if repeat_count < 1:
            return Response(
                {'error': 'repeat_count must be >= 1'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        samples = []

        for index in range(repeat_count):
            if index > 0 and delay_ms > 0:
                time.sleep(delay_ms / 1000)

            probe_result = probe_dashboard_index(connection)
            probe_sample = self._store_probe_sample(
                connection=connection,
                probe_result=probe_result,
                probe_type=ProbeSample.ProbeType.DASHBOARD_ASSET_PROBE,
            )
            samples.append(probe_sample)

        success_count = sum(1 for sample in samples if sample.success)

        return Response(
            {
                'connection': self._connection_payload(connection),
                'repeat_count': repeat_count,
                'delay_ms': delay_ms,
                'success_count': success_count,
                'failure_count': len(samples) - success_count,
                'success_rate': round(success_count / len(samples), 4),
                'latency': self._latency_summary(samples),
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='camera-active-job-polling',
    )
    def camera_active_job_polling(self, request, pk=None):
        printer_id = request.data.get('printer_id')
        if not printer_id:
            return self._missing_field_response('printer_id')

        connection = self.get_object()

        repeat_count = int(request.data.get('repeat_count', 10))
        delay_ms = int(request.data.get('delay_ms', 1000))

        if repeat_count < 1:
            return Response(
                {'error': 'repeat_count must be >= 1'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        samples = []
        snapshot_points = []

        for index in range(repeat_count):
            if index > 0 and delay_ms > 0:
                time.sleep(delay_ms / 1000)

            probe_result = probe_camera_active_job(
                connection=connection,
                printer_id=printer_id,
            )
            probe_sample = self._store_probe_sample(
                connection=connection,
                probe_result=probe_result,
                probe_type=ProbeSample.ProbeType.CAMERA_JOB_ACTIVE_PROBE,
            )
            samples.append(probe_sample)

            response_json = probe_result.response_json
            if isinstance(response_json, dict):
                latest_snapshot_id = response_json.get('latestSnapshotId')
                latest_capture_at = response_json.get('latestCaptureAt')

                snapshot_points.append(
                    {
                        'sample_id': probe_sample.id,
                        'latestSnapshotId': latest_snapshot_id,
                        'latestCaptureAt': latest_capture_at,
                    }
                )

        success_count = sum(1 for sample in samples if sample.success)

        return Response(
            {
                'connection': self._connection_payload(connection),
                'printer_id': printer_id,
                'repeat_count': repeat_count,
                'delay_ms': delay_ms,
                'success_count': success_count,
                'failure_count': len(samples) - success_count,
                'latency': self._latency_summary(samples),
                'snapshot_points': snapshot_points,
            },
            status=status.HTTP_200_OK,
        )
 