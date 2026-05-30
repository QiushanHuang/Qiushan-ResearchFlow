# Command: Skill Usage Log

Use this whenever a skill choice is useful for future retrospectives or project planning.

## Required Context

- `project_id`
- `project_path`
- `researchflow_project_entry`
- `usage_scope`: `framework | project | cross_project`
- `task_type`
- `skill_ids`
- `outcome`

## Project-Local Mirror

If the current project has `.researchflow/project.rf.yaml`, also write or update:

```text
<project-root>/.researchflow/skills/usage.index.jsonl
```

The global ResearchFlow record remains in `indexes/skill-usage.index.jsonl`.

## Do Not

- Do not log secrets, tokens, private server details, or irrelevant skill chatter.
- Do not claim a skill was effective unless the outcome supports it.
