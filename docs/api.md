# API

Base URL (local): `http://localhost:8000`

Versioned prefix: `/api/v1`

## Phase 1 endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Process liveness for Docker and local checks |
| GET | `/api/v1/health` | Versioned health payload |
| GET | `/api/v1/` | API name, version, and environment |
| GET | `/docs` | OpenAPI Swagger UI |
| GET | `/openapi.json` | OpenAPI schema |

Authentication, knowledge bases, documents, and conversations are added in later phases.
