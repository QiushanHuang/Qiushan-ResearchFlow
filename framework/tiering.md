# T0-T3 Task Tiering

Use the lowest sufficient tier.

| Tier | Use When | Flow | Review |
|---|---|---|---|
| T0 | Answering, explaining, rewriting, tiny reversible advice. | Direct answer. | None. |
| T1 | Small local file/doc task, simple command, low-risk lookup. | Brief plan, run, self-check. | Optional. |
| T2 | Multi-step task, multiple files, research evidence, experiment interpretation, project impact. | Plan, run, digest, claim, review. | Required. |
| T3 | Long-term memory, framework changes, cross-project transfer, architecture, self-upgrade, high risk. | Multi-agent review, user confirmation, proposal/apply split. | Required plus human gate. |

## Upgrade Triggers

- T0 -> T1: filesystem, command execution, external lookup, or durable output.
- T1 -> T2: multiple files, tests, evidence evaluation, experiment analysis, or nontrivial risk.
- T2 -> T3: memory writes, self-upgrade, architecture, permissions, security, cross-project claims, or irreversible changes.

## Downgrade Conditions

Downgrade if the goal is explicit, impact is local, failure cost is low, verification is simple, and no long-term state changes are involved.

## T3 Hard Gates

T3 tasks require:

- explicit plan
- review
- user confirmation for key decisions
- proposal/apply split for memory or framework changes
- rollback or supersession record

