---
name: rf-skill-governance
description: Use when recording available Codex skills, selecting skills for a ResearchFlow task, or logging which skills were used in a project or framework update.
---

# RF Skill Governance

Skill governance keeps ResearchFlow aware of available agent skills and where they worked.

## Workflow

1. Read `rf.yaml`.
2. Use `commands/skill-inventory.md` to snapshot available skills.
3. Use `commands/skill-select.md` before non-obvious skill choices.
4. Use `commands/skill-usage-log.md` after a meaningful task or milestone.
5. Link project-local usage to the global `indexes/skill-usage.index.jsonl`.

## Rules

- Inventory is a snapshot, not a guarantee of future availability.
- Usage records need both `project_path` and `researchflow_project_entry`.
- Project-local records mirror global records; they do not replace them.
- Skill usage is evidence for future planning, not a universal rule by itself.
