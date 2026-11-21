# Knowcast Phase 1 Tracker

This document is the working roadmap and progress record for the Phase 1 backend described in [the engineering brief](ENGINEERING_BRIEF.md). Update it as work is approved and completed. Keep evidence factual: record commands and results that were actually observed, and never mark a placeholder or mock-only feature complete.

## Status key

| Status | Meaning |
|---|---|
| Not started | No implementation work has begun for the item. |
| In progress | Work has begun and is not yet accepted. |
| Blocked | Progress depends on an unresolved decision, access, or external condition. Add the blocker below. |
| Complete | Acceptance criteria and required checks have passed, and evidence is recorded. |

Set a milestone to **Blocked** if one of its required items is blocked. Set it to **In progress** once work starts. Mark it **Complete** only when every checklist item and the milestone deliverable are verified. A milestone with no work started remains **Not started**.

## Project status

| Area | Status | Evidence / notes |
|---|---|---|
| Repository bootstrap | Complete | Git initialized; initial commit `2dcb06a` (`chore: initialize Knowcast repository`); branch `main` tracks `origin/main`; clean status observed on 2026-11-18. |
| Phase 1 backend | In progress | Chunk 1 settings and project configuration are implemented; remaining foundation chunks are not started. |
| Overall Phase 1 | In progress | Milestones 1–7 below are the scope of this tracker. Future mobile and product phases are out of scope. |

## Milestone tracker

### Milestone 1 — Backend foundation

**Status:** In progress

**Goal:** Establish the backend structure and local development foundation.

**Acceptance:** The backend starts locally, exposes health checks, applies initial database migrations, and passes foundation tests. Architecture documentation describes the resulting structure.

**Implementation branch:** Create `feat/backend-foundation` before starting the first code chunk. Keep all Milestone 1 implementation changes on that branch.

Complete the chunks in order. Start each chunk only after its plan is approved. Update its status, evidence, test result, and blockers as work progresses.

#### Chunk 1 — Project structure and configuration

**Status:** Complete

**Goal:** Establish the backend folders, dependencies, centralized settings, and environment example.

- [x] Inspect existing files and establish the backend structure from the engineering brief.
- [x] Add the baseline Python project/dependency configuration for the approved stack.
- [x] Add centralized Pydantic settings and a safe `.env.example` with no secrets.
- **Verification:** Confirm safe defaults and valid overrides work, invalid values fail with sanitized errors, root `.env` loading is independent of the working directory, `.env` is ignored, and `.env.example` remains trackable; run Ruff and focused tests.
- **Evidence / test result:** Python 3.14.2; `.venv\Scripts\ruff.exe check .` passed; `.venv\Scripts\python.exe -m pytest` passed (5 tests). Root `.env` loaded from the `backend` working directory (`test WARNING`). `git check-ignore` confirmed `.env` is ignored and `.env.example` is trackable. Settings validation errors did not echo invalid input values.
- **Blockers:** None recorded.

#### Chunk 2 — FastAPI app and health checks

**Status:** Complete

**Goal:** Create the API application entry point and health endpoint.

- [x] Create the FastAPI application and minimal app startup wiring.
- [x] Add a health endpoint with a stable response.
- [x] Add focused tests for app startup and health responses.
- **Verification:** Run Ruff and focused pytest tests; verify the endpoint locally.
- **Evidence / test result:** `.venv\Scripts\ruff.exe check .` passed. `.venv\Scripts\python.exe -m pytest` passed (7 tests, no warnings). A local Uvicorn smoke check returned `GET /health` → `{"status":"ok"}`. Response tests confirm no environment, version, or dependency details; invalid settings prevent app creation without echoing their values.
- **Blockers:** None recorded.

#### Chunk 3 — PostgreSQL, SQLAlchemy, and Alembic

**Status:** Complete

**Goal:** Establish database connection/session configuration and the migration workflow.

