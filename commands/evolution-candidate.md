# Command: Evolution Candidate

Create a candidate when an evolution item may need follow-up.

## Candidate Types

- `todo`
- `memory`
- `upgrade`
- `reusable_action`
- `library`
- `project_task`
- `resource_route`

## Rules

- `requires_human_confirmation: true`
- `apply_allowed: false`
- `status: candidate`
- Cite the source item.
- Route durable changes to `memory-propose` or `upgrade-propose`.

Candidates do not change active memory or framework behavior by themselves.
