from app.core.config import Settings, get_settings


def test_settings_load_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@db:5432/testdb")
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/1")
    monkeypatch.setenv("LLM_MODEL", "test-llm")
    monkeypatch.setenv("EMBEDDING_MODEL", "test-embed")
    monkeypatch.setenv("EMBEDDING_DIMENSIONS", "768")
    monkeypatch.setenv("JWT_SECRET", "unit-test-secret")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")

    get_settings.cache_clear()
    settings = Settings()

    assert settings.app_env == "test"
    assert settings.database_url.endswith("/testdb")
    assert settings.redis_url == "redis://redis:6379/1"
    assert settings.llm_model == "test-llm"
    assert settings.embedding_model == "test-embed"
    assert settings.embedding_dimensions == 768
    assert settings.jwt_secret == "unit-test-secret"
    assert settings.cors_origin_list == [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    get_settings.cache_clear()
