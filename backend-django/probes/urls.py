from rest_framework.routers import DefaultRouter

from .views import ProbeSampleViewSet

router = DefaultRouter()
router.register(r'probe-samples', ProbeSampleViewSet, basename='probe-sample')

urlpatterns = router.urls