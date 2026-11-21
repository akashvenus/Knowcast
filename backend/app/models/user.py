"""User records that own newsletter sources and playback progress."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.playback_progress import PlaybackProgress
    from app.models.source import Source


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sources: Mapped[list[Source]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    playback_progress: Mapped[list[PlaybackProgress]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
