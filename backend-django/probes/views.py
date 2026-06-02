from rest_framework import viewsets

from .models import ProbeSample
from .serializers import ProbeSampleSerializer


class ProbeSampleViewSet(viewsets.ModelViewSet):
    queryset = ProbeSample.objects.all()
    serializer_class = ProbeSampleSerializer