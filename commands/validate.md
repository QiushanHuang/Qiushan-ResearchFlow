# Command: Validate

Use `rf_validate` before claiming that ResearchFlow indexes, claims, digests, or memory proposals are structurally clean.

## Run

```bash
python3 agent-framework/researchflow/scripts/rf_validate.py agent-framework/researchflow
python3 agent-framework/researchflow/scripts/rf_validate.py agent-framework/researchflow --strict
```

## Scope

The validator checks:

- JSONL parseability;
- required index fields;
- duplicate IDs within an index;
- date and read-policy shapes;
- unsafe boundary fields;
- claim, digest, and memory proposal skeletons;
- candidate records that try to apply themselves;
- resource records that allow auto execution.

It does not verify factual truth, evidence strength, RSS accuracy, cross-project fact transfer, or whether a recommendation is scientifically good.

## Output

```text
PASS path rule message
WARN path rule message
FAIL path rule message
```

`--strict` treats warnings as failures.
