from rest_framework import viewsets

from .models import ConnectionProfile
from .serializers import ConnectionProfileSerializer


class ConnectionProfileViewSet(viewsets.ModelViewSet):
    queryset = ConnectionProfile.objects.all().order_by('name')
    serializer_class = ConnectionProfileSerializer