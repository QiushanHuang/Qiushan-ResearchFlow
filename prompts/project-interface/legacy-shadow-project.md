# Prompt: Legacy Shadow Project

Use this prompt before `rf_project_legacy_connect`.

## Input Contract

- `project_id`:
- `title`:
- `project_root`:
- `reason_no_directory_change`:
- `allowed_writes`: `agent-framework/researchflow/project-interfaces/legacy/<safe-project-id>/**`
- `forbidden_writes`: `<project-root>/**`
- `known_large_paths`: `logs/**`, `raw/**`, `artifacts/**`, checkpoints, arrays, dependency folders
- `privacy_constraints`:
- `skills_to_consider`:
- `validation_command`: `python3 agent-framework/researchflow/scripts/rf_project_validate.py --framework-root agent-framework/researchflow --adapter agent-framework/researchflow/project-interfaces/legacy/<safe-project-id>/project.rf.yaml --strict`

## Output Contract

- selected mode: legacy;
- adapter path;
- no-touch confirmation;
- index files created under ResearchFlow;
- skill usage log path;
- unresolved issues for `evolution/inbox/`.

Follow `commands/project-interface.md`, `commands/project-connect.md`, and `framework/cross-project-boundaries.md`.
