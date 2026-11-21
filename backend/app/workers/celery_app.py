"""Celery application configured to use Redis as its broker and result store."""

from celery import Celery

from app.core.config import Settings


def create_celery_app(settings: Settings | None = None) -> Celery:
    """Create a Celery app without connecting to Redis during setup."""
    if settings is None:
        settings = Settings()

    redis_url = str(settings.redis_url)
    celery_application = Celery(
        "knowcast",
        broker=redis_url,
        backend=redis_url,
        include=["app.workers.tasks"],
    )
    celery_application.conf.update(
        broker_connection_retry=True,
        broker_connection_retry_on_startup=True,
        broker_connection_max_retries=None,
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
    )
    return celery_application


celery_app = create_celery_app()
