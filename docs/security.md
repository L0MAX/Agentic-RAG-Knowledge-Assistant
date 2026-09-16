# Security

## Current controls

- Secrets come from environment variables. `.env` is not committed.
- Passwords are hashed with bcrypt. Plaintext is never stored. bcrypt’s 72-byte limit is enforced.
- JWTs are signed with `JWT_SECRET` / `JWT_ALGORITHM`. Production must replace `change-me-in-development`.
- Protected routes require `Authorization: Bearer <token>`. Invalid or missing tokens return 401.
- Knowledge-base reads/writes are scoped to the authenticated user in the repository layer (404 on IDOR).
- Request bodies are validated with Pydantic (email format, password length, field limits).
- CORS origins are explicit and configurable via `CORS_ORIGINS`.
- Retrieved document text is wrapped with untrusted delimiters (`app/core/untrusted.py`). The agent must use this helper so document content cannot override developer instructions.
- Production responses must never include stack traces, API keys, database credentials, JWT secrets, or system prompts.

## Upcoming controls

See `TODO.md` phases 13 and 21 for prompt-injection regression tests, upload validation, and rate limiting.
