from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),

    path(
        'api/',
        include('connections.urls'),
    ),

    path(
        'api/',
        include('probes.urls'),
    ),

    path(
        'api/',
        include('benchmarks.urls'),
    ),

    path(
        'api/',
        include('reports.urls'),
    ),

    path(
        '',
        include('probes.urls'),
    ),
]