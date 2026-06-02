from django.contrib import admin
from django.urls import include, path

from health.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health', health_check, name='api-health'),
    path('api/', include('probes.urls')),
    path('api/', include('connections.urls')),
]