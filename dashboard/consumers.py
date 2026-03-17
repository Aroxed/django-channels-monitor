import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

from .metrics import collect_metrics, decrement_connections, get_open_connections, increment_connections


class MetricsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        increment_connections()
        self.push_task = asyncio.create_task(self.push_loop())

    async def disconnect(self, close_code):
        decrement_connections()
        if hasattr(self, "push_task"):
            self.push_task.cancel()

    async def push_loop(self):
        try:
            while True:
                payload = collect_metrics(open_connections=get_open_connections())
                await self.send_json(payload)
                await asyncio.sleep(settings.METRICS_INTERVAL_SECONDS)
        except asyncio.CancelledError:
            return
