---
name: rf-review-gate
description: Use when reviewing ResearchFlow claims, T2/T3 outputs, memory proposals, upgrade proposals, or any durable state change.
---

# RF Review Gate

Review checks whether the claim is true, scoped, verified, and compliant with ResearchFlow rules.

## Workflow

1. Read `commands/review.md`.
2. Check original goal.
3. Check claim against evidence.
4. Check tier, context loading, and forbidden reads.
5. Check that memory or upgrade was not applied silently.
6. Return `pass`, `conditional-pass`, or `fail`.

## Invalid Review

Reviews are invalid when they only restate the answer, say "LGTM", or skip evidence.

