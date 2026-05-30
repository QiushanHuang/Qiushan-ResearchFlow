# Prompt: First-Run Golden Procedure

Use this prompt after a human-agent run succeeds once and may become repeatable.

## Input Contract

- `project_id`:
- `adapter_path`:
- `task_id`:
- `human_creative_decision`:
- `agent_actions_completed`:
- `files_or_artifacts_changed`:
- `validation_evidence`:
- `repeatable_steps`:
- `non_repeatable_judgment`:
- `exception_conditions`:
- `skill_usage`:

## Output Contract

- `creative_pass_id` when human judgment shaped the run;
- `golden_run_id` when the result is approved as a reference;
- procedure candidate path when repeat work is safe;
- repeat-run guardrails;
- digest and claim links;
- unresolved issues for `evolution/inbox/`.

Follow `commands/project-procedure.md` and keep first-run capture prompt-driven, not skill-driven.
