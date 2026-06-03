from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProbeSampleViewSet
from .views import metrics_view

router = DefaultRouter()

router.register(
    r'probe-samples',
    ProbeSampleViewSet,
    basename='probe-samples',
)

urlpatterns = [
    path(
        '',
        include(router.urls),
    ),

    path(
        'metrics',
        metrics_view,
        name='metrics',
    ),
]