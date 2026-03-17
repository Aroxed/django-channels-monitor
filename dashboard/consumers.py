import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.conf import settings

from .metrics import collect_metrics, decrement_connections, get_open_connections, increment_connections

GROUP_NAME = "dashboard_metrics"
_publisher_task: asyncio.Task | None = None
_publisher_lock = asyncio.Lock()
_stop_publisher = asyncio.Event()


async def ensure_metrics_publisher_running():
    global _publisher_task
    async with _publisher_lock:
        should_start = _publisher_task is None or _publisher_task.done()
        if should_start:
            _stop_publisher.clear()
            _publisher_task = asyncio.create_task(metrics_publisher_loop())


async def stop_metrics_publisher_if_idle():
    if get_open_connections("ws") > 0:
        return
    _stop_publisher.set()


async def metrics_publisher_loop():
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    while not _stop_publisher.is_set():
        payload = collect_metrics(open_connections=get_open_connections("ws"))
        await channel_layer.group_send(
            GROUP_NAME,
            {
                "type": "metrics.update",
                "payload": payload,
            },
        )
        await asyncio.sleep(settings.METRICS_INTERVAL_SECONDS)


class MetricsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(GROUP_NAME, self.channel_name)
        await self.accept()

        increment_connections("ws")
        await ensure_metrics_publisher_running()

        await self.send_json(
            collect_metrics(open_connections=get_open_connections("ws"))
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(GROUP_NAME, self.channel_name)
        decrement_connections("ws")
        await stop_metrics_publisher_if_idle()

    async def metrics_update(self, event):
        await self.send_json(event["payload"])
