# FastAPI Backend

FastAPI port of the original Flask leaderboard backend. The API paths, query parameters, and response bodies are intended to match the Flask backend.

## Run with Docker Compose

Create a local `.env` file from the FastAPI example file:

```bash
cp fastapi-backend/.env.example fastapi-backend/.env
```

Start the FastAPI backend on port `8000`:

```bash
docker compose -f docker-compose.fastapi.yml up --build
```

For local runs outside Docker Compose, the app also loads `fastapi-backend/.env`:

```bash
cd fastapi-backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Routes

- `GET /api/leaderboard/`
- `GET /api/leaderboard/profile/map/`
- `GET /api/leaderboard/profile/stats/`
- `GET /api/health`

The service reads PostgreSQL connection settings from:

- `WS_OSM_DB_HOST`
- `WS_OSM_DB_NAME`
- `WS_OSM_DB_USER`
- `WS_OSM_DB_PASS`
