# Backend

```bash
pip install -r requirements.txt
flask --app main run --reload
```

Server runs at `http://localhost:8000`.

- `GET /health` — `{"status": "ok"}`
- `GET /ping` — `"Pong!"`
