from statistics import mean

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ProbeSample
from .serializers import ProbeSampleSerializer


def percentile(values: list[int], percentile_value: float) -> int | None:
    if not values:
        return None

    ordered = sorted(values)
    index = round((len(ordered) - 1) * percentile_value)

    return ordered[index]


class ProbeSampleViewSet(viewsets.ModelViewSet):
    queryset = ProbeSample.objects.all()
    serializer_class = ProbeSampleSerializer

    def get_queryset(self):
        queryset = ProbeSample.objects.all()

        probe_type = self.request.query_params.get('probe_type')
        url = self.request.query_params.get('url')
        success = self.request.query_params.get('success')

        if probe_type:
            queryset = queryset.filter(probe_type=probe_type)

        if url:
            queryset = queryset.filter(url=url)

        if success is not None:
            if success.lower() == 'true':
                queryset = queryset.filter(success=True)
            elif success.lower() == 'false':
                queryset = queryset.filter(success=False)

        return queryset.order_by('-created_at')

    @action(
        detail=False,
        methods=['get'],
        url_path='latency-summary',
    )
    def latency_summary(self, request):
        queryset = self.get_queryset().exclude(latency_ms__isnull=True)

        values = list(queryset.values_list('latency_ms', flat=True))

        if not values:
            return Response(
                {
                    'count': 0,
                    'min_latency_ms': None,
                    'max_latency_ms': None,
                    'average_latency_ms': None,
                    'p50_latency_ms': None,
                    'p95_latency_ms': None,
                    'p99_latency_ms': None,
                }
            )

        return Response(
            {
                'count': len(values),
                'min_latency_ms': min(values),
                'max_latency_ms': max(values),
                'average_latency_ms': round(mean(values), 2),
                'p50_latency_ms': percentile(values, 0.50),
                'p95_latency_ms': percentile(values, 0.95),
                'p99_latency_ms': percentile(values, 0.99),
            }
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='error-summary',
    )
    def error_summary(self, request):
        queryset = self.get_queryset().filter(success=False)

        summary = {}

        for sample in queryset:
            key = sample.error_message or f'HTTP_STATUS_{sample.status_code}'
            summary[key] = summary.get(key, 0) + 1

        return Response(
            {
                'failure_count': queryset.count(),
                'errors': summary,
            }
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='slowdown-summary',
    )
    def slowdown_summary(self, request):
        queryset = self.get_queryset().exclude(latency_ms__isnull=True).order_by('created_at')
        samples = list(queryset)

        if len(samples) < 2:
            return Response(
                {
                    'sample_count': len(samples),
                    'trend': 'INSUFFICIENT_DATA',
                    'first_latency_ms': samples[0].latency_ms if samples else None,
                    'last_latency_ms': samples[-1].latency_ms if samples else None,
                    'delta_latency_ms': None,
                }
            )

        first_latency = samples[0].latency_ms
        last_latency = samples[-1].latency_ms
        delta = last_latency - first_latency

        if delta > 0:
            trend = 'SLOWER'
        elif delta < 0:
            trend = 'FASTER'
        else:
            trend = 'STABLE'

        return Response(
            {
                'sample_count': len(samples),
                'trend': trend,
                'first_latency_ms': first_latency,
                'last_latency_ms': last_latency,
                'delta_latency_ms': delta,
            }
        )
 