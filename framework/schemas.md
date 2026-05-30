# Schemas

First-version schemas are documented as required fields. Future versions can add machine-readable JSON Schema.

## Common Index Entry

Required:

```yaml
schema_version:
id:
kind:
title:
status:
path:
created_at:
updated_at:
checksum:
read_policy:
```

Recommended boundary fields for external, cross-project, resource, and evolution entries:

```yaml
fact_status: pointer | candidate | observed | verified | stale | conflict
truth_boundary:
```

## Task Record

Required:

```yaml
task_id:
tier:
state:
goal:
scope:
inputs:
outputs:
opened_context:
review_gate:
memory_updates:
```

Valid states:

```text
NEW TRIAGED PLANNED EXECUTING DIGESTING CLAIMING REVIEWING DONE WAITING_USER BLOCKED ABORTED
```

## Experiment Claim

Required:

```yaml
claim_id:
claim:
claim_status:
claim_strength:
evidence_level:
scope:
valid_only_when:
invalid_when:
result_digest_id:
not_domain_law: true
generalization_allowed: false
```

## Memory Proposal

Required:

```yaml
proposal_id:
target_layer:
content:
source:
scope:
confidence:
invalidates_on:
requires_human_confirmation: true
```

## Evolution Item

Required:

```yaml
id:
kind:
status:
source:
summary:
evidence:
linked_task:
authority_scope:
entered_where:
requires_human_confirmation: true
apply_allowed: false
```

Valid `entered_where` values:

```text
none todo project_memory_candidate bridge_candidate universal_memory_candidate upgrade_candidate reusable_action_candidate library rss archived
```

## Project Adapter

The project-local adapter lives at `<project-root>/.researchflow/project.rf.yaml`.

Required:

```yaml
schema_version: 1
kind: project-adapter
project_id:
title:
status:
framework.root:
paths.project_root:
paths.project_memory:
paths.local_indexes:
sync.authority: local_project
privacy.export_allowed:
```

## Skill Inventory Entry

Required for `kind: codex-skill`:

```yaml
skill_name:
trigger_summary:
source_root:
skill_path:
recommended_for:
```

## Skill Usage Entry

Required for `kind: skill-usage`:

```yaml
skill_ids:
project_id:
project_path:
researchflow_project_entry:
usage_scope:
task_type:
used_at:
outcome:
```

Project-local usage can be mirrored at `<project-root>/.researchflow/skills/usage.index.jsonl`. The framework-level index remains `indexes/skill-usage.index.jsonl`.
