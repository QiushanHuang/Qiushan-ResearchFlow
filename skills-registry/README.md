# Skills Registry

`skills-registry/` records which Codex skills are available, which skills were used in which projects, and what skill combinations worked for recurring task types.

## Layers

- `inventory/`: snapshots of available Codex skills and trigger summaries.
- `usage/`: framework-level usage records keyed by project, path, task type, and outcome.
- `selection/`: optional notes explaining why skills were selected or rejected.

## Project-Local Mirror

Each project can also keep:

```text
<project-root>/.researchflow/skills/usage.index.jsonl
<project-root>/.researchflow/skills/usage/*.md
```

The framework-level usage entry must still include:

- `project_id`
- `project_path`
- `researchflow_project_entry`
- `usage_scope`
- `skill_ids`
- `task_type`
- `outcome`

This makes project retrospectives and new-project planning faster without loading old conversations.
