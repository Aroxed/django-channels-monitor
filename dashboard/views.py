from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import render


def index(request):
    context = {
        "transport": settings.DASHBOARD_TRANSPORT,
        "interval_seconds": settings.METRICS_INTERVAL_SECONDS,
    }
    return render(request, "dashboard/index.html", context)


def metrics_events(request):
    return HttpResponseNotFound("SSE endpoint is enabled only in SSE branch.")
