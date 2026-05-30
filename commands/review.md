# Command: Review

Use review for T2/T3 tasks and whenever durable state changes are proposed.

Read `framework/stage-gates.md` first.

## Reviewer Must

- Check the original goal.
- Check claim against evidence.
- Check whether the task used the right tier.
- Check whether source bodies, logs, artifacts, or experiments were over-read.
- Check whether memory or upgrade was applied without approval.
- Identify a residual risk or explain why risk is low.

## Invalid Review

The review is invalid if it only restates the solution or says "looks good" without evidence.

## Output

```yaml
state: review
decision: pass | conditional-pass | fail
evidence_checked:
issues:
residual_risk:
required_changes:
memory_apply_allowed: false
upgrade_apply_allowed: false
```

