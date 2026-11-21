"""Newsletter source subscriptions associated with a user."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.ingestion_job import IngestionJob
    from app.models.newsletter import Newsletter
    from app.models.user import User


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    ingestion_type: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="sources")
    newsletters: Mapped[list[Newsletter]] = relationship(
        back_populates="source", cascade="all, delete-orphan", passive_deletes=True
    )
    ingestion_jobs: Mapped[list[IngestionJob]] = relationship(
        back_populates="source", cascade="all, delete-orphan", passive_deletes=True
    )
