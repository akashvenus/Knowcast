# Knowcast

Knowcast is a newsletter-to-audio backend project. Phase 1 is planned as a modular backend that extracts technical newsletters, explains relevant diagrams, and generates audio.

The current Phase 1 roadmap and progress record are in [docs/phase_tracker.md](docs/phase_tracker.md). The complete engineering requirements are in [docs/ENGINEERING_BRIEF.md](docs/ENGINEERING_BRIEF.md).

## Project Structure

```text
Knowcast/
├── .agents/                         # Project-specific agent instructions and skills
│   └── skills/                      # Workflows for edge cases, file layout, and clear code
│       ├── edge-case-detection/     # Prompts for resolving edge cases before planning
│       ├── file-hierarchy/          # Repository layout and README requirements
│       └── simple-code-structure/   # Guidelines for readable code
├── docs/                            # Project requirements and planning documents
│   ├── ENGINEERING_BRIEF.md        # Phase 1 architecture, requirements, and milestones
│   └── phase_tracker.md            # Current status, checklist, evidence, and issue history
├── AGENTS.md                        # Project workflow and engineering rules
└── README.md                        # Project overview and repository map
```

The backend folders listed in the engineering brief will be added incrementally as their milestones are approved and implemented.
