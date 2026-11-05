---
name: refactoring
description: Plan and execute a structural change that preserves observable behavior. Use only for a new, independent request to refactor, restructure, or migrate internal structure. During an active task, handle structural changes in that task's workflow. Switch to this skill only if the user explicitly starts a separate refactoring task.
argument-hint: "Describe the target structure and why it is needed."
author: André Schubert
date: 2026-11-05
---

Use this workflow only for a distinct refactoring request or an explicit `/refactoring` invocation. If a structural change comes up during another active task, continue that task's workflow instead.

Change structure, keep behavior. Every step leaves the main branch green and mergeable on its own.

> Make the change easy, then make the easy change.

When a request mixes a refactoring with new behavior, this skill covers only the first half: make the change easy. The feature follows afterwards as a separate task.

## Plan

Planning is read-only: run tests, change no code. Run only tests that use disposable resources and leave shared state unchanged; otherwise stop with `BLOCKED`.

1. State the target structure, the reason, and the **invariant**: the public contracts, data, and outputs that stay unchanged.
2. Find every consumer of the code that changes. Record the list and the search scope, including repositories you cannot access. A contract with unverified consumers stays compatible; remove it only after all consumers are known.
3. Check the **safety net**: tests that pin the observable behavior on every affected path. Tests that only check mocks of internal calls do not count. Run them against the unchanged code and record the result as the baseline. The baseline must be green; if it is red or cannot run, stop with `BLOCKED` and show the evidence. Where the safety net has gaps, the first steps add characterization tests. If a path cannot be pinned, stop with `NO_SAFETY_NET`.
4. Choose one mechanism:
   - **Parallel change** (expand → migrate → contract): a contract changes and has many consumers.
   - **Strangler**: a component is replaced behind a stable entry point.
   - **Mikado**: dependencies are tangled. The plan names the goal and the first probe. During execution, try the change, revert on failure, record the prerequisite, and start at the leaf.
   - **Small direct steps**: the change is local.
5. Cut steps. Each step is one mechanical change, keeps all tests green, and is mergeable alone. If more than one consumer changes, one separate step migrates one real consumer end to end before the others follow.

Stop after the plan with status `PLAN_READY` and wait for the user to confirm it.

## Execute

Run the steps in order. After each step, run the tests and check the invariant. Each step carries structure only; a behavior change becomes its own task.

To revert, undo only the edits of the current step. Keep all work that existed before it.

A deviation from the plan that keeps the invariant and the consumer list is recorded, and execution continues. A deviation that changes the invariant, the consumer list, or the mechanism returns to planning and needs a new `PLAN_READY` confirmation.

Report `DONE` only when the target structure is reached, every recorded consumer is migrated or kept with a stated reason, all steps are complete, and the final tests and invariant checks pass.

## Stop Conditions

- `NO_SAFETY_NET`: an affected path has no pinning tests, and characterization tests are not feasible.
- `BEHAVIOR_CHANGED`: a step changes observable behavior, and the fix would change the approved plan. Revert the step and stop.
- `TOO_BROAD`: a step cannot be cut so that it is green and mergeable alone.
- `BLOCKED`: a precondition outside the team is missing.

## Output

Start with one status: `PLAN_READY`, `DONE`, or a stop status.

After the plan:
- Invariant
- Consumers found
- Safety net, baseline result, and gaps
- Mechanism and reason
- Steps: change · consumers touched · verification
- Deferred behavior changes, if the request mixed refactoring with new behavior

After execution:
- Steps completed, with the verification result for each
- Deviations from the plan
- Consumers migrated or kept, with reason
- Final checks executed and results
