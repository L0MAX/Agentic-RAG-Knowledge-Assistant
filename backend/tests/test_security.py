from uuid import uuid4

import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_is_not_plaintext() -> None:
    hashed = hash_password("password12")
    assert hashed != "password12"
    assert verify_password("password12", hashed)
    assert not verify_password("other-password", hashed)


def test_password_longer_than_bcrypt_limit_is_rejected() -> None:
    with pytest.raises(ValueError, match="72 bytes"):
        hash_password("x" * 80)


def test_access_token_round_trip() -> None:
    user_id = uuid4()
    token = create_access_token(user_id)
    assert decode_access_token(token) == user_id
