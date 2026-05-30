---
name: rf-project-legacy-onboarding
description: Use when an old or external project must join ResearchFlow without changing its directory.
---

# RF Project Legacy Onboarding

Legacy onboarding creates a ResearchFlow-managed shadow adapter and leaves the target project unchanged.

## Required Shape

```text
agent-framework/researchflow/project-interfaces/legacy/<safe-project-id>/project.rf.yaml
```

## Steps

1. Fill `prompts/project-interface/legacy-shadow-project.md`.
2. Run `scripts/rf_project_connect.py --mode legacy`.
3. Confirm no `.researchflow/` exists inside `project_root` because of this operation.
4. Validate the shadow adapter with `scripts/rf_project_validate.py --strict`.
5. Log skill usage in the global registry.

## Invariant

Legacy mode never writes under `project_root`; all adapter indexes, memory, and skill usage records live under ResearchFlow.
