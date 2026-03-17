from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock

import psutil

_OPEN_CONNECTIONS = 0
_LOCK = Lock()

# Warm-up call prevents first CPU sample from being uninformative.
psutil.cpu_percent(interval=None)


def increment_connections() -> int:
    global _OPEN_CONNECTIONS
    with _LOCK:
        _OPEN_CONNECTIONS += 1
        return _OPEN_CONNECTIONS


def decrement_connections() -> int:
    global _OPEN_CONNECTIONS
    with _LOCK:
        _OPEN_CONNECTIONS = max(0, _OPEN_CONNECTIONS - 1)
        return _OPEN_CONNECTIONS


def get_open_connections() -> int:
    with _LOCK:
        return _OPEN_CONNECTIONS


def collect_metrics(open_connections: int) -> dict[str, float | int | str]:
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": psutil.virtual_memory().percent,
        "open_connections": open_connections,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
