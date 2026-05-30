# Command: Memory Propose

Use memory-propose after claim/review when durable memory may be useful.

Memory proposal is not memory application.

## Do

- Choose target layer: project, bridge, or universal.
- Provide source evidence.
- State scope, confidence, and invalidation condition.
- Explain why this is reusable.
- Ask for human approval before apply.

## Output

```yaml
proposal_id:
target_layer: project | bridge | universal
content:
source:
scope:
confidence:
invalidates_on:
requires_human_confirmation: true
status: proposed
```

