import os
from collections.abc import Generator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from tests.db_support import ensure_test_database, postgres_available, test_database_url

from app.core.config import get_settings
from app.db.session import get_db, reset_engine
from app.main import create_app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    get_settings.cache_clear()
    with TestClient(create_app()) as test_client:
        yield test_client
    get_settings.cache_clear()


@pytest.fixture(scope="session")
def test_engine() -> Generator[Engine, None, None]:
    if not postgres_available():
        pytest.skip("PostgreSQL is required for integration tests")
    test_url = ensure_test_database()
    os.environ["DATABASE_URL"] = test_url
    get_settings.cache_clear()
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_url)
    command.upgrade(alembic_cfg, "head")
    engine = create_engine(test_url, pool_pre_ping=True)
    yield engine
    engine.dispose()
    get_settings.cache_clear()


@pytest.fixture
def db_session(test_engine: Engine) -> Generator[Session, None, None]:
    connection = test_engine.connect()
    transaction = connection.begin()
    factory = sessionmaker(bind=connection, autocommit=False, autoflush=False, class_=Session)
    session = factory()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def api_client(
    db_session: Session, monkeypatch: pytest.MonkeyPatch
) -> Generator[TestClient, None, None]:
    monkeypatch.setenv("DATABASE_URL", test_database_url())
    get_settings.cache_clear()
    reset_engine()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    application = create_app()
    application.dependency_overrides[get_db] = override_get_db
    with TestClient(application) as test_client:
        yield test_client
    application.dependency_overrides.clear()
    get_settings.cache_clear()
    reset_engine()
