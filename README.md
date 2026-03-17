# Django Live Dashboard: Real Metrics + Open Connections

This repository contains two implementation branches for a real-time dashboard:

- `feature/ws-no-celery`: WebSockets with Django Channels group broadcast (Redis-backed channel layer).
- `feature/sse-no-celery`: SSE stream with plain Django `StreamingHttpResponse`.

The dashboard shows:

- `CPU %` from host (`psutil.cpu_percent`)
- `RAM %` from host (`psutil.virtual_memory().percent`)
- `Open WS/SSE connections` from server-side connection counters

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Run SSE branch

```bash
git checkout feature/sse-no-celery
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Run WebSocket branch

```bash
git checkout feature/ws-no-celery
docker run --rm -p 6379:6379 redis:7-alpine
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## What each branch demonstrates

### `feature/ws-no-celery`

- Channels group (`dashboard_metrics`) and `group_send` broadcast
- Redis channel layer
- Server push through WebSocket
- Per-connection `connect`/`disconnect` tracking
- Background async metrics publisher loop with 1-second interval

### `feature/sse-no-celery`

- Server push through SSE (`/events/`)
- Per-connection `open`/`close` tracking in stream generator
- Real metrics pushed every 1 second
- Browser auto-reconnect via `EventSource`

## WS vs SSE in this project

- Use **WebSockets** when you need bidirectional communication or richer realtime interactions.
- Use **SSE** when you only need server-to-client push and want a simpler transport.

Both branches intentionally avoid Celery and rely on server-side periodic loops.