- [x] Configure optional PostgreSQL settings and lazy SQLAlchemy engine/session handling.
- [x] Define all nine engineering-brief entities with UUID keys, timezone-aware timestamps, JSONB content, indexes, unique keys, and owned-record cascades.
- [x] Configure Alembic with application settings and all model metadata; generate and manually review the initial migration.
- [x] Add focused settings, session, metadata, and disposable PostgreSQL migration/integrity tests.
- [x] Verify upgrade, repeat upgrade, downgrade to base, re-upgrade, unique email enforcement, and user-owned cascade deletion on PostgreSQL 16.
- **Verification:** Ruff and the full pytest suite ran against the disposable local `knowcast_test` database.
- **Evidence / test result:** `.venv\Scripts\ruff.exe check .` passed (`All checks passed!`). With `KNOWCAST_TEST_DATABASE_URL` pointed at a temporary PostgreSQL 16 container on `127.0.0.1:55432`, `.venv\Scripts\python.exe -m pytest -q` passed (21 tests, 0 skipped). The migration integration test completed upgrade → repeat upgrade → downgrade base → re-upgrade and passed PostgreSQL uniqueness/cascade checks. `.venv\Scripts\python.exe -m alembic -c backend\alembic.ini check` reported `No new upgrade operations detected.` The `/health` endpoint returned `200 {"status":"ok"}` with an unreachable database URL configured, confirming engine creation is lazy. Database credentials are optional; missing configuration produces a generic 503 only when a database session is requested. The migration keeps credentials out of `alembic.ini`.
- **Blockers:** None.

#### Chunk 4 — Redis and Celery

**Status:** Complete

**Goal:** Configure the background job infrastructure used by later pipeline milestones.

- [x] Configure a safe local Redis URL setting and environment example.
- [x] Configure Celery Redis broker/result settings and explicit task discovery.
- [x] Add a smoke task and unit tests for configuration, registration, and task output.
- [x] Verify a live worker executes the smoke task against temporary Redis.
- [x] Verify a worker reconnects when Redis becomes available after startup.
- **Verification:** Run Ruff and the full pytest suite with disposable PostgreSQL and Redis services; verify Redis outage recovery manually.
- **Evidence / test result:** `.venv\Scripts\ruff.exe check .` passed (`All checks passed!`). With temporary PostgreSQL 16 and Redis 7 containers running, `.venv\Scripts\python.exe -m pytest -q` passed (**28 passed**). The worker integration test launched a separate `--pool=solo` Celery worker and observed the smoke task return `{"status": "ok"}`. For recovery, the worker was started against an unavailable local Redis port, stayed running for six seconds, then connected after Redis started and processed the smoke task successfully. The liveness tests confirmed `/health` returns `200 {"status":"ok"}` while Redis is unavailable. Temporary containers were stopped after verification.
- **How to run the worker locally:** Start Redis, set `KNOWCAST_REDIS_URL` (or use the local default), change to `backend`, then run `..\.venv\Scripts\python.exe -m celery -A app.workers.celery_app:celery_app worker --pool=solo --loglevel=INFO`.
- **Blockers:** None.

#### Chunk 5 — Docker Compose and foundation closeout

**Status:** Not started

**Goal:** Run the foundation services together and document how the backend works locally.

- [ ] Add Docker Compose for the API, PostgreSQL, and Redis services.
- [ ] Verify local startup, health checks, database migration, and worker operation.
- [ ] Complete foundation tests and write architecture/setup documentation.
- [ ] Review all Milestone 1 acceptance criteria and record actual command results.
- **Verification:** Run Ruff and the full relevant pytest suite; verify local startup and health checks end to end.
- **Evidence / test result:** Not started.
- **Blockers:** None recorded.

**Milestone test gate:** All five chunks are complete; Ruff and relevant pytest checks pass; the backend starts locally, health checks respond, and the initial database migration applies. Record actual outputs below before marking the milestone complete.
- **Milestone evidence / results:** Not started.
- **Milestone blockers / decisions:** None recorded.

### Milestone 2 — ByteByteGo extraction

**Status:** Not started

**Goal:** Turn an authorized ByteByteGo page into a validated, provider-independent document with ordered content blocks.

**Acceptance:** Fixtures produce normalized documents that preserve metadata, ordering, lists, code, images, and relevant links; unsafe URL destinations and redirects are rejected.

