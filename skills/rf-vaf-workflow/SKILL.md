---
name: rf-vaf-workflow
description: Use when executing a ResearchFlow task after triage, especially T1-T3 tasks that need planning, execution, digest, claim, and review.
---

# RF VAF Workflow

VAF means Validate, Act, Feedback.

## Validate

Use:

- `commands/plan.md`
- `commands/context-load.md` when context is needed

## Act

Use:

- `commands/run.md`

## Feedback

Use:

- `commands/digest.md`
- `commands/claim.md`
- `commands/review.md` for T2/T3

## Rule Source

Use `framework/state-machine.md` and `framework/stage-gates.md` as the source of truth.

## Hard Limits

- Memory is not part of the default chain.
- Upgrade is not part of the default chain.
- Claim without evidence cannot pass review.

