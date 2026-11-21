# Knowcast

Knowcast is a newsletter-to-audio backend project. Phase 1 is planned as a modular backend that extracts technical newsletters, explains relevant diagrams, and generates audio.

The current Phase 1 roadmap and progress record are in [docs/phase_tracker.md](docs/phase_tracker.md). The complete engineering requirements are in [docs/ENGINEERING_BRIEF.md](docs/ENGINEERING_BRIEF.md).

## Project Structure

```text
Knowcast/
├── .agents/                         # Project instructions and development skills
├── backend/
│   ├── app/
│   │   ├── api/                      # Health route
│   │   ├── core/                     # Pydantic application settings
│   │   ├── db/                       # Declarative metadata and DB sessions
│   │   ├── models/                   # Nine PostgreSQL entity models
│   │   ├── workers/                  # Celery app and background task modules
│   │   └── main.py                   # FastAPI app factory and ASGI entry point
│   ├── migrations/
│   │   ├── versions/                 # Initial schema migration
│   │   └── env.py                    # Alembic settings and metadata wiring
│   ├── tests/
│   │   ├── integration/              # Disposable PostgreSQL and Redis checks
│   │   └── unit/                     # API, settings, database, model, and worker tests
│   ├── alembic.ini                   # Migration tool configuration
│   └── requirements.txt              # Backend and development dependencies
├── docs/
│   ├── ENGINEERING_BRIEF.md          # Phase 1 requirements
│   └── phase_tracker.md              # Roadmap, evidence, and issue history
├── .env.example                      # Safe local settings template
├── .gitignore                        # Excludes local secrets and generated files
├── AGENTS.md                         # Project workflow and engineering rules
├── pyproject.toml                    # Ruff and pytest configuration
└── README.md                         # Overview and repository map
```

Folders for the remaining backend features will be added as their milestones are approved.
