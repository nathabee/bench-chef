from prometheus_client import CollectorRegistry
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram
from prometheus_client import generate_latest

from .models import ProbeSample


def build_metrics_payload() -> bytes:
    registry = CollectorRegistry()

    probe_requests_total = Counter(
        'benchchef_probe_requests_total',
        'Total BenchChef probe requests',
        [
            'probe_type',
            'connection_name',
            'success',
        ],
        registry=registry,
    )

    probe_failures_total = Counter(
        'benchchef_probe_failures_total',
        'Total BenchChef probe failures',
        [
            'probe_type',
            'connection_name',
        ],
        registry=registry,
    )

    probe_timeout_total = Counter(
        'benchchef_probe_timeout_total',
        'Total BenchChef probe timeouts',
        [
            'probe_type',
            'connection_name',
        ],
        registry=registry,
    )

    probe_http_status_total = Counter(
        'benchchef_probe_http_status_total',
        'Total BenchChef HTTP status codes',
        [
            'probe_type',
            'connection_name',
            'status_code',
        ],
        registry=registry,
    )

    probe_duration_seconds = Histogram(
        'benchchef_probe_duration_seconds',
        'BenchChef probe duration',
        [
            'probe_type',
            'connection_name',
        ],
        registry=registry,
    )

    spaghettichef_up = Gauge(
        'benchchef_spaghettichef_up',
        'Latest SpaghettiChef health status',
        [
            'connection_name',
            'base_url',
        ],
        registry=registry,
    )

    queryset = ProbeSample.objects.select_related(
        'connection_profile',
    )

    for sample in queryset:

        connection_name = (
            sample.connection_profile.name
            if sample.connection_profile
            else 'unknown'
        )

        base_url = (
            sample.connection_profile.base_url
            if sample.connection_profile
            else 'unknown'
        )

        probe_requests_total.labels(
            probe_type=sample.probe_type,
            connection_name=connection_name,
            success=str(sample.success).lower(),
        ).inc()

        if not sample.success:
            probe_failures_total.labels(
                probe_type=sample.probe_type,
                connection_name=connection_name,
            ).inc()

        if sample.timed_out:
            probe_timeout_total.labels(
                probe_type=sample.probe_type,
                connection_name=connection_name,
            ).inc()

        if sample.status_code is not None:
            probe_http_status_total.labels(
                probe_type=sample.probe_type,
                connection_name=connection_name,
                status_code=str(sample.status_code),
            ).inc()

        if sample.latency_ms is not None:
            probe_duration_seconds.labels(
                probe_type=sample.probe_type,
                connection_name=connection_name,
            ).observe(
                sample.latency_ms / 1000,
            )

    health_samples = (
        ProbeSample.objects
        .filter(
            probe_type=ProbeSample.ProbeType.HEALTH_PROBE,
        )
        .select_related(
            'connection_profile',
        )
        .order_by(
            'connection_profile_id',
            '-created_at',
        )
    )

    processed_connections = set()

    for sample in health_samples:

        if not sample.connection_profile:
            continue

        connection_id = sample.connection_profile.id

        if connection_id in processed_connections:
            continue

        processed_connections.add(connection_id)

        spaghettichef_up.labels(
            connection_name=sample.connection_profile.name,
            base_url=sample.connection_profile.base_url,
        ).set(
            1 if sample.success else 0,
        )

    return generate_latest(registry)