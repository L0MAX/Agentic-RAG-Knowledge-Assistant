"""Data-access abstractions. Callers go through repositories, not ad-hoc queries in routers."""

from app.repositories.knowledge_base import KnowledgeBaseRepository
from app.repositories.user import UserRepository

__all__ = ["KnowledgeBaseRepository", "UserRepository"]
