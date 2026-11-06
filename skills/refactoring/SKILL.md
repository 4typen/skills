---
name: refactoring
description: Plan and execute a structural change that preserves observable behavior, either as a standalone refactoring or as a preparatory step inside a larger task. Use when the user asks to refactor, restructure, extract, centralize, or migrate internal structure; when `/refactoring` is invoked or this skill text is pasted into the prompt; or when a task changes a shared contract, call routing, or module boundary.
argument-hint: "Describe the target structure and why it is needed."
author: André Schubert
date: 2026-11-05
---

Change structure, keep behavior.

> Make the change easy, then make the easy change.

## Modes

State the active mode in the first line of your response: `MODE: STANDALONE` or `MODE: EMBEDDED`.

- **STANDALONE**: a pure refactoring request, or an explicit `/refactoring` or this skill text pasted into the prompt (even during an active task or when mixed with new behavior: defer the new behavior, run the full `## Plan`, and stop at `PLAN_READY`).
- **EMBEDDED**: a structural step inside an active feature or bug task when `/refactoring` or the skill text was not explicitly provided. Separate the structural change from the behavior change. Run the full `## Plan` and stop at `PLAN_READY` only when at least one threshold applies:
  - a shared contract changes (public API, event, schema, cross-module signature);
  - 3 or more consumers are affected (1 or 2 consumers stay below this threshold);
  - 4 or more production files change (1 to 3 files stay below this threshold).
  Below all three thresholds, do not stop at `PLAN_READY`: state the invariant and the affected consumers, confirm the tests are green before and after the structural step, then implement the behavior step.

If a request mixes structural change with new behavior (for example retries, circuit breaker, new exceptions) without explicit `/refactoring` or pasted skill text and the mode is unclear, stop with `CLARIFY_MODE` and ask one direct question.

## What Counts as Structural

A change is structural if at least one applies:
- call paths are rerouted through a new central method, wrapper, or dispatcher;
- responsibilities move across classes, modules, or layers;
- a shared contract changes;
- 3 or more consumers or 4 or more production files change shape without changing observable behavior.

If none apply (for example renaming a private helper inside one file), the change is not structural: this skill does not apply and no plan gate or light check is required.

## Precedence

- `AGENTS.md` rules always apply. For shared contracts, run the blast-radius analysis (CBM `trace_path` where available) before editing.
- The `PLAN_READY` gate, safety-net check, and step separation from this skill override `ponytail` (smallest single diff). Apply `ponytail` only inside each individual step.

## Plan

Planning is read-only: change no code. Run only tests that use disposable resources and leave shared state unchanged.

1. State the mode, the target structure, the reason, and the **invariant**: the public contracts, data, and outputs that stay unchanged.
2. Find every consumer. Record the list and the search scope, including repositories you cannot access. Do not remove a contract until all its consumers are known.
3. Run the **safety net** against the unchanged code: tests that pin observable behavior on every affected path. Tests that only check mocks do not count. The baseline must be green. Fill gaps with characterization tests as the first steps.
4. Choose one mechanism:
   - **Parallel change** (expand → migrate → contract): a contract with many consumers changes.
   - **Strangler**: a component is replaced behind a stable entry point.
   - **Mikado**: dependencies are tangled. The plan names the goal and the first probe. During execution, try the change, revert on failure, record the prerequisite, and start at the leaf.
   - **Small direct steps**: the change is local.
5. Cut steps. Each step is one mechanical change, keeps all tests green, and is mergeable alone. Keep structural steps separate from steps that add new behavior. With more than one consumer, one step first migrates one real consumer end to end.

Stop with `PLAN_READY` and wait for the user to confirm.

## Execute

Run the steps in order. After each step, run the tests and check the invariant. To revert, undo only the edits of the current step.

If a step needs extra work and the invariant, the consumer list, and the mechanism stay the same, record the deviation and continue. If one of them changes, return to planning and wait for a new `PLAN_READY` confirmation.

Report `DONE` only when the target structure is reached, every consumer is migrated or kept with a reason, all steps are complete, and the final tests and invariant checks pass.

## Stop Conditions

- `CLARIFY_MODE`: the mode is unclear, or a request without explicit `/refactoring` or pasted skill text mixes structural change with new behavior. Ask one question and wait.
- `BLOCKED`: the baseline is red, cannot run, or would change shared state; or a precondition outside the team is missing. Show the evidence.
- `NO_SAFETY_NET`: an affected path cannot be pinned, not even by characterization tests.
- `BEHAVIOR_CHANGED`: a step changes observable behavior, and the fix would change the plan. Revert the step and stop.
- `TOO_BROAD`: a step cannot be cut so that it is green and mergeable alone.

## Output

Start with mode and status: `MODE: <STANDALONE|EMBEDDED> | <PLAN_READY|DONE|STOP_STATUS>`. Then summarize:

After the plan:
- Invariant
- Consumers, blast radius, and search scope
- Safety net, baseline, and gaps
- Mechanism and reason
- Steps: change · consumers touched · verification
- Deferred behavior changes, if any

After execution:
- Steps with verification results
- Deviations from the plan
- Consumers migrated or kept, with reason
- Final checks and results
