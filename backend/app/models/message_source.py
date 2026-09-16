from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class MessageSource(Base):
    __tablename__ = "message_sources"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    message_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE"), index=True, nullable=False
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL"), index=True, nullable=True
    )
    chunk_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("document_chunks.id", ondelete="SET NULL"), index=True, nullable=True
    )
    relevance_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    citation_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    message: Mapped[Message] = relationship(back_populates="sources")
