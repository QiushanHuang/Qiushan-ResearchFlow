---
name: rf-evolution-governance
description: Use when capturing ResearchFlow feedback, bugs, user preferences, self-check findings, unresolved issues, or candidate memory and upgrade signals.
---

# RF Evolution Governance

`evolution/` is a signal layer. It records what was noticed, how it was triaged, what was done, and what may need memory or framework change.

## Workflow

1. Read `rf.yaml`.
2. Use `commands/evolution-capture.md` for raw signals.
3. Use `commands/evolution-triage.md` to create normalized items.
4. Use `commands/evolution-candidate.md` for memory, upgrade, action, library, project, or resource candidates.
5. Use `commands/evolution-journal.md` after substantial maintenance work.
6. Use `commands/evolution-resolve.md` only when evidence supports closure.
7. Use `commands/evolution-self-check.md` for autonomous summaries.

## Hard Limits

- Do not apply memory.
- Do not apply framework upgrades.
- Do not mark `resolved` without `resolution_evidence`.
- Do not turn cross-project links, RSS, library sources, or evolution records into current-project facts.
- Do not treat agent habit candidates as active memory unless the user approves the memory proposal and apply record.
