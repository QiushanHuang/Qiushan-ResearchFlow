# Command: Project Procedure

Use this after a human-agent task has been run successfully once.

## Flow

```text
creative-pass -> golden-run -> procedure draft -> human approval -> approved procedure -> repeat-run
```

## Rules

- Procedure can only derive from a reviewed golden run or explicit user instruction.
- Repeat-run can only use an approved procedure and exact procedure version.
- Deviation, new judgment, failed validation, or changed scope creates an exception.
- Exception stops execution and routes to `needs_user`, `blocked`, `evolution_capture`, or procedure revision candidate.
- Do not add new state-machine states.

## Adapter Local Only

Creative pass, golden run, procedure, repeat run, and exception records live in the connected adapter:

- native: the project's `.researchflow/` folder;
- legacy: ResearchFlow's `project-interfaces/legacy/<safe-project-id>/` folder.

The global framework keeps only the project adapter pointer.
