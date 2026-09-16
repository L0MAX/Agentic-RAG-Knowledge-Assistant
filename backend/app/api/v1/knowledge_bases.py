from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.deps import get_current_user, get_knowledge_base_service
from app.models.user import User
from app.schemas.knowledge_base import (
    KnowledgeBaseCreateRequest,
    KnowledgeBaseResponse,
    KnowledgeBaseUpdateRequest,
)
from app.services.knowledge_base import KnowledgeBaseService

router = APIRouter(prefix="/knowledge-bases", tags=["knowledge-bases"])


@router.post("", response_model=KnowledgeBaseResponse, status_code=status.HTTP_201_CREATED)
def create_knowledge_base(
    payload: KnowledgeBaseCreateRequest,
    current_user: User = Depends(get_current_user),
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
) -> KnowledgeBaseResponse:
    knowledge_base = service.create(current_user.id, payload.name, payload.description)
    return KnowledgeBaseResponse.model_validate(knowledge_base)


@router.get("", response_model=list[KnowledgeBaseResponse])
def list_knowledge_bases(
    current_user: User = Depends(get_current_user),
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
) -> list[KnowledgeBaseResponse]:
    return [
        KnowledgeBaseResponse.model_validate(item)
        for item in service.list_for_user(current_user.id)
    ]


@router.get("/{knowledge_base_id}", response_model=KnowledgeBaseResponse)
def get_knowledge_base(
    knowledge_base_id: UUID,
    current_user: User = Depends(get_current_user),
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
) -> KnowledgeBaseResponse:
    knowledge_base = service.get_for_user(current_user.id, knowledge_base_id)
    return KnowledgeBaseResponse.model_validate(knowledge_base)


@router.patch("/{knowledge_base_id}", response_model=KnowledgeBaseResponse)
def update_knowledge_base(
    knowledge_base_id: UUID,
    payload: KnowledgeBaseUpdateRequest,
    current_user: User = Depends(get_current_user),
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
) -> KnowledgeBaseResponse:
    knowledge_base = service.update_for_user(
        current_user.id,
        knowledge_base_id,
        name=payload.name,
        description=payload.description,
    )
    return KnowledgeBaseResponse.model_validate(knowledge_base)


@router.delete("/{knowledge_base_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge_base(
    knowledge_base_id: UUID,
    current_user: User = Depends(get_current_user),
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
) -> Response:
    service.delete_for_user(current_user.id, knowledge_base_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
