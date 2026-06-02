from rest_framework import serializers

from .models import ConnectionProfile


class ConnectionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionProfile
        fields = (
            'id',
            'name',
            'base_url',
            'role_header',
            'enabled',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )