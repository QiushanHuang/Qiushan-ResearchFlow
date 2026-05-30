# Command: Subagent Five-Pass Review

Use `rf_subagent_five_pass_review` when the user asks for multiple high-reasoning subagents to analyze the same problem before implementation, decision, or framework update.

## Trigger

Equivalent user wording includes:

```text
使用多个 5.5 xhigh subagent
对同一问题拆解和互相讨论
审核后 5 次完整迭代
最后再整体重复一次全流程并整体审核
```

## Preconditions

- The user explicitly asked for subagents, delegation, or this named action.
- The objective, scope, and output expectations have been normalized.
- The next local step does not depend on an unbounded open-ended subagent task.

## Five-Pass Flow

1. **Pass 1: Independent decomposition**  
   Spawn multiple subagents with distinct angles. Ask each to produce a bounded memo: assumptions, decomposition, risks, proposed files or actions, and non-goals.

2. **Pass 2: Cross-review**  
   Give each subagent the other memos. Ask for conflicts, missing constraints, naming problems, and overreach risks.

3. **Pass 3: Synthesis audit**  
   Ask each subagent to converge on a minimal executable specification and identify what should be postponed.

4. **Pass 4: Implementation readiness**  
   Ask for must-fix, can-defer, cannot-do, and minimum verification.

5. **Pass 5: Go/No-Go**  
   Ask for a final `GO` or `NO-GO`, with any required corrections.

## Next Phase

Only move to the next phase after:

- `NO-GO` blockers are resolved; or
- `GO` is received and the local controller has checked scope and safety.

## Whole-Flow Repeat

After the next phase is completed, run one additional overall pass of the same pattern on the whole result:

- independent overall audit;
- cross-review of audit findings;
- synthesis of residual risks;
- verification readiness check;
- final go/no-go.

This repeat checks integration, not just individual pieces.

## Output Contract

Record:

- subagent names or IDs;
- pass count;
- major disagreements;
- adopted decisions;
- rejected suggestions;
- verification run;
- remaining risks.

For framework work, save the summary in `framework/subagent-iteration-log.md` or an `evolution/journals/` record.

## Boundaries

- Do not spawn subagents unless explicitly requested.
- Do not let subagent memos apply memory or upgrades.
- Do not run the same work redundantly in the main agent and subagents.
- Close subagents after their final result.
