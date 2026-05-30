# Self Upgrade

Self-upgrade changes framework rules, skills, commands, schemas, templates, or read policies.

## Flow

```text
needs_upgrade -> upgrade-propose -> human approval -> upgrade-apply
```

## Proposal Must Include

- trigger event
- rule or workflow that failed
- proposed change
- affected files
- expected benefit
- possible side effects
- rollback or supersession path

## Upgrade Triggers

Repeated high-frequency mechanical work is an upgrade trigger when it has clear inputs, repeatable steps, recoverable failures, and reviewable outputs.

This trigger may create an evolution or upgrade candidate. It does not bypass proposal, review, human approval, or apply records.

## Apply Rules

- No silent upgrade.
- No upgrade from a single low-risk task unless the user explicitly requests it.
- Framework and skill changes require review and user approval.
- Applied upgrades must record source and date.

## Evolution Boundary

`evolution/` may capture a weakness, bug, need, user preference, or proposed improvement. That record is only a signal until it becomes an upgrade proposal, passes review, receives human approval, and is applied with an apply record.

Do not treat an evolution candidate, journal, or self-check as an applied framework upgrade.
