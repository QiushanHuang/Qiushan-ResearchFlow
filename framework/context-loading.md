# Context Loading

ResearchFlow uses VKF-like context loading: indexes first, evidence on demand.

## Default Rule

Load only:

1. `rf.yaml`
2. relevant command
3. root index entry
4. project memory summary if needed

Do not load source bodies, logs, artifacts, PDFs, notebooks, raw experiment outputs, or RSS source pages unless the task requires evidence.

## Tiered Reads

| Tier | Allowed by Default | Requires Trigger |
|---|---|---|
| T0 | User message only. | Any durable source. |
| T1 | `rf.yaml`, relevant command, one or two indexes. | Source body, file edits, experiments. |
| T2 | Multiple indexes, limited source evidence, project memory. | Raw experiment files, logs, artifacts. |
| T3 | Systematic index and evidence read. | Apply memory or framework changes. |

## Research Library

`library/` is an external background library. It can be indexed but is not project fact. Use it when the task asks for concepts, formulas, papers, parameters, or theory.

## Experiments

Read order:

1. `indexes/experiment.registry.jsonl`
2. `experiments/_catalog/`
3. relevant `ResultDigest`
4. relevant `ExperimentClaim`
5. run metadata only if needed
6. artifact or log only if explicitly needed

## RSS

RSS issues are high-density entries. Treat AI summaries as leads, not truth. Important claims require original source review.

## Project Adapter Rule

If the current working directory, or one of its parents, contains `.researchflow/project.rf.yaml`, load that adapter before global project indexes.

Adapter loading means:

- read the adapter path and local index pointers;
- respect its skip rules;
- treat its project memory as current-project evidence only when the task needs it;
- do not copy adapter content into the global framework;
- do not read `raw/`, `logs/`, `artifacts/`, or linked project memory unless a specific evidence need exists.

Global `project.index.jsonl` entries are pointers to adapters. They are not project fact.
