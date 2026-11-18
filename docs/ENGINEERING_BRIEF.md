# Knowcast — Phase 1 Engineering Brief
## Build the Newsletter-to-Audio Backend Engine

Act as a senior backend engineer and software architect. You are responsible for designing and implementing **Phase 1 of Knowcast**, a production-minded newsletter-to-audio learning platform.

This is a significant portfolio project intended to demonstrate strong backend engineering, AI integration, system design, reliability, testing, and engineering practices relevant to Senior Software Engineer and Forward Deployed Engineer roles.

Do not treat this as a quick prototype or generate everything in one unstructured pass. Build it incrementally, with clear module boundaries, tests, documentation, and working integrations.

---

# 1. Product Overview

Knowcast converts technical newsletters into audio learning experiences.

The initial supported newsletter is **ByteByteGo**. The architecture must make it straightforward to add other newsletter providers later, such as Substack and other technical newsletter platforms.

A user should eventually be able to:

1. Submit a newsletter URL.
2. Forward a newsletter email to a Knowcast address.
3. Have the system extract and normalize its content.
4. Preserve the original order of text, headings, images, diagrams, code, and lists.
5. Use Gemini to generate explanations for relevant technical images and diagrams.
6. Generate natural-sounding audio narration using Gemini TTS.
7. Store the generated audio securely.
8. Retrieve and stream the audio from a mobile application.

**Phase 1 is strictly the backend content-to-audio engine.**

Do not implement the React Native application, mobile UI, user-facing authentication flows, subscriptions, payments, or contextual AI chat in this phase.

However, design the backend APIs and data models so those features can be added without major architectural changes.

---

# 2. Technology Stack

Use the following stack unless a technical limitation justifies a documented alternative.

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Redis
- Celery for background processing

### AI
- Google Gemini API
- Gemini models on the available free tier initially
- Gemini multimodal capabilities for image understanding
- Gemini TTS for audio generation

Important:
- Do not hardcode model identifiers throughout the application.
- Read model identifiers from environment variables.
- Verify that the selected models are currently supported by the Gemini API and that the required capabilities are available.
- Do not assume every model supports image input, structured output, search grounding, or speech generation.
- Make provider-specific implementations responsible for handling their respective API differences.
- Design the AI layer so OpenAI or another provider can be added later without changing business logic.

### Content extraction
- httpx
- BeautifulSoup
- Trafilatura where appropriate
- Source-specific extraction adapters

### Audio processing
- FFmpeg
- MP3 output
- Segment-level audio generation and metadata

### Storage
- S3-compatible object storage abstraction
- MinIO for local development
- AWS S3 or Cloudflare R2 can be configured later

### Email ingestion
- Resend inbound email webhook
- Signature verification
- HTML/plain-text email parsing

### Development and infrastructure
- Docker
- Docker Compose
- pytest
- Ruff
- Type checking where practical
- Structured logging

---

# 3. Architecture Requirements

Build a **modular monolith**, not microservices.

Use clear separation between:

- API layer
- Business logic/services
- Database models and repositories
- Newsletter source providers
- AI providers
- Audio processing
- Storage providers
- Background workers

Use dependency injection where it improves testability.

Avoid:
- Large files containing unrelated functionality.
- Business logic inside API route handlers.
- Direct Gemini API calls scattered throughout the codebase.
- Hardcoded secrets, URLs, or model identifiers.
- Unnecessary abstractions that make a small system harder to understand.
- Premature microservice architecture.

Use async APIs where appropriate, but do not force asynchronous execution into libraries that do not support it properly.

---

# 4. Proposed Repository Structure

Start with the following structure and refine it if necessary. Document any meaningful changes.

```text
knowcast/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── providers/
│   │   │   ├── newsletters/
│   │   │   ├── llm/
│   │   │   ├── vision/
│   │   │   ├── tts/
│   │   │   └── storage/
│   │   ├── services/
│   │   │   ├── ingestion/
│   │   │   ├── extraction/
│   │   │   ├── image_processing/
│   │   │   └── audio/
│   │   ├── workers/
│   │   └── main.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── fixtures/
│   ├── migrations/
│   ├── Dockerfile
│   └── requirements.txt
├── infrastructure/
│   ├── docker-compose.yml
│   └── README.md
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   ├── api.md
│   ├── decisions/
│   └── evaluation/
├── .env.example
├── .gitignore
└── README.md
```

Keep configuration centralized. Use environment-specific configuration and Pydantic settings.

---

# 5. Core Domain Model

Every newsletter source must eventually produce the same normalized document representation.

Use Pydantic schemas for application-level data validation.

A simplified conceptual model:

```python
from typing import Literal
from pydantic import BaseModel

class ContentBlock(BaseModel):
    id: str
    type: Literal[
        "heading",
        "paragraph",
        "image",
        "code",
        "list"
    ]

    position: int

    text: str | None = None
    level: int | None = None

    original_url: str | None = None
    storage_key: str | None = None
    alt_text: str | None = None
    caption: str | None = None
    ai_description: str | None = None
    narration: str | None = None

    code: str | None = None
    language: str | None = None

    items: list[str] | None = None


class NewsletterDocument(BaseModel):
    id: str
    source_id: str

    title: str
    author: str | None = None
    published_at: str | None = None
    original_url: str | None = None

    blocks: list[ContentBlock]

    processing_status: str
```

Treat this as a conceptual starting point. Improve the schema where necessary.

Requirements:

- Preserve original content order.
- Every block must have a stable identifier and position.
- Preserve useful original metadata.
- Preserve image references and attribution information.
- Do not discard code snippets or technical lists.
- Keep extracted content separate from AI-generated descriptions.
- Do not overwrite original text with generated narration.
- Make the normalized document independent of its original newsletter provider.

---

# 6. Newsletter Ingestion

Implement two ingestion entry points that eventually feed the same processing pipeline.

## A. URL ingestion

Endpoint:

`POST /api/v1/ingestion/url`

Input:

```json
{
  "url": "https://example.com/newsletter"
}
```

Expected behavior:

1. Validate the URL.
2. Reject unsupported protocols and unsafe destinations.
3. Identify the newsletter provider.
4. Select the appropriate provider adapter.
5. Fetch publicly accessible or user-authorized content.
6. Extract the newsletter.
7. Create an ingestion job.
8. Enqueue processing.
9. Return a job identifier immediately.

Do not bypass authentication, subscriptions, paywalls, or publisher access restrictions.

### SSRF protection

This is a security-critical feature.

Protect URL ingestion against:
- localhost destinations
- private IP ranges
- link-local addresses
- internal network services
- malicious redirects
- DNS rebinding where practical
- unsupported URL schemes

Validate the resolved destination and redirects, not only the original hostname.

Apply timeouts, response-size limits, content-type validation, and download limits.

## B. Newsletter provider architecture

Create a provider abstraction.

Conceptual example:

```python
from abc import ABC, abstractmethod

class NewsletterProvider(ABC):

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        pass

    @abstractmethod
    async def fetch(self, url: str):
        pass

    @abstractmethod
    async def extract(self, raw_content):
        pass
```

Implement:
- ByteByteGo provider first.
- A clean registration mechanism for future providers.
- Provider-specific extraction logic.
- A common normalized output.

Do not create separate ingestion pipelines for each newsletter source.

For ByteByteGo, extract:
- Newsletter title
- Author
- Publication date
- Headings and subheadings
- Paragraphs
- Lists
- Images
- Image captions and alt text
- Code snippets
- Relevant links

Use a combination of semantic HTML parsing and source-specific selectors.

Do not rely entirely on fragile CSS selectors.

Create HTML fixtures for testing. Include multiple newsletter examples.

## C. Email ingestion

Endpoint:

`POST /api/v1/ingestion/email/webhook`

Use Resend inbound email.

Requirements:
- Verify webhook signatures.
- Parse HTML and plain-text content.
- Extract inline images.
- Handle attachments safely.
- Normalize email content into the same document model.
- Deduplicate messages.
- Track sender and message metadata.
- Apply attachment and request size limits.
- Make webhook processing idempotent.

Do not build Gmail OAuth in Phase 1.

Keep the email provider integration separate from the newsletter provider abstraction.

Document the Resend setup required for local development and deployment.

---

# 7. Image Processing and AI Explanations

Technical newsletters frequently contain architecture diagrams, system design illustrations, charts, and infographics.

The objective is to make these useful during audio narration.

Implement an image-processing pipeline.

### Image download and validation

For each relevant image:

