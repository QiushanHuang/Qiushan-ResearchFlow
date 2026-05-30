---
name: rf-project-native-onboarding
description: Use when a project allows a local .researchflow adapter and should join ResearchFlow in native mode.
---

# RF Project Native Onboarding

Native onboarding creates project-owned ResearchFlow metadata inside the project.

## Required Shape

```text
<project-root>/.researchflow/project.rf.yaml
<project-root>/.researchflow/indexes/
<project-root>/.researchflow/memory/project.md
<project-root>/.researchflow/skills/usage.index.jsonl
```

## Steps

1. Fill `prompts/project-interface/native-new-project.md`.
2. Run `scripts/rf_project_connect.py` with `--mode native` or omitted mode.
3. Validate the adapter with `scripts/rf_project_validate.py --strict`.
4. Start work through `rf_intake` and index-first context loading.
5. Mirror meaningful skill usage to the project-local skill usage index.

## Invariant

Native mode may write inside `.researchflow/`; global indexes still remain pointer-only.
