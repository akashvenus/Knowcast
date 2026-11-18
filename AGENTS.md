# AGENTS.md — Knowcast

## Project
Knowcast converts technical newsletters into audio. Phase 1 is the backend only.
The full specification is in `docs/ENGINEERING_BRIEF.md`. Read it before planning any milestone.

## The developer
The person you are working with is a junior developer who must be able to explain every line in an interview.
Prefer clarity over cleverness. Explain decisions in plain language.

## Workflow (always)
1. Inspect the repo and `git status` before changing anything.
2. Propose a plan and WAIT for approval before substantial changes.
3. Before planning, use the `edge-case-detection` skill.
4. Implement one milestone at a time. Never build several milestones in one pass.
5. After each milestone: run Ruff, run the relevant tests, fix failures, update docs.
6. Finish each milestone with a summary: files changed, decisions made, how to run it,
   what each new module does, and any open issues.
7. Never claim tests pass unless you actually ran them. Paste the real result.

## Scope (do not build in Phase 1)
React Native UI, user-facing auth, contextual AI chat, web research, subscriptions,
payments, public content sharing, word-level audio sync, HLS, an OpenAI provider.
If something seems to need these, ask instead of building it.

## Engineering rules
- Modular monolith. No microservices.
- No business logic in API route handlers. Routes call services.
- All AI calls go through the provider interfaces (LLM, Vision, TTS). Never call Gemini directly elsewhere.
- No hardcoded secrets, URLs, or model names. Use environment variables and Pydantic settings.
- Do not store binary files (images, audio) in PostgreSQL or Redis messages. Pass IDs and storage keys.
- Do not add a dependency or abstraction unless it clearly pays for itself. Explain it if you add one.
- Verify current Gemini model names and capabilities against the official docs. Do not assume them.

## Security (non-negotiable)
- SSRF protection on all URL fetching (validate resolved IPs and every redirect).
- Verify webhook signatures. Enforce request, download, and image size limits.
- Private storage buckets, short-lived signed URLs.
- Never log API keys, signed URLs, or email tokens.
- Never bypass paywalls or authentication.

## Testing
- pytest. Mock Gemini and Resend in automated tests. No paid API calls in the normal suite.
- Every new feature needs tests, including failure cases.
- A feature backed only by a placeholder or mock is NOT done. Say so honestly.

## Git
- For each new app feature, create a dedicated branch before implementation. Keep that feature's changes and commits on the branch. Run Ruff and all relevant tests; only after the required checks pass, commit the changes and push the branch to GitHub.
- Do not merge feature branches or rewrite history unless I explicitly ask.
- For work that is not a new app feature, do not run `git commit` or `git push` unless I explicitly ask.
- At the end of each milestone, tell me what to review and suggest a commit message.
- Commit format: `type: short description` (feat, fix, docs, test, refactor, chore).
  Example: `feat: establish backend foundation`
- One milestone = one or a few focused commits. Do not mix unrelated changes.
- Never commit `.env`, secrets, or generated media.

## Skills
Use these skills automatically:
- `simple-code-structure` for all code you write.
- `edge-case-detection` before planning any feature.
- `file-hierarchy` when creating or moving files, and when updating the README.
