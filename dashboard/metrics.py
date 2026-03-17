from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock

import psutil


@dataclass
class ConnectionCounters:
    ws: int = 0
    sse: int = 0


_COUNTERS = ConnectionCounters()
_LOCK = Lock()

# Warm-up call prevents first CPU sample from being uninformative.
psutil.cpu_percent(interval=None)


def increment_connections(kind: str) -> int:
    with _LOCK:
        if kind == "ws":
            _COUNTERS.ws += 1
            return _COUNTERS.ws
        if kind == "sse":
            _COUNTERS.sse += 1
            return _COUNTERS.sse
        raise ValueError(f"Unknown connection kind: {kind}")


def decrement_connections(kind: str) -> int:
    with _LOCK:
        if kind == "ws":
            _COUNTERS.ws = max(0, _COUNTERS.ws - 1)
            return _COUNTERS.ws
        if kind == "sse":
            _COUNTERS.sse = max(0, _COUNTERS.sse - 1)
            return _COUNTERS.sse
        raise ValueError(f"Unknown connection kind: {kind}")


def get_open_connections(kind: str) -> int:
    with _LOCK:
        if kind == "ws":
            return _COUNTERS.ws
        if kind == "sse":
            return _COUNTERS.sse
        raise ValueError(f"Unknown connection kind: {kind}")


def collect_metrics(open_connections: int) -> dict[str, float | int | str]:
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": psutil.virtual_memory().percent,
        "open_connections": open_connections,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
