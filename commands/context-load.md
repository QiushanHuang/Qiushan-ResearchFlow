# Command: Context Load

Use context-load whenever a task needs project, research, experiment, RSS, or memory context.

Read `framework/context-loading.md` first.

## Do

- Load indexes before source bodies.
- Record every opened file or source.
- Record why each source was opened.
- Stop before reading skipped paths unless a specific evidence need exists.

## Default Skip

Follow `rf.yaml` `skip_by_default`.

## Output

```yaml
opened:
  - path:
    reason:
    tier:
excluded:
  - path_or_pattern:
    reason:
remaining_unknowns:
```