- [ ] Define the newsletter provider interface and provider selection.
- [ ] Implement the ByteByteGo adapter and metadata/content extraction.
- [ ] Preserve content order and normalize headings, paragraphs, lists, images, code, and links.
- [ ] Add HTML fixtures and extraction/normalization tests, including malformed HTML.
- [ ] Add URL safety checks for protocols, resolved IPs, redirects, timeouts, and download limits.
- **Test gate:** Run Ruff and relevant pytest tests, including unsafe URLs and redirects.
- **Evidence / results:** Not started.
- **Blockers / decisions:** None recorded.

### Milestone 3 — Image processing

**Status:** Not started

**Goal:** Safely process newsletter images and create grounded explanations for relevant diagrams.

**Acceptance:** Relevant diagrams are validated, stored, and have structured AI explanations and narration; failures are recorded and recoverable.

- [ ] Download images with request and size limits; validate before storage.
- [ ] Classify images and retain source references and attribution.
- [ ] Add the vision provider interface and configured Gemini implementation.
- [ ] Generate structured diagram explanations and narration without overwriting extracted content.
- [ ] Add success and failure tests; mock Gemini in normal automated tests.
- **Test gate:** Run Ruff and relevant pytest tests, including invalid/oversized images and provider failures.
- **Evidence / results:** Not started.
- **Blockers / decisions:** None recorded.

### Milestone 4 — Audio generation

**Status:** Not started

**Goal:** Generate and assemble narration audio from normalized newsletter content.

**Acceptance:** Audio segments are generated, normalized, assembled into an MP3, and have persisted metadata with retryable failures.

- [ ] Define the TTS provider interface and configured Gemini implementation.
- [ ] Build narration scripts and segment them within provider limits.
- [ ] Generate individual audio segments and normalize them with FFmpeg.
- [ ] Assemble the final MP3 and persist duration/format metadata.
- [ ] Add retry, recovery, and failure tests; mock external AI in normal automated tests.
- **Test gate:** Run Ruff and relevant pytest tests for segmentation, provider errors, and assembly.
- **Evidence / results:** Not started.
- **Blockers / decisions:** None recorded.

### Milestone 5 — Storage and playback API

**Status:** Not started

**Goal:** Store media privately and provide short-lived playback access.

**Acceptance:** A generated MP3 can be fetched with a signed URL, and range requests support seeking.

- [ ] Define the storage abstraction and implement local MinIO storage.
- [ ] Store original images, segments, and final audio outside PostgreSQL and Redis messages.
- [ ] Keep buckets private and generate short-lived signed URLs.
- [ ] Implement audio playback and signed-URL refresh endpoints.
- [ ] Verify range-request behavior and add storage/playback tests.
- **Test gate:** Run Ruff and relevant pytest tests, including signed URL and range behavior.
- **Evidence / results:** Not started.
- **Blockers / decisions:** None recorded.

### Milestone 6 — Email ingestion

**Status:** Not started

**Goal:** Accept forwarded newsletters through a verified Resend webhook and feed them into the common processing pipeline.

**Acceptance:** Valid forwarded content is deduplicated and queued through the shared pipeline; invalid signatures and malformed content are rejected safely.

- [ ] Verify webhook signatures and enforce request size limits.
- [ ] Parse HTML/plain-text email content and image references.
- [ ] Add webhook idempotency/deduplication and common-pipeline integration.
- [ ] Add tests for invalid signatures, malformed email, duplicate delivery, and provider errors.
- **Test gate:** Run Ruff and relevant pytest tests; mock Resend in normal automated tests.
- **Evidence / results:** Not started.
- **Blockers / decisions:** None recorded.

### Milestone 7 — End-to-end validation

**Status:** Not started

**Goal:** Validate the complete pipeline, recovery behavior, and evaluation process.

**Acceptance:** The pipeline is repeatably validated against at least three newsletters, and the evaluation dataset contains at least ten newsletters with documented manual review.

- [ ] Run the complete pipeline against at least three authorized ByteByteGo newsletters.
- [ ] Test duplicate processing, image download failure, Gemini/TTS failures, and worker retry/restart.
- [ ] Build or complete the evaluation dataset of at least ten newsletters.
- [ ] Measure extraction completeness/order, image explanations, audio quality, reliability, cost, and performance.
- [ ] Manually compare output with source newsletters; update architecture and API documentation.
- **Test gate:** Run Ruff and the relevant/full pytest suite; record actual outcomes and any skipped checks.
- **Evidence / results:** Not started.
- **Blockers / decisions:** None recorded.

