from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="dashboard-index"),
    path("events/", views.metrics_events, name="dashboard-events"),
]
