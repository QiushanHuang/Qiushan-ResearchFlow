---
name: rf-intake-router
description: Use when starting a ResearchFlow task, choosing task tier, selecting the read scope, or deciding whether a request needs the VAF workflow.
---

# RF Intake Router

This is the single entry skill for ResearchFlow tasks.

## Workflow

1. Read `rf.yaml`.
2. Follow `commands/intake.md`.
3. Follow `commands/triage.md`.
4. Assign T0-T3 using `framework/tiering.md`.
5. Route to:
   - T0: direct answer.
   - T1/T2/T3: `rf-vaf-workflow`.
   - Context-heavy tasks: `rf-knowledge-access`.
   - Memory or upgrade proposals: `rf-memory-upgrade-governance`.

## Hard Limits

- Do not apply memory.
- Do not apply upgrades.
- Do not recursively scan experiments or research sources.

