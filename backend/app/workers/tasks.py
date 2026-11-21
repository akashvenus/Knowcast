"""Small task used to verify that the Celery worker can process messages."""

from typing import Any

from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks.smoke_check")
def smoke_check() -> dict[str, Any]:
    """Return a small result to confirm the worker executed a task."""
    return {"status": "ok"}
