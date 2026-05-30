# Indexing Taxonomy

Indexes are loaded before source bodies. An index entry should help an agent decide whether to open a file, not replace the file.

## Source Classes

```text
project -> current project evidence and local adapter
project-link -> pointer to another project
experiment -> registry, digest, claim, artifact
library -> external knowledge source
rss -> high-density external feed entry
evolution -> feedback, issue, habit, bug, candidate, self-check
resource -> compute resource, storage location, task-route suggestion
skill -> available Codex skill, selection note, project usage history
memory -> durable project, bridge, or universal memory after approval
```

## Boundary Fields

Use these fields on entries that are not current-project facts:

```yaml
fact_status: pointer | candidate | observed | verified | stale | conflict
truth_boundary:
not_project_fact: true
```

`pointer` means "this may be relevant, open the source if needed." It does not make a claim true.

## Multi-Level Lookup

Use this order for dense projects and simulation folders:

1. Framework entrypoint: `rf.yaml`.
2. Global index: `indexes/*.jsonl`.
3. Project adapter: `.researchflow/project.rf.yaml`, if present.
4. Local project indexes: task, artifact, experiment, knowledge.
5. Manifests and digests.
6. Source bodies, logs, raw data, or artifacts only when evidence is required.

Do not recursively scan large experiment folders when a registry or manifest exists.
