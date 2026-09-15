# Security

Phase 1 only establishes the configuration and isolation baseline. Authentication, authorization, upload validation, and prompt-injection controls are implemented in later phases.

## Current controls

- Secrets come from environment variables. `.env` is not committed.
- JWT secret and LLM API keys have no production defaults that are safe to ship; replace `JWT_SECRET` and `LLM_API_KEY` before any deployment.
- CORS origins are explicit and configurable via `CORS_ORIGINS`.
- Production responses must never include stack traces, API keys, database credentials, JWT secrets, or system prompts.

## Upcoming controls

See `TODO.md` phases 3, 13, and 21 for authentication, prompt-injection protection, and the full security checklist.
