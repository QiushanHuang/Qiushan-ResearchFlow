# Command: Project Interface

Use this when a project must be connected to ResearchFlow and the correct adapter mode is not already settled.

## Reusable Actions

| Action | Route |
|---|---|
| `rf_project_interface` | Select native or legacy mode, then run the matching connect path |
| `rf_project_native_connect` | Use `commands/project-connect.md` with `--mode native` or omitted mode |
| `rf_project_legacy_connect` | Use `commands/project-connect.md` with `--mode legacy` |
| `rf_project_first_run_capture` | Use `prompts/project-interface/first-run-golden-procedure.md` |
| `rf_project_skill_retrospective` | Use `prompts/project-interface/skill-retrospective.md` |

## Natural Language Entry

The normal user interface is natural language. The user should not need to run shell commands, copy command blocks, or manually choose script arguments.

When the user says they want to connect, adopt, register, 接入, 兼容接入, or start using ResearchFlow for a project, the agent runs this interface:

1. infer whether the current Codex workspace is the target project or ResearchFlow itself;
2. read `prompts/project-interface/natural-language-connect.md`;
3. choose native mode when project-local `.researchflow/` is allowed;
4. choose legacy mode when the target directory must not change;
5. ask only for missing required facts that cannot be inferred safely;
6. agent runs the connect and validate scripts;
7. report adapter path, mode, validation result, and logs written.

If the user gives a full request in natural language, do not answer with shell commands as the primary result. Run the workflow and summarize the outcome.

## Mode Selection

Use native mode when the project may contain a local `.researchflow/` folder. Use legacy mode when the target project directory must not change.

Native adapter:

```text
<project-root>/.researchflow/project.rf.yaml
```

Legacy shadow adapter:

```text
agent-framework/researchflow/project-interfaces/legacy/<safe-project-id>/project.rf.yaml
```

## Native Route

1. Use `skills/rf-project-native-onboarding/SKILL.md`.
2. Fill `prompts/project-interface/native-new-project.md`.
3. Run `commands/project-connect.md` with native mode.
4. Validate with `scripts/rf_project_validate.py --strict`.
5. Log skill usage globally and project-locally when the project adapter exists.

## Legacy Route

1. Use `skills/rf-project-legacy-onboarding/SKILL.md`.
2. Fill `prompts/project-interface/legacy-shadow-project.md`.
3. Run `commands/project-connect.md` with `--mode legacy`.
4. Confirm no `.researchflow/` was created inside the target project.
5. Validate with `scripts/rf_project_validate.py --strict`.
6. Log skill usage in the ResearchFlow global registry.

## First-Run Capture

After a human-agent run succeeds, use `prompts/project-interface/first-run-golden-procedure.md` and `templates/first-run-golden-procedure.md` to decide whether it should become a golden run, a procedure candidate, or only a digest.

## Logging

Every project interface run records:

- selected mode;
- adapter path;
- project root;
- skills used;
- validation command and result;
- unresolved gaps routed to `evolution/inbox/`.

## Guardrails

- Global `indexes/project.index.jsonl` is pointer-only.
- Legacy mode never writes under `project_root`.
- Prompts do not override `framework/` or `commands/` policy.
- Memory and framework upgrades still require proposal, review, and apply records.
