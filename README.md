# Agentic RAG Knowledge Assistant

Production-oriented knowledge assistant: authenticated users upload documents, an agent decides when to retrieve, and answers are grounded in cited sources.

This repository is a monorepo (`backend/`, `frontend/`, `docs/`). Implementation follows `TODO.md` one phase at a time. Phase 1 is project initialization only.

## Local setup

Copy environment variables, then start Postgres and Redis:

```bash
cp .env.example .env
docker compose up postgres redis -d
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements-dev.txt
pytest
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check: `http://localhost:8000/health`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: `http://localhost:5173`

### Full stack

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`
- Postgres: `localhost:5433` (pgvector image; host port 5433 avoids clashes with other local Postgres instances)
- Redis: `localhost:6379`

Never commit `.env` or API keys.

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Security](docs/security.md)
- [RAG pipeline](docs/rag-pipeline.md)
- [Agent](docs/agent.md)
- [Implementation TODOs](TODO.md)
