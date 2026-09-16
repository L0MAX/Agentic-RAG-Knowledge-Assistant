from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError, NotFoundError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def register(self, email: str, password: str) -> tuple[User, str]:
        normalized = _normalize_email(email)
        if self.users.get_by_email(normalized) is not None:
            raise EmailAlreadyRegisteredError()
        now = datetime.now(UTC)
        user = User(
            id=uuid4(),
            email=normalized,
            password_hash=hash_password(password),
            created_at=now,
            updated_at=now,
        )
        self.users.add(user)
        return user, create_access_token(user.id)

    def login(self, email: str, password: str) -> tuple[User, str]:
        user = self.users.get_by_email(_normalize_email(email))
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        return user, create_access_token(user.id)

    def get_user(self, user_id: UUID) -> User:
        user = self.users.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        return user

    def update_profile(
        self,
        user: User,
        *,
        email: str | None = None,
        current_password: str | None = None,
        new_password: str | None = None,
    ) -> User:
        if email is not None:
            normalized = _normalize_email(email)
            existing = self.users.get_by_email(normalized)
            if existing is not None and existing.id != user.id:
                raise EmailAlreadyRegisteredError()
            user.email = normalized
        if new_password is not None:
            if current_password is None or not verify_password(
                current_password, user.password_hash
            ):
                raise InvalidCredentialsError()
            user.password_hash = hash_password(new_password)
        self.users.save()
        return user


def _normalize_email(email: str) -> str:
    return email.strip().lower()
