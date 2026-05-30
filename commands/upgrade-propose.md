# Command: Upgrade Propose

Use upgrade-propose when current workflow, schema, skill, command, or read policy is insufficient.

## Do

- Describe the failure or repeated friction.
- Identify affected files.
- Propose minimal change.
- State side effects and rollback path.
- Ask for human approval.

## Output

```yaml
upgrade_proposal_id:
trigger:
current_rule:
problem:
proposed_change:
affected_files:
expected_benefit:
side_effects:
rollback:
requires_human_confirmation: true
status: proposed
```