1. Download the original image.
2. Validate the content type.
3. Apply file-size and dimension limits.
4. Reject unsupported or dangerous formats.
5. Deduplicate where practical.
6. Preserve the original URL and attribution.
7. Store the original image in object storage.

Do not fail the entire newsletter because one image fails processing.

### Image classification

Determine whether the image is:
- Technical diagram
- Architecture diagram
- Chart
- Infographic
- Screenshot
- Decorative image
- Other

Avoid narrating decorative images.

### Gemini vision integration

Send the image together with:
- Newsletter title
- Surrounding paragraph
- Previous and next relevant content blocks
- Image caption and alt text when available

Ask Gemini to return structured information.

Conceptual output:

```json
{
  "image_type": "architecture_diagram",
  "summary": "A distributed caching architecture",
  "key_components": [
    "Client",
    "Load balancer",
    "Cache cluster",
    "Database"
  ],
  "explanation": "Detailed technical explanation...",
  "narration": "Let's look at how this architecture works..."
}
```

Requirements:

- Validate AI responses against a schema.
- Handle malformed responses and API failures.
- Do not invent components that are not visible.
- Distinguish visual observations from contextual assumptions.
- Preserve the original image.
- Save AI descriptions separately.
- Make model and generation configuration configurable.

Keep the image provider behind a `VisionProvider` interface.

---

# 8. Audio Generation Pipeline

This is one of the most important parts of Knowcast.

The pipeline should convert the normalized newsletter into natural audio while preserving the original reading order.

Implement the following stages:

### Stage 1: Content preparation

- Clean extraction artifacts.
- Remove navigation, advertisements, irrelevant footers, and duplicated text.
- Preserve meaningful headings and lists.
- Preserve technical terms, code, and acronyms.
- Avoid reading URLs and HTML artifacts aloud.

### Stage 2: Narration script generation

Build a narration script from the ordered content blocks.

For image blocks:
- Include the AI-generated narration when relevant.
- Introduce diagrams naturally.
- Keep explanations connected to surrounding text.

For code blocks:
- Do not blindly read long source-code snippets character by character.
- Use a configurable narration strategy.
- Initially, explain the code's purpose or introduce it without reading every symbol.

Store the narration script separately from the original document.

### Stage 3: Segmentation

Split narration at logical boundaries:
- Headings
- Paragraphs
- Image explanations
- Sections

Keep segments within the model's documented input limits.

Each segment must have:
- Stable ID
- Source block ID
- Sequence position
- Narration text
- Generation status
- Duration
- Audio storage key

### Stage 4: TTS

Create a provider abstraction:

```python
from abc import ABC, abstractmethod

class TTSProvider(ABC):

    @abstractmethod
    async def generate_audio(
        self,
        text: str,
        voice: str,
        configuration: dict
    ) -> bytes:
        pass
```

Implement Gemini TTS first.

Requirements:
- Model identifier from environment configuration.
- Configurable voice.
- Configurable speaking style where supported.
- Proper error handling.
- Rate-limit handling.
- Retry with exponential backoff where appropriate.
- Respect the model's input limits.
- Track model usage and estimated cost where available.

Do not assume all TTS providers return identical audio formats.

Normalize provider output before it reaches the audio assembly service.

### Stage 5: Audio encoding and assembly

Use FFmpeg.

Requirements:
- Normalize audio format.
- Produce MP3.
- Normalize sample rate and bitrate.
- Concatenate segments in the correct order.
- Extract total duration.
- Store the final audio asset.
- Retain individual audio segments.

Segment-level regeneration must be possible without regenerating the entire newsletter.

Do not claim to support word-level synchronization in Phase 1.

Implement segment-level timing only.

### Stage 6: Reliability

Make audio generation:
- Idempotent.
- Retryable.
- Resumable after worker failures.
- Independently recoverable at segment level.

A failed segment should not require successful segments to be regenerated.

Persist job and segment states in the database.

---

# 9. Database Design

Use PostgreSQL with SQLAlchemy 2.x and Alembic migrations.

Start with these entities:

### users
- id
- email
- created_at

### sources
- id
- user_id
- provider
- name
- ingestion_type
- created_at

### newsletters
- id
- source_id
- title
- author
- published_at
- original_url
- status
- created_at
- updated_at

### content_blocks
- id
- newsletter_id
- position
- type
- content_json

### image_assets
- id
- content_block_id
- original_url
- storage_key
- image_type
- ai_description
- processing_status

