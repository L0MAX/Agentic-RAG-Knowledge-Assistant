from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge_base import KnowledgeBase


class KnowledgeBaseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_for_user(self, user_id: UUID) -> list[KnowledgeBase]:
        return list(
            self.db.scalars(
                select(KnowledgeBase)
                .where(KnowledgeBase.user_id == user_id)
                .order_by(KnowledgeBase.created_at.desc())
            ).all()
        )

    def get_owned(self, knowledge_base_id: UUID, user_id: UUID) -> KnowledgeBase | None:
        return self.db.scalar(
            select(KnowledgeBase).where(
                KnowledgeBase.id == knowledge_base_id,
                KnowledgeBase.user_id == user_id,
            )
        )

    def get_owned_by_name(self, user_id: UUID, name: str) -> KnowledgeBase | None:
        return self.db.scalar(
            select(KnowledgeBase).where(
                KnowledgeBase.user_id == user_id,
                KnowledgeBase.name == name,
            )
        )

    def add(self, knowledge_base: KnowledgeBase) -> KnowledgeBase:
        self.db.add(knowledge_base)
        self.db.flush()
        return knowledge_base

    def delete(self, knowledge_base: KnowledgeBase) -> None:
        self.db.delete(knowledge_base)
        self.db.flush()

    def save(self) -> None:
        self.db.flush()
