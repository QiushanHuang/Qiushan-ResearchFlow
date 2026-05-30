# Command: Project Connect

Use this to connect another project folder to ResearchFlow.

Project connect has two modes:

- `--mode native` creates a local `.researchflow/` adapter inside the target project. This is also the default when `--mode` is omitted.
- `--mode legacy` creates a ResearchFlow-managed shadow adapter under `project-interfaces/legacy/` and does not change the target project directory.

It does not import project facts, memory, logs, raw data, artifacts, or secrets into global indexes.

## Native Run

```bash
python3 agent-framework/researchflow/scripts/rf_project_connect.py \
  --mode native \
  --framework-root agent-framework/researchflow \
  --project-root /abs/path/to/project \
  --project-id project:<slug> \
  --title "Project Title"
```

## Created In The Project

```text
.researchflow/project.rf.yaml
.researchflow/memory/project.md
.researchflow/local.private.yaml.example
.researchflow/indexes/task.index.jsonl
.researchflow/indexes/knowledge.index.jsonl
.researchflow/indexes/artifact.index.jsonl
.researchflow/indexes/experiment.index.jsonl
.researchflow/indexes/creative-pass.index.jsonl
.researchflow/indexes/golden-run.index.jsonl
.researchflow/indexes/procedure.index.jsonl
.researchflow/indexes/repeat-run.index.jsonl
.researchflow/indexes/exception.index.jsonl
.researchflow/skills/usage.index.jsonl
```

## Legacy Run

Use legacy mode for old projects, mounted drives, external repos, or folders that must not receive new metadata.

```bash
python3 agent-framework/researchflow/scripts/rf_project_connect.py \
  --mode legacy \
  --framework-root agent-framework/researchflow \
  --project-root /abs/path/to/old-project \
  --project-id project:<slug> \
  --title "Project Title"
```

Created in ResearchFlow:

```text
project-interfaces/legacy/project-<slug>/project.rf.yaml
project-interfaces/legacy/project-<slug>/memory/project.md
project-interfaces/legacy/project-<slug>/indexes/task.index.jsonl
project-interfaces/legacy/project-<slug>/indexes/knowledge.index.jsonl
project-interfaces/legacy/project-<slug>/indexes/artifact.index.jsonl
project-interfaces/legacy/project-<slug>/indexes/experiment.index.jsonl
project-interfaces/legacy/project-<slug>/indexes/creative-pass.index.jsonl
project-interfaces/legacy/project-<slug>/indexes/golden-run.index.jsonl
project-interfaces/legacy/project-<slug>/indexes/procedure.index.jsonl
project-interfaces/legacy/project-<slug>/indexes/repeat-run.index.jsonl
project-interfaces/legacy/project-<slug>/indexes/exception.index.jsonl
project-interfaces/legacy/project-<slug>/skills/usage.index.jsonl
```

Legacy mode must not create `/abs/path/to/old-project/.researchflow`.

## Global Update

Only `indexes/project.index.jsonl` receives a pointer to the adapter. The pointer includes `adapter_mode`, `adapter_path`, and `project_root`.

## Verify Native

```bash
python3 agent-framework/researchflow/scripts/rf_project_validate.py \
  --framework-root agent-framework/researchflow \
  --adapter /abs/path/to/project/.researchflow/project.rf.yaml \
  --strict
```

## Verify Legacy

```bash
python3 agent-framework/researchflow/scripts/rf_project_validate.py \
  --framework-root agent-framework/researchflow \
  --adapter agent-framework/researchflow/project-interfaces/legacy/project-<slug>/project.rf.yaml \
  --strict
```
