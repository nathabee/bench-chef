from rest_framework.routers import DefaultRouter

from .views import BenchmarkRunViewSet

router = DefaultRouter()
router.register(r'benchmark-runs', BenchmarkRunViewSet, basename='benchmark-run')

urlpatterns = router.urls