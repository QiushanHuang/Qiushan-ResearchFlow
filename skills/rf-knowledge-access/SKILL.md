---
name: rf-knowledge-access
description: Use when a ResearchFlow task needs project indexes, research-library pointers, experiments, RSS issues, artifacts, or any context loading decision.
---

# RF Knowledge Access

Use VKF-like access: view indexes first, fetch evidence on demand.

## Workflow

1. Read `framework/context-loading.md`.
2. Read root indexes in `indexes/`.
3. For research, prefer `library/` indexes and notes before source bodies.
4. For experiments, prefer registry, digest, and claim indexes before run files.
5. For RSS, treat summaries as leads and preserve original links.
6. Record opened and excluded context using `commands/context-load.md`.

## Hard Limits

- Do not treat research-library notes as project facts.
- Do not treat RSS summaries as source truth.
- Do not recursively scan large experiment folders.
- Do not read skipped paths unless the task requires specific evidence.

