from uuid import uuid4

import pytest
from tests.fakes import InMemoryUserRepository

from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.services.auth import AuthService


def test_register_normalizes_email_and_hashes_password() -> None:
    service = AuthService(InMemoryUserRepository())
    user, token = service.register("  Admin@Example.COM ", "password12")
    assert user.email == "admin@example.com"
    assert user.password_hash != "password12"
    assert verify_password("password12", user.password_hash)
    assert token


def test_register_rejects_duplicate_email() -> None:
    service = AuthService(InMemoryUserRepository())
    service.register("a@example.com", "password12")
    with pytest.raises(EmailAlreadyRegisteredError):
        service.register("A@example.com", "password12")


def test_login_rejects_wrong_password() -> None:
    users = InMemoryUserRepository()
    users.add(
        User(
            id=uuid4(),
            email="a@example.com",
            password_hash=hash_password("password12"),
        )
    )
    service = AuthService(users)
    with pytest.raises(InvalidCredentialsError):
        service.login("a@example.com", "nope-nope")


def test_login_accepts_valid_credentials() -> None:
    service = AuthService(InMemoryUserRepository())
    service.register("a@example.com", "password12")
    user, token = service.login("a@example.com", "password12")
    assert user.email == "a@example.com"
    assert token
