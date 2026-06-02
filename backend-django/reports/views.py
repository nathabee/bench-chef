from rest_framework import viewsets

from .models import ReportRecord
from .serializers import ReportRecordSerializer


class ReportRecordViewSet(viewsets.ModelViewSet):
    queryset = ReportRecord.objects.all()
    serializer_class = ReportRecordSerializer