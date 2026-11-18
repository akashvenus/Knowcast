---
name: file-hierarchy
description: Use when creating, moving, or renaming files and folders, or when updating the README. Keeps the project structure simple, clean, and enterprise-style, and documents it in the README.
---

# File Hierarchy

## Rules
1. Follow the structure in `docs/ENGINEERING_BRIEF.md` section 4. Do not invent new top-level folders.
2. Organize by responsibility (api, services, repositories, providers, models, schemas, workers),
   not by file type or by feature name alone.
3. One clear responsibility per file. Split a file when it grows past roughly 300 lines or mixes concerns.
4. Keep nesting shallow. Do not add a folder for a single file unless the brief calls for it.
5. Use `snake_case` for Python files and folders. Names should say what the file does.
6. Tests mirror the app structure: `tests/unit/...` matches `app/...`.
7. Never put secrets, generated media, or local data in the repo. Keep `.env.example` current.
8. Every package folder that needs it has an `__init__.py`.
9. Any meaningful deviation from the brief's structure is recorded in `docs/decisions/`.

## README requirement
The root `README.md` must contain a "Project Structure" section with:
- The current folder tree in a code block, updated whenever files are added, moved, or removed.
- One line next to each folder explaining its purpose, for example:

```text
backend/app/
├── api/v1/        # HTTP routes only, no business logic
├── services/      # Business logic
├── repositories/  # Database access
├── providers/     # External integrations (Gemini, storage, newsletters)
└── workers/       # Celery background tasks
```

## Before finishing
Compare the README tree with the real folders and fix any mismatch.