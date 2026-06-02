from rest_framework.routers import DefaultRouter

from .views import ReportRecordViewSet

router = DefaultRouter()
router.register(r'report-records', ReportRecordViewSet, basename='report-record')

urlpatterns = router.urls