import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from app.core.config import get_settings

REQUIRED_TABLES = {
    "users",
    "knowledge_bases",
    "documents",
    "document_chunks",
    "conversations",
    "messages",
    "message_sources",
}


def test_database_url() -> str:
    base = get_settings().database_url.rsplit("/", 1)[0]
    return f"{base}/agentic_rag_test"


def psycopg_url(sqlalchemy_url: str) -> str:
    return sqlalchemy_url.replace("postgresql+psycopg://", "postgresql://")


def postgres_available() -> bool:
    try:
        engine = create_engine(get_settings().database_url, pool_pre_ping=True)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        engine.dispose()
        return True
    except Exception:
        return False


requires_postgres = pytest.mark.skipif(
    not postgres_available(), reason="PostgreSQL is required for integration tests"
)


def ensure_test_database() -> str:
    import psycopg

    admin_url = psycopg_url(get_settings().database_url).rsplit("/", 1)[0] + "/postgres"
    url = test_database_url()
    db_name = url.rsplit("/", 1)[1]
    with psycopg.connect(admin_url, autocommit=True) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            if cursor.fetchone() is None:
                cursor.execute(f'CREATE DATABASE "{db_name}"')
    return url


def auth_header(client: TestClient, email: str, password: str = "password12") -> dict[str, str]:
    response = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
