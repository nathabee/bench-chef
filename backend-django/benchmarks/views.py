from rest_framework import viewsets

from .models import BenchmarkRun
from .serializers import BenchmarkRunSerializer


class BenchmarkRunViewSet(viewsets.ModelViewSet):
    queryset = BenchmarkRun.objects.all()
    serializer_class = BenchmarkRunSerializer