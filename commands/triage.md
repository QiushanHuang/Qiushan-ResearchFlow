# Command: Triage

Use triage to assign T0-T3 and choose the read policy.

Read `framework/tiering.md` before assigning the tier.

## Do

- Assign `T0`, `T1`, `T2`, or `T3`.
- State why the tier is sufficient.
- State upgrade and downgrade conditions.
- Choose context read scope.
- Decide whether review, subagents, or user confirmation are required.

## Output

```yaml
state: triage
tier:
reason:
read_scope:
review_required:
subagents_required:
user_confirmation_required:
upgrade_if:
downgrade_if:
```

