"""PostgreSQL engine and request-scoped SQLAlchemy sessions."""

from collections.abc import Generator

from fastapi import HTTPException, Request
from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_session_factory(
    database_url: PostgresDsn | None,
) -> sessionmaker[Session] | None:
    """Build a lazy PostgreSQL engine and its session factory when configured."""
    if database_url is None:
        return None

    engine = create_engine(str(database_url), pool_pre_ping=True)
    return sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def get_db_session(request: Request) -> Generator[Session, None, None]:
    """Yield one database session and always close it after the request."""
    session_factory = request.app.state.database_session_factory
    if session_factory is None:
        raise HTTPException(status_code=503, detail="Database is not configured.")

    session = session_factory()
    try:
        yield session
    finally:
        session.close()
