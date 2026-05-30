# Command: Skill Select

Use this before planning a task when skill choice is non-obvious or when a project has useful prior skill usage records.

## Read Order

1. `indexes/skill.index.jsonl`
2. `indexes/skill-usage.index.jsonl`
3. Project-local `.researchflow/skills/usage.index.jsonl`, if present.
4. The relevant skill `SKILL.md`, only when the trigger matches.

## Selection Output

```yaml
task_type:
candidate_skills:
selected_skills:
rejected_skills:
why_selected:
usage_log_required:
```

Prefer narrow skills with direct triggers. Record the selection if it will help future project planning.
