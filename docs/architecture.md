# Architecture

## Runtime shape

```text
User
 ↓
React frontend (Vite)
 ↓
FastAPI (`/health`, `/api/v1`)
 ├── Auth service / user repository
 └── Knowledge-base service / repository
 ↓
PostgreSQL + pgvector    Redis
```

## Decisions

- **Monorepo.** Backend, frontend, docs, and Compose live in one repository so API contracts and local startup stay together.
- **Configuration.** All runtime config is loaded through `pydantic-settings` from environment variables. Secrets are never hard-coded. `.env` is gitignored; `.env.example` documents required keys.
- **API prefix.** Versioned application routes live under `/api/v1`. `/health` stays at the app root so Docker and load balancers can probe liveness without a version.
- **Logging.** Application logs are JSON objects (timestamp, level, logger, message, plus extra fields). Request IDs and token usage are added in later phases.
- **Layering.** Routers validate input and call services. Services own use-cases. Repositories own SQL. This keeps business rules out of controllers and makes ownership checks live in one place.
- **Identity.** Users authenticate with email/password. Passwords are bcrypt-hashed. Access tokens are JWTs (`sub` = user id). Logout is client-side token discard plus `POST /api/v1/auth/logout`.
- **Tenancy.** Knowledge bases are fetched only with `user_id` in the repository query. Missing or foreign IDs return 404 so resource existence is not leaked.
- **LLM providers.** LLM and embedding calls will go through interfaces in `backend/app/llm/`. Config keys exist (`LLM_PROVIDER`, `LLM_MODEL`, `EMBEDDING_MODEL`).
- **Untrusted retrieval.** `wrap_retrieved_content` delimiters mark document text as data. The agent (later phases) must pass retrieved chunks through this helper and must never concatenate them into the system prompt.
- **Persistence.** Alembic migration `0001_initial_schema` creates all domain tables, foreign keys, indexes, the `vector` extension, and an HNSW cosine index on `document_chunks.embedding`. Embedding dimension is 1536 at migration time.
- **Host ports.** Postgres is published on **5433** so it does not collide with other local databases on 5432. Containers still use `postgres:5432` on the Compose network.
