---
name: refactoring
description: Plan and execute a structural change that preserves observable behavior. Use only for a new, independent request to refactor, restructure, or migrate internal structure. During an active task, handle structural changes in that task's workflow. Switch to this skill only if the user explicitly starts a separate refactoring task.
argument-hint: "Describe the target structure and why it is needed."
author: André Schubert
date: 2026-11-05
---

Use this workflow only for a distinct refactoring request or an explicit `/refactoring` invocation. If a structural change comes up during another active task, continue that task's workflow instead.

Change structure, keep behavior. If the request or a step needs new behavior, defer that behavior to a separate task.

> Make the change easy, then make the easy change.

## Plan

Planning is read-only: change no code. Run only tests that use disposable resources and leave shared state unchanged.

1. State the target structure, the reason, and the **invariant**: the public contracts, data, and outputs that stay unchanged.
2. Find every consumer. Record the list and the search scope, including repositories you cannot access. Do not remove a contract until all its consumers are known.
3. Run the **safety net** against the unchanged code: tests that pin observable behavior on every affected path. Tests that only check mocks do not count. The baseline must be green. Fill gaps with characterization tests as the first steps.
4. Choose one mechanism:
   - **Parallel change** (expand → migrate → contract): a contract with many consumers changes.
   - **Strangler**: a component is replaced behind a stable entry point.
   - **Mikado**: dependencies are tangled. The plan names the goal and the first probe. During execution, try the change, revert on failure, record the prerequisite, and start at the leaf.
   - **Small direct steps**: the change is local.
5. Cut steps. Each step is one mechanical change, keeps all tests green, and is mergeable alone. With more than one consumer, one step first migrates one real consumer end to end.

Stop with `PLAN_READY` and wait for the user to confirm.

## Execute

Run the steps in order. After each step, run the tests and check the invariant. To revert, undo only the edits of the current step.

If a step needs extra work and the invariant, the consumer list, and the mechanism stay the same, record the deviation and continue. If one of them changes, return to planning and wait for a new `PLAN_READY` confirmation.

Report `DONE` only when the target structure is reached, every consumer is migrated or kept with a reason, all steps are complete, and the final tests and invariant checks pass.

## Stop Conditions

- `BLOCKED`: the baseline is red, cannot run, or would change shared state; or a precondition outside the team is missing. Show the evidence.
- `NO_SAFETY_NET`: an affected path cannot be pinned, not even by characterization tests.
- `BEHAVIOR_CHANGED`: a step changes observable behavior, and the fix would change the plan. Revert the step and stop.
- `TOO_BROAD`: a step cannot be cut so that it is green and mergeable alone.

## Output

Start with one status: `PLAN_READY`, `DONE`, or a stop status. Then summarize:

After the plan:
- Invariant
- Consumers and search scope
- Safety net, baseline, and gaps
- Mechanism and reason
- Steps: change · consumers touched · verification
- Deferred behavior changes, if any

After execution:
- Steps with verification results
- Deviations from the plan
- Consumers migrated or kept, with reason
- Final checks and results
