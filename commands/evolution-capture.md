# Command: Evolution Capture

Use this when the user reports a need, feeling, bug, habit, confusion, repeated preference, or when the agent notices a framework problem during work.

## Do

- Preserve the source wording or a compact faithful summary.
- Add `Normalized Intent`: concise, typo-corrected, deduplicated, and structured.
- Add `Ambiguities` when the user's wording is unclear instead of guessing.
- Record where it came from: user, agent, review, validator, self-check, or subagent.
- Keep it in `evolution/inbox/` until triaged.
- Add or update `indexes/evolution.item.index.jsonl` only after normalization.

## Do Not

- Do not write active memory.
- Do not apply an upgrade.
- Do not mark the issue resolved.
- Do not rewrite the user's intent into something stronger than the evidence supports.

## Normalization Rule

When user input has typos, repeated phrases, mixed clauses, or unclear ordering:

1. preserve enough raw wording to audit the source;
2. rewrite the intent into short, clean bullets;
3. separate requirements from preferences;
4. preserve uncertainty under `Ambiguities`;
5. use the normalized version for future context loading unless the raw wording is needed as evidence.
