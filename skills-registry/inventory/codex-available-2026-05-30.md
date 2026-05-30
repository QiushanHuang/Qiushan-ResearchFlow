---
schema_version: 1
inventory_id: skill-inventory-public
kind: skill-inventory-snapshot
status: active
created_at: 2026-05-30
updated_at: 2026-05-30
read_policy: index_only
source: public_release
---

# Public Skill Inventory Snapshot

This public snapshot lists skills relevant to the ResearchFlow framework. It is a planning index, not a guarantee that every runtime has the same local skill set.

## Core Skills

- `skill-creator`
- `writing-skills`
- `test-driven-development`
- `verification-before-completion`
- `requesting-code-review`
- `subagent-driven-development`
- `dispatching-parallel-agents`
- `systematic-debugging`

## ResearchFlow Local Skills

- `rf-intake-router`
- `rf-vaf-workflow`
- `rf-knowledge-access`
- `rf-review-gate`
- `rf-memory-upgrade-governance`
- `rf-evolution-governance`
- `rf-skill-governance`
- `rf-project-interface-router`
- `rf-project-native-onboarding`
- `rf-project-legacy-onboarding`

## Selection Rule

Start from the task type, then choose the narrowest skill whose trigger matches.
