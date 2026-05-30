# Command: Evolution Triage

Turn an inbox signal into a normalized evolution item.

## Classify

- issue
- bug
- user_preference
- agent_habit
- framework_gap
- validation_gap
- cross_project_risk
- resource_routing_need

## Required Output

```yaml
status:
severity:
summary:
evidence:
authority_scope:
entered_where:
requires_human_confirmation:
apply_allowed: false
not_done:
```

If the item might become memory or an upgrade, create a candidate. Do not apply it.
