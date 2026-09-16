# API

Base URL (local): `http://localhost:8000`

Versioned prefix: `/api/v1`

## Health

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/health` | No | Process liveness |
| GET | `/api/v1/health` | No | Versioned health payload |
| GET | `/api/v1/` | No | API name, version, and environment |

## Auth

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/v1/auth/register` | No | Create account, return JWT |
| POST | `/api/v1/auth/login` | No | Authenticate, return JWT |
| POST | `/api/v1/auth/logout` | Yes | Client should discard the token |
| GET | `/api/v1/auth/me` | Yes | Current user profile |
| PATCH | `/api/v1/auth/me` | Yes | Update email and/or password |

Register/login body: `{ "email": "...", "password": "..." }`  
Token response: `{ "access_token": "...", "token_type": "bearer", "user": { ... } }`

## Knowledge bases

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/v1/knowledge-bases` | Yes | Create |
| GET | `/api/v1/knowledge-bases` | Yes | List current user's KBs |
| GET | `/api/v1/knowledge-bases/{id}` | Yes | Get owned KB (404 otherwise) |
| PATCH | `/api/v1/knowledge-bases/{id}` | Yes | Update owned KB |
| DELETE | `/api/v1/knowledge-bases/{id}` | Yes | Delete owned KB |

Errors use `{ "code": "...", "message": "..." }`. Validation failures use FastAPI’s 422 shape.

OpenAPI: `/docs` and `/openapi.json`.
