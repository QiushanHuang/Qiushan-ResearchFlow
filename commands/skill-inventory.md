# Command: Skill Inventory

Use this to record which Codex skills are available in a session and how they should be selected for future projects.

## Do

- Snapshot available skill names, source roots, paths, and trigger summaries.
- Group skills by task type for low-token lookup.
- Add high-value entries to `indexes/skill.index.jsonl`.
- Treat inventory as session-specific. Availability can change by machine, plugin, or Codex session.

## Output

```yaml
inventory_id:
created_at:
source:
skill_count:
groups:
  - name:
    skills:
```

## Storage

- Snapshot: `skills-registry/inventory/`
- Index: `indexes/skill.index.jsonl`