## Phase completion checklist

Update each item only when the behavior is implemented and verified. These are the 18 Definition of Done criteria from the engineering brief; all must be checked before Phase 1 is complete.

- [ ] A ByteByteGo URL can be submitted through the API.
- [ ] The request returns a job ID without waiting for processing.
- [ ] A background worker extracts and normalizes the newsletter.
- [ ] Content ordering is preserved.
- [ ] Relevant images are downloaded and stored.
- [ ] Gemini generates structured image explanations.
- [ ] Narration scripts are generated.
- [ ] Gemini TTS generates individual audio segments.
- [ ] FFmpeg assembles the segments into an MP3.
- [ ] The final audio is stored privately.
- [ ] The API returns a signed playback URL.
- [ ] Audio seeking/range requests have been verified.
- [ ] Job failures are persisted and recoverable.
- [ ] Duplicate processing is prevented.
- [ ] Email forwarding is supported through Resend.
- [ ] Automated tests pass.
- [ ] Docker Compose can run the development environment.
- [ ] Documentation explains setup, architecture, APIs, and evaluation.

## Error history

Retain resolved errors here so recovery steps are visible. Add a new entry rather than deleting a resolved one. Never include secrets, API keys, signed URLs, or email tokens.

| Date | Area | Symptom | Resolution | Verification | Status |
|---|---|---|---|---|---|
| 2026-11-18 | Git bootstrap | Initial Git metadata write was denied in the restricted shell; the first push attempt also lacked interactive GitHub authentication. | Git metadata operations were retried with elevated access and GitHub authentication was completed. | User confirmed setup worked; repository later showed clean `main...origin/main`. | Resolved |
| 2026-11-18 | Chunk 1 lint | Ruff reported import-order errors in the settings module and its tests. | Reordered imports to match Ruff's configured rules. | `.venv\Scripts\ruff.exe check .` passed after the fix. | Resolved |
| 2026-11-21 | Chunk 2 TestClient | Sandboxed Windows asyncio socket-pair setup caused TestClient requests to hang. | Ran the tests with local socket access; used Starlette's recommended `httpx2` transport alongside `httpx` for later newsletter fetching. | Full pytest suite passed (7 tests) without warnings. | Resolved |
| 2026-11-21 | Chunk 2 dependency warning | Starlette warned that its `TestClient` use of plain `httpx` is deprecated. | Added `httpx2` for the current TestClient while retaining `httpx` for planned newsletter fetching. | Full pytest suite passed (7 tests) without warnings. | Resolved |
| 2026-11-21 | Chunk 3 dependency install | Initial dependency installation could not reach the package index from the restricted environment. | Retried the approved package installation with network access. | SQLAlchemy, Alembic, Psycopg 3 and their dependencies installed successfully. | Resolved |
| 2026-11-21 | Chunk 3 settings test | A URL containing a password was assumed malformed, but Pydantic correctly accepted it as a valid PostgreSQL DSN. | Changed the validation test to use an invalid port while checking that the password portion is absent from the error. | Full pytest suite passed; invalid URL validation did not reveal the secret. | Resolved |
| 2026-11-21 | Chunk 3 Ruff | Ruff flagged import ordering and line length in newly added database modules and generated migration code. | Applied Ruff's import fixes and formatting, then corrected remaining long declarations. | `.venv\Scripts\ruff.exe check .` passed (`All checks passed!`). | Resolved |
| 2026-11-21 | Chunk 4 settings and task tests | Initial test inputs treated a loosely formatted Redis URL as invalid and compared Celery task proxies by object identity. | Used an invalid port for validation and compared the stable registered task name instead. | Worker unit tests passed; full suite passed (28 tests). | Resolved |
| 2026-11-21 | Chunk 4 worker integration | The first live worker test did not locate the backend package from the subprocess working directory, so the task result was not observed. | Ran the worker and task producer from the `backend` directory and used a separate producer process with the configured Redis URL. | Redis worker integration test passed; task returned `{"status": "ok"}`. | Resolved |

## Decision and blocker log

Add decisions that affect implementation and unresolved blockers here. Link to a decision record under `docs/decisions/` if a significant architectural choice needs a permanent rationale.

| Date | Type | Topic | Decision / blocker | Status |
|---|---|---|---|---|
| — | — | — | No open decisions or blockers recorded. | — |

