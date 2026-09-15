# Architecture

Phase 1 establishes the monorepo and runtime seams. Domain features are added in later phases.

## Runtime shape

```text
User
 ↓
React frontend (Vite)
 ↓
FastAPI (`/health`, `/api/v1`)
 ↓
PostgreSQL + pgvector    Redis
```

## Decisions

- **Monorepo.** Backend, frontend, docs, and Compose live in one repository so API contracts and local startup stay together.
- **Configuration.** All runtime config is loaded through `pydantic-settings` from environment variables. Secrets are never hard-coded. `.env` is gitignored; `.env.example` documents required keys.
- **API prefix.** Versioned application routes live under `/api/v1`. `/health` stays at the app root so Docker and load balancers can probe liveness without a version.
- **Logging.** Application logs are JSON objects (timestamp, level, logger, message, plus extra fields). Request IDs and token usage are added in later phases.
- **LLM providers.** LLM and embedding calls will go through interfaces in `backend/app/llm/`. Phase 1 only reserves the package and config keys (`LLM_PROVIDER`, `LLM_MODEL`, `EMBEDDING_MODEL`).
- **Persistence.** SQLAlchemy `Base` and Alembic are wired, but tables are created in Phase 2. Compose uses the `pgvector/pgvector` image so the vector extension is available when migrations start. Postgres is published on host port **5433** so it does not collide with other local databases on 5432. Containers still use `postgres:5432` on the Compose network.
- **Business logic.** Routers stay thin. Services, repositories, agents, retrieval, and ingestion packages exist as empty seams for later phases.
