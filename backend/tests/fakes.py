from uuid import UUID

from app.models.user import User


class InMemoryUserRepository:
    def __init__(self) -> None:
        self.by_id: dict[UUID, User] = {}
        self.by_email: dict[str, User] = {}

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.by_id.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.by_email.get(email)

    def add(self, user: User) -> User:
        self.by_id[user.id] = user
        self.by_email[user.email] = user
        return user

    def save(self) -> None:
        self.by_email = {user.email: user for user in self.by_id.values()}
