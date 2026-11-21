"""Generated audio segment metadata and ordering."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.audio_asset import AudioAsset
    from app.models.content_block import ContentBlock


class AudioSegment(Base):
    __tablename__ = "audio_segments"
    __table_args__ = (
        UniqueConstraint("audio_asset_id", "position", name="uq_segment_audio_position"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    audio_asset_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("audio_assets.id", ondelete="CASCADE"), nullable=False
    )
    content_block_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("content_blocks.id", ondelete="SET NULL")
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[float | None] = mapped_column(Float)
    end_time: Mapped[float | None] = mapped_column(Float)
    storage_key: Mapped[str | None] = mapped_column(String(1024))
    status: Mapped[str] = mapped_column(String(40), nullable=False, server_default="queued")

    audio_asset: Mapped[AudioAsset] = relationship(back_populates="segments")
    content_block: Mapped[ContentBlock | None] = relationship(back_populates="audio_segments")
