# Memory Chain

The memory chain prevents project facts and experiment observations from becoming universal rules too early.

```text
ResearchKnowledge / Run / Artifact
-> ResultDigest / ExperimentClaim
-> ProjectMemory
-> MemoryBridge
-> UniversalMemory
```

## Layers

`ResearchKnowledge`: background concepts, papers, formulas, theories, and learning notes. Not project fact.

`EvolutionSignal`: feedback, bug, issue, habit, or self-check record. It can propose a memory candidate but is not memory itself.

`HabitObservation`: observed user method or preference. It is not active memory.

`HabitCandidate`: scoped habit proposal candidate. It still requires memory proposal, review, human approval, and apply.

`Run`: a single execution with config, inputs, command, outputs, and metrics.

`Artifact`: output file, plot, table, log, model, report, or dataset.

`ResultDigest`: batch/run summary. It says what was observed under scoped conditions.

`ExperimentClaim`: atomic, reviewable claim derived from digest evidence. Default is not a domain law.

`ProjectMemory`: concrete project fact, decision, problem, parameter, command, result, or constraint.

`MemoryBridge`: evidence relation between project memory and universal memory.

`UniversalMemory`: transferable method, failure pattern, heuristic, checklist, or preference.

## Hard Rules

- Universal memory may not directly cite logs, artifacts, raw runs, or RSS summaries.
- Experiment claims are evidence nodes, not domain laws.
- Single runs stay observations.
- Project memory may cite digest, claim, batch index, and run metadata.
- Universal memory requires bridge, scope, exceptions, and review.
- Controller may propose memory but may not apply memory.
- Evolution records may not become project, bridge, or universal memory without the memory proposal flow.
- Habit learning follows `HabitObservation -> HabitCandidate -> MemoryProposal -> ApprovedMemory`.
- A single observation, typo, tone, temporary constraint, or one-project preference cannot become universal memory directly.
