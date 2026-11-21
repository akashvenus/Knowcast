"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import Settings
from app.db.session import create_session_factory


def create_app() -> FastAPI:
    """Create the API application using validated settings."""
    settings = Settings()
    application = FastAPI(
        title="Knowcast",
        debug=settings.app_env == "development",
    )
    application.state.database_session_factory = create_session_factory(settings.database_url)
    application.include_router(health_router)
    return application


app = create_app()
