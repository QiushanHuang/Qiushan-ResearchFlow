# Stage Gates

## Intake Gate

Pass when:

- user goal is recorded
- expected output is known
- obvious constraints are recorded
- missing critical context is either resolved or marked unknown

## Triage Gate

Pass when:

- tier is assigned
- scope and non-goals are stated
- read policy is chosen
- subagent and review needs are identified

## Plan Gate

Pass when:

- plan matches tier
- dependencies and user-confirmation points are known
- verification method is stated

T0 can skip a written plan if the answer is direct and no durable state changes occur.

## Run Gate

Pass when:

- commands or edits are recorded
- no forbidden paths were read by default
- no memory or upgrade apply occurred silently

## Digest Gate

Pass when:

- opened indexes and sources are listed
- outputs are summarized
- assumptions and unknowns are listed
- evidence links are preserved

## Claim Gate

Pass when:

- completed and incomplete items are separated
- claim is tied to evidence
- residual risk is stated

## Review Gate

Reviewer must not just approve. Review is valid only when it:

- checks the original goal
- checks claim against evidence
- identifies at least one residual risk or explains why risk is low
- checks for over-reading, silent upgrade, and memory bypass
- checks for identity impersonation or unauthorized external commitment
- checks for unsupported habit learning or missing evidence chain
- checks whether repeated mechanical work should be captured as a candidate
- gives `pass`, `conditional-pass`, or `fail`
