from rest_framework import serializers

from .models import BenchmarkRun


class BenchmarkRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenchmarkRun
        fields = (
            'id',
            'name',
            'scenario_name',
            'status',
            'target_base_url',
            'started_at',
            'finished_at',
            'message',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )