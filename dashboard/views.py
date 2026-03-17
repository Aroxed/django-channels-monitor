import json
import time

from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import render

from .metrics import collect_metrics, connections


def index(request):
    return render(request, "dashboard/index.html")


def metrics_events(request):
    def event_stream():
        connections.increment()
        try:
            while True:
                payload = collect_metrics(open_connections=connections.get())
                yield f"data: {json.dumps(payload)}\n\n"
                time.sleep(settings.METRICS_INTERVAL_SECONDS)
        finally:
            connections.decrement()

    response = StreamingHttpResponse(
        streaming_content=event_stream(),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
