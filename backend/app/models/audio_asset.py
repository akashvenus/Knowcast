"""Generated audio versions for a newsletter."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.audio_segment import AudioSegment
    from app.models.newsletter import Newsletter


class AudioAsset(Base):
    __tablename__ = "audio_assets"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    newsletter_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("newsletters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    storage_key: Mapped[str | None] = mapped_column(String(1024))
    format: Mapped[str] = mapped_column(String(20), nullable=False, server_default="mp3")
    duration: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(40), nullable=False, server_default="queued")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    newsletter: Mapped[Newsletter] = relationship(back_populates="audio_assets")
    segments: Mapped[list[AudioSegment]] = relationship(
        back_populates="audio_asset", cascade="all, delete-orphan", passive_deletes=True
    )
