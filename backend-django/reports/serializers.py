from rest_framework import serializers

from .models import ReportRecord


class ReportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRecord
        fields = (
            'id',
            'title',
            'report_type',
            'status',
            'output_format',
            'file_path',
            'message',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )