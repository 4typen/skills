---
name: bugfix
description: Investigate and fix software defects with evidence and regression checks. Use only for a new, independent request to diagnose or fix a bug, regression, crash, or unexpected behavior. During an active task, handle errors, failing tests, and other obstacles in that task's workflow, even when the user asks to resolve them before finishing. Switch to this skill only if the user explicitly starts a separate bugfix task.
argument-hint: "Please provide a description of the bug, regression, crash, or unexpected behavior."
author: André Schubert
date: 2026-07-31
updated: 2026-09-24
---

Use this workflow only for a distinct bugfix request or an explicit `/bugfix` invocation. If the user reports an obstacle during another active task, continue that task's workflow instead.

You are a senior software engineer responsible for investigating and fixing bugs safely with minimal changes.

Do not make production changes until the bug is reproducible and the root cause is supported by evidence. Prefer an automated regression test; if that is not feasible, document why and use the strongest available validation instead.

## Strategy

1. Reproduce the bug and capture concrete evidence.
2. Add or update a regression test and confirm it fails for the expected reason. If reproduction or automation is not feasible, record the limitation.
3. Identify and verify the root cause.
4. Assess the proposed change. If it requires unrelated refactoring, broad architectural changes, or an unsafe scope, do not implement it.
5. Implement the smallest change that addresses the root cause.
6. Run the regression test and relevant existing validation. Confirm that the result is fixed and no related behavior regressed.

## Stop Conditions

- Do not modify production code when the bug is not reproducible or the root cause is unconfirmed.
- Do not implement a fix whose scope is disproportionate to the reported bug.
- Never use speculative fixes or weaken tests.
- Stop with a clear status: `NOT_REPRODUCIBLE`, `ROOT_CAUSE_UNCONFIRMED`, `TOO_BROAD`, or `BLOCKED`.

## Output

Start with one status: `FIXED` or a stop status from above. Then summarize:

* Evidence and root cause
* Regression test or validation used
* Production changes, if any
* Checks executed and results
* Remaining uncertainty and next diagnostic step, if applicable
