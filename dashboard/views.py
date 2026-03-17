import json
import time

from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import render

from .metrics import (
    collect_metrics,
    decrement_connections,
    get_open_connections,
    increment_connections,
)


def index(request):
    context = {
        "transport": settings.DASHBOARD_TRANSPORT,
        "interval_seconds": settings.METRICS_INTERVAL_SECONDS,
    }
    return render(request, "dashboard/index.html", context)


def metrics_events(request):
    def event_stream():
        increment_connections("sse")
        try:
            while True:
                payload = collect_metrics(open_connections=get_open_connections("sse"))
                yield f"data: {json.dumps(payload)}\n\n"
                time.sleep(settings.METRICS_INTERVAL_SECONDS)
        finally:
            decrement_connections("sse")

    response = StreamingHttpResponse(
        streaming_content=event_stream(),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
