from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.core.exceptions import ConflictError, NotFoundError
from app.models.knowledge_base import KnowledgeBase
from app.repositories.knowledge_base import KnowledgeBaseRepository


class KnowledgeBaseService:
    def __init__(self, knowledge_bases: KnowledgeBaseRepository) -> None:
        self.knowledge_bases = knowledge_bases

    def create(self, user_id: UUID, name: str, description: str | None) -> KnowledgeBase:
        if self.knowledge_bases.get_owned_by_name(user_id, name) is not None:
            raise ConflictError("A knowledge base with this name already exists.")
        now = datetime.now(UTC)
        knowledge_base = KnowledgeBase(
            id=uuid4(),
            user_id=user_id,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
        )
        return self.knowledge_bases.add(knowledge_base)

    def list_for_user(self, user_id: UUID) -> list[KnowledgeBase]:
        return self.knowledge_bases.list_for_user(user_id)

    def get_for_user(self, user_id: UUID, knowledge_base_id: UUID) -> KnowledgeBase:
        knowledge_base = self.knowledge_bases.get_owned(knowledge_base_id, user_id)
        if knowledge_base is None:
            raise NotFoundError("Knowledge base not found.")
        return knowledge_base

    def update_for_user(
        self,
        user_id: UUID,
        knowledge_base_id: UUID,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> KnowledgeBase:
        knowledge_base = self.get_for_user(user_id, knowledge_base_id)
        if name is not None and name != knowledge_base.name:
            if self.knowledge_bases.get_owned_by_name(user_id, name) is not None:
                raise ConflictError("A knowledge base with this name already exists.")
            knowledge_base.name = name
        if description is not None:
            knowledge_base.description = description
        self.knowledge_bases.save()
        return knowledge_base

    def delete_for_user(self, user_id: UUID, knowledge_base_id: UUID) -> None:
        knowledge_base = self.get_for_user(user_id, knowledge_base_id)
        self.knowledge_bases.delete(knowledge_base)
