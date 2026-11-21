"""Live worker test for a disposable local Redis instance."""

import os
import subprocess
import sys
import time

import pytest
from sqlalchemy.engine import make_url

pytestmark = pytest.mark.integration


def test_local_worker_executes_smoke_task() -> None:
    redis_url = os.getenv("KNOWCAST_TEST_REDIS_URL")
    if not redis_url:
        pytest.skip("Set KNOWCAST_TEST_REDIS_URL to a disposable local Redis instance.")

    parsed_url = make_url(redis_url)
    assert parsed_url.host in {"localhost", "127.0.0.1"}, "Test Redis must be local."

    worker_environment = os.environ.copy()
    worker_environment["KNOWCAST_REDIS_URL"] = redis_url
    worker = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "celery",
            "-A",
            "app.workers.celery_app:celery_app",
            "worker",
            "--pool=solo",
            "--loglevel=WARNING",
            "--without-gossip",
            "--without-mingle",
            "--without-heartbeat",
        ],
        cwd="backend",
        env=worker_environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        time.sleep(1)
        assert worker.poll() is None, "Celery worker exited before receiving the smoke task."
        producer = subprocess.run(
            [
                sys.executable,
                "-c",
                "import json; from app.workers.tasks import smoke_check; "
                "result = smoke_check.apply_async().get(timeout=30); "
                "print(json.dumps(result, sort_keys=True))",
            ],
            cwd="backend",
            env=worker_environment,
            capture_output=True,
            text=True,
            timeout=40,
            check=True,
        )
        assert producer.stdout.strip() == '{"status": "ok"}'
    finally:
        worker.terminate()
        try:
            worker.wait(timeout=10)
        except subprocess.TimeoutExpired:
            worker.kill()
            worker.wait(timeout=5)
