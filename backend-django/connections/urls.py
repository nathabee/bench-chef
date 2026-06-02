from rest_framework.routers import DefaultRouter

from .views import ConnectionProfileViewSet

router = DefaultRouter()
router.register(r'connections', ConnectionProfileViewSet, basename='connection-profile')

urlpatterns = router.urls