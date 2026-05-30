# State Machine

The main flow is:

```text
intake -> triage -> plan -> run -> digest -> claim -> review -> done
```

## States

| State | Meaning | Exit Requirement |
|---|---|---|
| `intake` | Capture user goal, constraints, and expected output. | Goal and inputs recorded. |
| `triage` | Assign T0-T3 tier and read policy. | Tier, scope, and risk recorded. |
| `plan` | Select the lowest sufficient plan. | Plan or explicit no-plan reason recorded. |
| `run` | Execute the task. | Outputs or blocker recorded. |
| `digest` | Summarize evidence, files, commands, sources, and remaining uncertainty. | Digest record exists. |
| `claim` | State what was completed and what was not. | Claim is tied to evidence. |
| `review` | Check claim, evidence, risk, and rule compliance. | Pass, conditional pass, or fail decision. |
| `done` | Deliver final result. | Review passed or user accepted residual risk. |

## Branches

`needs_user`: required input or approval is missing.

`blocked`: progress is impossible without external change.

`needs_upgrade`: the current workflow is insufficient.

`memory-propose`: a memory write is proposed after review.

`memory-apply`: a human-approved memory write is applied.

`upgrade-propose`: a framework or skill upgrade is proposed.

`upgrade-apply`: a human-approved upgrade is applied.

`aborted`: user cancels or task becomes obsolete.

Memory and upgrade branches are not part of the default task chain.

