from rest_framework import serializers

from .models import ProbeSample


class ProbeSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbeSample
        fields = (
            'id',
            'method',
            'url',
            'status_code',
            'latency_ms',
            'timed_out',
            'success',
            'error_message',
            'created_at',
        )
        read_only_fields = (
            'id',
            'created_at',
        )
