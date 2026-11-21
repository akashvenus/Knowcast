"""Per-user resume position for a newsletter."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.newsletter import Newsletter
    from app.models.user import User


class PlaybackProgress(Base):
    __tablename__ = "playback_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "newsletter_id", name="uq_progress_user_newsletter"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    newsletter_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("newsletters.id", ondelete="CASCADE"), nullable=False
    )
    position_seconds: Mapped[float] = mapped_column(Float, nullable=False, server_default="0")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[User] = relationship(back_populates="playback_progress")
    newsletter: Mapped[Newsletter] = relationship(back_populates="playback_progress")
