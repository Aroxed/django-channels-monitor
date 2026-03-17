# Django Live Dashboard (WebSocket branch)

Simple example of realtime metrics over WebSocket.

## Metrics

- `CPU %` from `psutil.cpu_percent`
- `RAM %` from `psutil.virtual_memory().percent`
- `Open WebSocket connections` from in-memory counter

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open <http://127.0.0.1:8000/>.
