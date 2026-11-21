"""Image source and processing metadata for a content block."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.content_block import ContentBlock


class ImageAsset(Base):
    __tablename__ = "image_assets"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    content_block_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("content_blocks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    storage_key: Mapped[str | None] = mapped_column(String(1024))
    image_type: Mapped[str | None] = mapped_column(String(80))
    ai_description: Mapped[str | None] = mapped_column(Text)
    processing_status: Mapped[str] = mapped_column(
        String(40), nullable=False, server_default="queued"
    )

    content_block: Mapped[ContentBlock] = relationship(back_populates="image_assets")
