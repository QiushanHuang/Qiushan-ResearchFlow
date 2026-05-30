# Sync Conflicts

ResearchFlow avoids automatic two-way sync in the first version.

## Staleness

Suggested stale windows:

- project adapter: 7 days without sync;
- compute resource dynamic status: 24 hours;
- storage free space: 6 hours;
- task route: 30 days without review;
- cross-project link: 90 days without confirmation.

## Conflict Rules

- Same `project_id`, `resource_id`, or `storage_id` with conflicting checksum: mark conflict and stop automatic merge.
- Local adapter beats stale global index data for current project structure.
- Latest `last_seen_at` can inform dynamic resource status, but stale status is advisory only.
- Other-project conclusions that conflict with current project evidence remain separate and should be linked with `conflicts_with`.
- Secret or private machine details belong in local private files, not global indexes.
