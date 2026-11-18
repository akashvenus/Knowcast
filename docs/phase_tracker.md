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
| Phase 1 backend | Not started | No backend implementation exists yet. |
| Overall Phase 1 | Not started | Milestones 1–7 below are the scope of this tracker. Future mobile and product phases are out of scope. |

## Milestone tracker

### Milestone 1 — Backend foundation

**Status:** Not started

**Goal:** Establish the backend structure and local development foundation.

**Acceptance:** The backend starts locally, exposes health checks, applies initial database migrations, and passes foundation tests. Architecture documentation describes the resulting structure.

- [ ] Inspect the repository and establish the agreed backend project structure.
- [ ] Configure FastAPI and centralized environment settings.
- [ ] Configure PostgreSQL, SQLAlchemy, and Alembic with an initial migration.
- [ ] Configure Redis and Celery for background processing.
- [ ] Add Docker Compose for the local development services.
- [ ] Add health checks, foundation tests, and architecture documentation.
- **Test gate:** Run Ruff and relevant pytest tests; verify local startup and health checks.
- **Evidence / results:** Not started.
- **Blockers / decisions:** None recorded.

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

## Decision and blocker log

Add decisions that affect implementation and unresolved blockers here. Link to a decision record under `docs/decisions/` if a significant architectural choice needs a permanent rationale.

| Date | Type | Topic | Decision / blocker | Status |
|---|---|---|---|---|
| — | — | — | No open decisions or blockers recorded. | — |

## Milestone closeout record

At the end of each milestone, add a dated entry with the files changed, decisions made, how to run the result, the purpose of each new module, test/lint commands and their actual output, open issues, what the user should review, and a suggested commit message. Do not create commits unless explicitly asked.
