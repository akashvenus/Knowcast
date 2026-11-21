"""Ordered extracted content blocks belonging to a newsletter."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.audio_segment import AudioSegment
    from app.models.image_asset import ImageAsset
    from app.models.newsletter import Newsletter


class ContentBlock(Base):
    __tablename__ = "content_blocks"
    __table_args__ = (
        UniqueConstraint("newsletter_id", "position", name="uq_block_newsletter_position"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    newsletter_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("newsletters.id", ondelete="CASCADE"), nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    content_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    newsletter: Mapped[Newsletter] = relationship(back_populates="content_blocks")
    image_assets: Mapped[list[ImageAsset]] = relationship(
        back_populates="content_block", cascade="all, delete-orphan", passive_deletes=True
    )
    audio_segments: Mapped[list[AudioSegment]] = relationship(back_populates="content_block")
