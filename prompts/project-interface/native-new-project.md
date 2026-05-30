# Prompt: Native New Project

Use this prompt before `rf_project_native_connect`.

## Input Contract

- `project_id`:
- `title`:
- `project_root`:
- `human_goal`:
- `allowed_writes`: `.researchflow/**`
- `forbidden_writes`:
- `initial_domains`:
- `expected_artifact_types`:
- `privacy_constraints`:
- `skills_to_consider`:
- `validation_command`: `python3 agent-framework/researchflow/scripts/rf_project_validate.py --framework-root agent-framework/researchflow --adapter <project-root>/.researchflow/project.rf.yaml --strict`

## Output Contract

- selected mode: native;
- adapter path;
- index files created;
- first-run capture need;
- skill usage log path;
- unresolved issues for `evolution/inbox/`.

Follow `commands/project-interface.md`, `commands/project-connect.md`, and `framework/cross-project-boundaries.md`.