### audio_assets
- id
- newsletter_id
- storage_key
- format
- duration
- status
- created_at

### audio_segments
- id
- audio_asset_id
- content_block_id
- position
- start_time
- end_time
- storage_key
- status

### ingestion_jobs
- id
- source_id
- newsletter_id
- status
- current_stage
- error
- retry_count
- created_at
- updated_at

### playback_progress
- id
- user_id
- newsletter_id
- position_seconds
- updated_at

Use UUID primary keys.

Use JSONB only where flexible structured content is genuinely useful.

Add indexes for frequently queried fields.

Add foreign keys and appropriate deletion behavior.

Enforce uniqueness and idempotency where necessary.

Design ownership relationships so user authentication and row-level security can be introduced in the mobile phase.

Do not implement a complete authentication system in Phase 1.

---

# 10. Background Jobs

Use Celery and Redis.

Newsletter processing must not block API requests.

Create background tasks for:

1. Fetching and extracting newsletter content.
2. Downloading and processing images.
3. Generating image explanations.
4. Preparing narration scripts.
5. Generating audio segments.
6. Assembling audio.
7. Updating processing status.

Define explicit job states, such as:

`queued → processing → completed`

and:

`queued → processing → failed`

Persist stage information so users can see where processing failed.

Implement:
- Retry policies
- Task idempotency
- Timeouts
- Structured errors
- Correlation IDs
- Safe handling of worker restarts

Avoid passing large image or audio byte arrays through Redis task messages. Pass database identifiers and storage keys instead.

---

# 11. Object Storage and Audio Streaming

Create an abstract storage provider.

Implement:
- Local MinIO storage for development.
- An S3-compatible production implementation.

Store:
- Original images
- Generated audio segments
- Final assembled MP3

Do not store audio binaries in PostgreSQL.

Keep storage buckets private.

Generate short-lived signed URLs for audio playback.

Implement:

`GET /api/v1/newsletters/{id}/audio`

`POST /api/v1/audio/{id}/refresh-url`

The API should return:
- Audio asset ID
- Signed URL
- Duration
- Format
- Relevant metadata

Design for HTTP range requests so a future React Native audio player can seek through an MP3.

Verify that the selected storage provider and delivery path actually support the required range-request behavior.

Do not implement HLS in Phase 1.

---

# 12. API Endpoints

Implement the following Phase 1 API surface.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/ingestion/url` | Submit newsletter URL |
| POST | `/api/v1/ingestion/email/webhook` | Receive forwarded newsletter |
| GET | `/api/v1/jobs/{id}` | Retrieve processing status |
| GET | `/api/v1/newsletters` | List newsletters |
| GET | `/api/v1/newsletters/{id}` | Retrieve normalized newsletter |
| GET | `/api/v1/newsletters/{id}/audio` | Retrieve audio playback information |
| POST | `/api/v1/audio/{id}/refresh-url` | Refresh signed audio URL |
| PUT | `/api/v1/playback/{id}` | Save playback position |

Use versioned routes.

Use consistent response schemas and HTTP status codes.

Implement pagination for newsletter listing.

Validate all incoming data.

Return useful error responses without exposing internal exceptions or secrets.

Use OpenAPI documentation generated by FastAPI.

---

# 13. Gemini Provider Architecture

Create separate interfaces for:

- LLM
- Vision
- TTS

Example:

```python
class LLMProvider:
    async def generate(self, request):
        raise NotImplementedError


class VisionProvider:
    async def explain_image(self, request):
        raise NotImplementedError


class TTSProvider:
    async def generate_audio(self, request):
        raise NotImplementedError
```

Implement Gemini adapters first.

Use environment configuration such as:

```env
AI_PROVIDER=gemini

GEMINI_API_KEY=

GEMINI_TEXT_MODEL=
GEMINI_VISION_MODEL=
GEMINI_TTS_MODEL=

GEMINI_TTS_VOICE=

