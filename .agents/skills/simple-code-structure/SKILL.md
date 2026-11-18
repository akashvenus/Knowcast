---
name: simple-code-structure
description: Use whenever writing or modifying code. Keeps code simple, readable, and explained, suitable for a junior developer who must understand and explain every line.
---

# Simple Code Structure

The reader is a junior developer. Write code they can read once and understand.

## Rules
1. Prefer the plain, obvious solution over the short or clever one.
2. Use explicit loops and named variables instead of dense one-liners.
3. Avoid nested comprehensions, chained ternaries, and deep nesting. Use early returns instead.
4. Keep functions small and single-purpose. If a function needs a long comment to explain what it does, split it.
5. Use descriptive names (`download_image`, not `dl`). No unexplained abbreviations.
6. Add type hints everywhere. Add a short docstring to every public function and class.
7. Do not add abstractions, decorators, metaclasses, or generics unless the task truly needs them.
8. Do not add a dependency when the standard library does the job.

## When a non-obvious technique is genuinely needed
Examples: async context managers, decorators, `functools`, generators, dependency injection tricks,
regex, bit operations, SQLAlchemy loading options, Celery task options.

Add a block comment directly above it using this format:

```python
# NON-OBVIOUS: <name of the technique>
# What it does: <plain-language explanation, step by step>
# Why it is used here: <the problem it solves>
# Related code: <file and function names that depend on or call this>
# Simpler alternative: <what you could write instead and why it was not chosen>
```

## Before finishing
- Re-read the code as a beginner. Anything surprising must be simplified or commented.
- In your milestone summary, list every `NON-OBVIOUS` comment you added.