## Milestone closeout record

At the end of each milestone, add a dated entry with the files changed, decisions made, how to run the result, the purpose of each new module, test/lint commands and their actual output, open issues, what the user should review, and a suggested commit message. Do not create commits unless explicitly asked.

### Chunk 3 closeout — 2026-11-21

- **Files:** Added SQLAlchemy base/session modules; nine model modules; Alembic configuration, environment, template, and initial revision `178dc1618afc`; database settings and environment example; database and migration tests. Updated README, Ruff/pytest configuration, requirements, and this tracker.
- **Decisions:** Database configuration remains optional; app construction creates an engine without opening a connection. Foreign keys cascade through owned rows; `audio_segments.content_block_id` and `ingestion_jobs.newsletter_id` use `SET NULL` so retained work records can outlive an individual content association. Multiple audio assets and ingestion jobs remain valid. PostgreSQL JSONB is limited to `content_blocks.content_json`.
- **Modules:** `app/db/base.py` defines shared metadata and naming; `app/db/session.py` creates lazy engine/session factories and request-scoped cleanup; `app/models/` defines the nine schema entities; `migrations/env.py` reads configured settings and registers all models; the revision creates and drops the schema.
- **Run locally:** Set `KNOWCAST_DATABASE_URL` in an ignored `.env`, install `backend/requirements.txt`, then run `.venv\Scripts\python.exe -m alembic -c backend\alembic.ini upgrade head`. Run checks with `.venv\Scripts\ruff.exe check .` and `.venv\Scripts\python.exe -m pytest -q`. Set `KNOWCAST_TEST_DATABASE_URL` only to a disposable database named `knowcast_test` to run the migration lifecycle test.
- **Verification:** Ruff passed. Full pytest passed: **21 passed**. Disposable PostgreSQL 16 migration and integrity checks passed through upgrade, repeat upgrade, downgrade, re-upgrade, duplicate email rejection, and parent deletion cascade. Alembic schema drift check reported `No new upgrade operations detected.` No database service was needed for the unit suite or liveness endpoint.
- **Open issues:** None for Chunk 3.
- **Review guidance:** Review the initial schema revision and the chosen nullable email-ingestion URL / `SET NULL` relationships. The migration was generated and manually reviewed, then exercised through the full disposable-database lifecycle.
- **Suggested commit:** `feat: establish database foundation`

### Chunk 4 closeout — 2026-11-21

- **Files:** Added Redis settings and `.env.example` value; added `backend/app/workers/` with the Celery app and smoke task; added worker unit and Redis integration tests. Updated README, dependencies, and this tracker.
- **Decisions:** Redis is both the Celery broker and result backend. Worker startup reconnects indefinitely with Celery's increasing retry delays. FastAPI startup and `/health` do not connect to Redis. No in-memory fallback or newsletter-processing tasks were added.
- **Modules:** `core/config.py` owns the typed Redis URL setting; `workers/celery_app.py` creates the Celery app and declares broker, result, retry, serialization, and task discovery settings; `workers/tasks.py` provides the one smoke task used by the integration check.
- **Run locally:** Start Redis, set `KNOWCAST_REDIS_URL` (or use `redis://localhost:6379/0`), change to `backend`, then run `..\.venv\Scripts\python.exe -m celery -A app.workers.celery_app:celery_app worker --pool=solo --loglevel=INFO`. Run `.venv\Scripts\ruff.exe check .` and `.venv\Scripts\python.exe -m pytest -q`. Set `KNOWCAST_TEST_REDIS_URL` to a disposable local Redis URL to enable the live worker test.
- **Verification:** Ruff passed. Full pytest passed: **28 passed** with PostgreSQL 16 and Redis 7 integration services available. Worker start-before-Redis recovery was manually verified and returned `{"status": "ok"}` after Redis started. Health remained independent of Redis. Temporary containers were stopped.
- **Open issues:** None for Chunk 4. Docker Compose and combined foundation startup remain in Chunk 5.
- **Review guidance:** Review the Celery retry settings, task registration, and worker run command. No `NON-OBVIOUS` comments were added; Celery connection retries are explicit configuration values.
- **Suggested commit:** `feat: configure redis and celery worker`
