---
name: rf-project-interface-router
description: Use when a user asks in natural language to connect, adopt, register, or route a project into ResearchFlow.
---

# RF Project Interface Router

Route the project before loading project bodies.

## Decision

- Native: the project may contain `.researchflow/`.
- Legacy: the project directory must stay unchanged.

## Steps

1. Read `commands/project-interface.md`.
2. Treat natural language as the primary interface.
3. Confirm `project_root`, `project_id`, title, and write boundary.
4. Do not ask the user to run commands; run the connect and validate scripts yourself when enough information is available.
5. If local metadata is allowed, use `rf-project-native-onboarding`.
6. If no directory change is allowed, use `rf-project-legacy-onboarding`.
7. Keep `indexes/project.index.jsonl` pointer-only.
8. Record skill usage after the adapter validates.

## Mistakes To Avoid

- Do not scan large project folders during mode selection.
- Do not treat prompts as policy.
- Do not write universal memory from onboarding evidence.
