# Agentic RAG Knowledge Assistant

Production-oriented knowledge assistant: authenticated users upload documents, an agent decides when to retrieve, and answers are grounded in cited sources.

This repository is a monorepo (`backend/`, `frontend/`, `docs/`). Implementation follows `TODO.md` one phase at a time.

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
alembic upgrade head
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

## Git hooks

Husky runs the same local checks CI uses so broken lint or tests fail before they reach GitHub.

From the **repository root** (not `frontend/`):

```bash
npm install
```

That installs:

- **pre-commit** — Ruff lint/format on staged Python files; frontend `tsc` when TypeScript files are staged
- **pre-push** — full backend Ruff check, `pytest`, and frontend production build

Python tools run from `backend/.venv` when that virtualenv exists. Integration tests skip if Postgres is not up (`docker compose up postgres -d`). Skip a hook once with `git commit --no-verify` or `HUSKY=0 git push`.

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Security](docs/security.md)
- [RAG pipeline](docs/rag-pipeline.md)
- [Agent](docs/agent.md)
- [Implementation TODOs](TODO.md)