```

The model names above are intentionally configurable. Verify the current Gemini model identifiers, API methods, and free-tier availability before implementing integrations.

Do not hardcode the model selection inside business logic.

The application should be able to switch providers through configuration and dependency injection.

Normalize provider responses into application-owned schemas.

Account for:
- Different input formats
- Different response formats
- Different token limits
- Different audio formats
- Different error types
- Different rate limits

Do not implement an OpenAI provider yet.

---

# 14. Observability and Cost Tracking

Build basic observability from the beginning.

Track:
- Ingestion job duration
- Extraction duration
- Number of content blocks
- Number of images processed
- Number of AI calls
- Model identifiers
- Token usage when available
- Audio generation duration
- Generated audio duration
- Retry counts
- Processing failures
- Estimated cost where pricing information is available

Use structured logs.

Never log:
- API keys
- Signed URLs
- Sensitive user content unnecessarily
- Email authentication tokens

Create a provider usage record or an equivalent extensible mechanism.

Free-tier usage must be monitored. Do not assume unlimited requests.

---

# 15. Testing Strategy

Use pytest.

Testing is a core requirement, not an afterthought.

### Unit tests

Test:
- URL validation
- Provider selection
- HTML extraction
- Content normalization
- Block ordering
- Image classification
- Narration script generation
- Audio segmentation
- Storage abstraction
- Job-state transitions
- Idempotency

### Integration tests

Test:
- API submission
- Database persistence
- Celery task execution
- MinIO storage
- Audio assembly
- Signed URL generation

Mock external Gemini and Resend calls in automated tests.

Do not require paid API calls for the normal test suite.

### End-to-end tests

Use at least three ByteByteGo newsletter fixtures.

Include:
- Newsletter with several images.
- Newsletter with few or no images.
- Newsletter with code snippets and complex lists.
- Malformed HTML.
- Duplicate ingestion.
- Image download failure.
- Gemini API failure.
- TTS segment failure.
- Worker interruption and retry.
- Invalid or unsafe URLs.

Build a repeatable evaluation dataset.

Manually verify the resulting audio and image explanations against the original newsletters.

---

# 16. Evaluation Framework

Create an evaluation document and basic scripts for a dataset of at least 10 ByteByteGo newsletters.

Measure:

### Extraction
- Title and metadata accuracy.
- Content completeness.
- Block ordering.
- Image extraction completeness.
- Code and list preservation.

### Image understanding
- Correct image classification.
- Technical accuracy.
- Whether explanations are grounded in the actual diagram.
- Whether generated narration adds useful context.

### Audio
- Naturalness.
- Pronunciation of technical terminology.
- Completeness.
- Logical transitions.
- Correct ordering.
- Audio quality.

### Reliability
- Success rate.
- Retry behavior.
- Duplicate processing.
- Recovery after failure.

### Cost and performance
- Processing time per newsletter.
- AI calls per newsletter.
- Estimated cost per newsletter.
- Generated audio duration.

Do not use LLM-as-judge as the only evaluation method. Include manual human review, especially for technical diagram explanations.

---

# 17. Security and Engineering Standards

Treat security as a first-class requirement.

Implement:
- SSRF protection.
- Input validation.
- Request and download limits.
- Webhook signature verification.
- Private object storage.
- Short-lived signed URLs.
- Secret management through environment configuration.
- Safe file handling.
- SQL injection protection through parameterized ORM queries.
- Idempotent webhook and background task processing.
- Appropriate CORS configuration.
- Secure error responses.

Respect publisher access restrictions and copyright.

Do not bypass paywalls or authentication.

Design Knowcast around content users are authorized to access. Do not implement public redistribution or a public newsletter/audio library.

Do not assume that a personal subscription grants commercial redistribution rights.

---

# 18. Development Milestones

Implement the project in the following order.

Do not attempt to build every feature in one massive code-generation pass.

## Milestone 1 — Backend foundation

- Inspect the repository.
- Establish project structure.
- Configure FastAPI.
- Configure PostgreSQL.
- Configure SQLAlchemy.
- Configure Alembic.
- Configure Redis and Celery.
- Configure Docker Compose.
- Implement health checks.
- Implement environment configuration.
- Add initial migrations.
- Add initial tests.
- Write architecture documentation.

Deliverable: a backend that starts locally and passes its foundation tests.

## Milestone 2 — ByteByteGo extraction

- Implement provider interface.
- Implement ByteByteGo adapter.
- Extract metadata and content blocks.
- Preserve ordering.
- Add HTML fixtures.
- Add extraction tests.
- Add URL safety checks.

Deliverable: a ByteByteGo URL produces a validated normalized newsletter document.

## Milestone 3 — Image processing

- Download images.
- Validate and store images.
- Classify images.
- Integrate Gemini vision.
- Generate structured explanations and narration.
- Add image-processing tests.

Deliverable: relevant diagrams have stored AI explanations and narration.

## Milestone 4 — Audio generation

- Implement TTS abstraction.
- Integrate Gemini TTS.
- Build narration scripts.
- Implement segmentation.
- Generate individual audio segments.
- Normalize with FFmpeg.
- Assemble final MP3.
- Persist metadata.
- Add retry and recovery logic.

Deliverable: a normalized newsletter becomes a complete MP3.

## Milestone 5 — Storage and playback API

- Implement MinIO locally.
- Implement storage abstraction.
- Store original images and audio.
- Generate signed URLs.
- Implement playback API.
- Test seeking and range requests.

Deliverable: a generated MP3 can be retrieved and played through a signed URL.

## Milestone 6 — Email ingestion

- Integrate Resend.
- Implement webhook signature verification.
- Parse email content and images.
- Add deduplication.
- Feed email content into the common pipeline.

Deliverable: a forwarded newsletter can be processed through the same backend engine.

## Milestone 7 — End-to-end validation

- Run the full pipeline against at least three newsletters.
- Test failure and retry scenarios.
- Run the evaluation dataset.
- Fix extraction, narration, and reliability issues.
- Update architecture and API documentation.

Deliverable: a repeatable, tested Phase 1 backend.

---

# 19. Definition of Done

Phase 1 is complete only when:

1. A ByteByteGo URL can be submitted through the API.
2. The request returns a job ID without waiting for processing.
3. A background worker extracts and normalizes the newsletter.
4. Content ordering is preserved.
5. Relevant images are downloaded and stored.
6. Gemini generates structured image explanations.
7. Narration scripts are generated.
8. Gemini TTS generates individual audio segments.
9. FFmpeg assembles the segments into an MP3.
10. The final audio is stored privately.
11. The API returns a signed playback URL.
12. Audio seeking/range requests have been verified.
13. Job failures are persisted and recoverable.
14. Duplicate processing is prevented.
15. Email forwarding is supported through Resend.
16. Automated tests pass.
17. Docker Compose can run the development environment.
18. Documentation explains setup, architecture, APIs, and evaluation.

Do not mark a feature as complete if it is only represented by a placeholder, mock, or unimplemented interface.

---

# 20. How You Should Work

Follow these instructions throughout development.

### First: inspect before changing anything

Inspect:
- Existing repository structure.
- Existing source files.
- Git status.
- Existing dependencies.
- Existing configuration.
- Existing tests.

Do not overwrite existing work without understanding it.

### Second: propose an implementation plan

Before making substantial changes:
- Explain the architecture you intend to implement.
- Identify dependencies.
- Identify risks and design decisions.
- Identify any assumptions.
- Provide the milestones you intend to execute.

### Third: implement incrementally

For each milestone:

1. Explain the task.
2. Implement it.
3. Run formatting and linting.
4. Run relevant tests.
5. Fix failures.
6. Update documentation.
7. Summarize files changed and decisions made.
8. Identify any outstanding issues.

Do not silently skip tests or report tests as passing without actually running them.

### Fourth: make engineering decisions explicit

When there are multiple valid solutions:
- Prefer the simplest maintainable option.
- Explain meaningful trade-offs.
- Document important architectural decisions in `docs/decisions/`.
- Avoid unnecessary dependencies.

### Fifth: protect the project from unnecessary scope

Do not start implementing:
- React Native UI.
- Mobile authentication.
- Contextual AI chat.
- Web research.
- Subscription management.
- Payments.
- Public content sharing.
- Word-level audio synchronization.

These belong to later phases.

### Sixth: keep the code understandable

I want to understand the implementation, not just receive generated code.

Use:
- Clear naming.
- Small, focused modules.
- Type hints.
- Docstrings for non-obvious logic.
- Meaningful error handling.
- Tests that explain expected behavior.

When making a significant architectural decision, explain why it was chosen.

---

# Initial Instruction

Start by inspecting the existing repository and Git status.

Then propose the implementation plan for **Milestone 1 — Backend Foundation**.

Do not implement the entire project immediately.

Wait for my approval of the milestone plan before making substantial changes.

The goal is to build Knowcast as a well-engineered, extensible backend that I can confidently explain in a senior-level software engineering interview.