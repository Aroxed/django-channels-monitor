from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock

import psutil

# Warm-up call prevents first CPU sample from being uninformative.
psutil.cpu_percent(interval=None)


class ConnectionCounter:
    def __init__(self) -> None:
        self._value = 0
        self._lock = Lock()

    def increment(self) -> int:
        with self._lock:
            self._value += 1
            return self._value

    def decrement(self) -> int:
        with self._lock:
            self._value = max(0, self._value - 1)
            return self._value

    def get(self) -> int:
        with self._lock:
            return self._value


connections = ConnectionCounter()


def collect_metrics(open_connections: int) -> dict[str, float | int | str]:
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": psutil.virtual_memory().percent,
        "open_connections": open_connections,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
