# Command: Reusable Actions

Reusable actions are stable verbal handles for repeated ResearchFlow operations. They are not all separate command files.

## Action Names

| Action | Route |
|---|---|
| `rf_intake` | `commands/intake.md` |
| `rf_triage` | `commands/triage.md` |
| `rf_context_load` | `commands/context-load.md` |
| `rf_plan` | `commands/plan.md` |
| `rf_run` | `commands/run.md` |
| `rf_digest` | `commands/digest.md` |
| `rf_claim` | `commands/claim.md` |
| `rf_review` | `commands/review.md` |
| `rf_memory_propose` | `commands/memory-propose.md` |
| `rf_memory_apply` | `commands/memory-apply.md` |
| `rf_upgrade_propose` | `commands/upgrade-propose.md` |
| `rf_upgrade_apply` | `commands/upgrade-apply.md` |
| `rf_library_add_source` | source card plus `indexes/library.index.jsonl` |
| `rf_rss_add_feed` | RSS source card only |
| `rf_validate` | `commands/validate.md` and `scripts/rf_validate.py` |
| `rf_evolution_capture` | `commands/evolution-capture.md` |
| `rf_evolution_candidate` | `commands/evolution-candidate.md` |
| `rf_project_link` | `indexes/project-link.index.jsonl` pointer only |
| `rf_subagent_round` | role, round, independent memo, review synthesis |
| `rf_subagent_five_pass_review` | `commands/subagent-five-pass-review.md` |
| `rf_normalize_user_signal` | `commands/evolution-capture.md` |
| `rf_skill_inventory` | `commands/skill-inventory.md` |
| `rf_skill_select` | `commands/skill-select.md` |
| `rf_skill_usage_log` | `commands/skill-usage-log.md` |
| `rf_project_interface` | `commands/project-interface.md` |
| `rf_project_native_connect` | `commands/project-connect.md` with native mode |
| `rf_project_legacy_connect` | `commands/project-connect.md` with legacy mode |
| `rf_project_first_run_capture` | `prompts/project-interface/first-run-golden-procedure.md` |
| `rf_project_connect` | `commands/project-connect.md` |
| `rf_project_procedure` | `commands/project-procedure.md` |

## Naming Rule

Use `rf_<verb>_<object>`. A reusable action is a recall handle for the user and the agent. It does not imply automatic execution, memory application, or framework upgrade.

## High-Frequency Personal Actions

`rf_subagent_five_pass_review` means:

1. Use multiple `gpt-5.5` `xhigh` subagents when the user explicitly asks for this action or equivalent wording.
2. Have them decompose the same problem independently.
3. Exchange and critique the results.
4. Run 5 full review iterations before the next implementation or decision phase.
5. After the next phase, repeat the whole review flow once at the overall-system level.

`rf_normalize_user_signal` means:

1. Preserve the user's raw wording when capturing an evolution signal.
2. Add a concise `Normalized Intent` section that fixes typos, removes repetition, and clarifies structure.
3. Do not invent meaning. Keep uncertainty under `Ambiguities`.

`rf_skill_usage_log` means:

1. Record which skills were used.
2. Include both the project path and ResearchFlow project entry.
3. State why the skills were selected and what outcome they produced.
4. Mirror to project-local `.researchflow/skills/usage.index.jsonl` when that project adapter exists.

`rf_project_interface` means:

1. Treat the user's natural-language request as the interface.
2. Select native or legacy mode before onboarding.
3. Use native mode when `.researchflow/` may live inside the project.
4. Use legacy mode when the target directory must stay unchanged.
5. Run the connect and validate scripts internally.
6. Validate the adapter and record skill usage before treating the project as connected.
