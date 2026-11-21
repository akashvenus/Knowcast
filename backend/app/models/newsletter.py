"""Normalized newsletter records extracted from a source."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.audio_asset import AudioAsset
    from app.models.content_block import ContentBlock
    from app.models.ingestion_job import IngestionJob
    from app.models.playback_progress import PlaybackProgress
    from app.models.source import Source


class Newsletter(Base):
    __tablename__ = "newsletters"
    __table_args__ = (
        UniqueConstraint("source_id", "original_url", name="uq_newsletter_source_url"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    source_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    author: Mapped[str | None] = mapped_column(String(255))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    original_url: Mapped[str | None] = mapped_column(String(2048))
    status: Mapped[str] = mapped_column(String(40), nullable=False, server_default="queued")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    source: Mapped[Source] = relationship(back_populates="newsletters")
    content_blocks: Mapped[list[ContentBlock]] = relationship(
        back_populates="newsletter", cascade="all, delete-orphan", passive_deletes=True
    )
    audio_assets: Mapped[list[AudioAsset]] = relationship(
        back_populates="newsletter", cascade="all, delete-orphan", passive_deletes=True
    )
    ingestion_jobs: Mapped[list[IngestionJob]] = relationship(
        back_populates="newsletter", cascade="all, delete-orphan", passive_deletes=True
    )
    playback_progress: Mapped[list[PlaybackProgress]] = relationship(
        back_populates="newsletter", cascade="all, delete-orphan", passive_deletes=True
    )
