from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.knowledge_base import KnowledgeBaseRepository
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.knowledge_base import KnowledgeBaseService

bearer_scheme = HTTPBearer(auto_error=False)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_knowledge_base_repository(db: Session = Depends(get_db)) -> KnowledgeBaseRepository:
    return KnowledgeBaseRepository(db)


def get_auth_service(
    users: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(users)


def get_knowledge_base_service(
    knowledge_bases: KnowledgeBaseRepository = Depends(get_knowledge_base_repository),
) -> KnowledgeBaseService:
    return KnowledgeBaseService(knowledge_bases)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError()
    try:
        user_id: UUID = decode_access_token(credentials.credentials)
    except (jwt.InvalidTokenError, ValueError) as exc:
        raise UnauthorizedError("Invalid or expired token.") from exc
    user = auth_service.users.get_by_id(user_id)
    if user is None:
        raise UnauthorizedError("Invalid or expired token.")
    return user
