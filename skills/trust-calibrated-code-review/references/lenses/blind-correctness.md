# Lens: Blind Correctness & Invariants (`blind-correctness`)

Inspect what the changed code **actually executes** under adversarial inputs and edge states. Preserve **blind quarantine**: inspect diffs, full source files, and type definitions directly while leaving commit logs, PR descriptions, and ticket prose unread so author rationale cannot mask logic defects.

## Inspection protocol

1. **Risk-first entry**: Start at the `HIGH`-risk files in your packet, then `MEDIUM`, then `LOW`. For every changed hunk, read the complete enclosing function, class, or state machine rather than relying on 3-line diff context.
2. **Adversarial input walk**: Trace concrete boundary inputs through each changed branch before moving to the next file.
3. **Self-check before reporting**: Verify inside the enclosing file and its direct types that no immediate guard already blocks your trigger.

## Hunting vectors

- **Branch & boolean logic**: Inverted conditions, De Morgan errors in negated compound expressions, early returns skipping state updates or cleanup, missing `else`/default branches, `<` vs `<=` off-by-one bounds, and empty vs single-element vs duplicate-element collections.
- **Nullability, optionality & sentinel conflation**: Valid zero/empty values (`0`, `""`, `false`, `0.0`) treated as missing by truthy checks or fallback operators (`||` instead of `??`), unchecked nullable dereferences, or silent key-lookup misses.
- **Units, numeric math & time**: Integer division truncation, overflow, floating-point money/quantity rounding, unit mismatches (ms vs s, bytes vs KiB), UTC vs local date boundaries, DST transitions, and inclusive vs exclusive interval ends.
- **State invariants & partial mutation**: Mutating object, aggregate, or collection state before a validation or fallible call throws; broken idempotency when called twice; asymmetric resource acquisition and disposal (`Dispose`/`close`/listener teardown) on exception paths.
- **Refactor, move & deletion regressions**: Preconditions, null checks, sorting, filters, or side effects dropped when code was simplified, extracted, or deleted.
- **LLM generation hazards**: Stubbed/placeholder branches, swallowed errors (`catch` returning a default or logging without failing when state is corrupt), or comments asserting checks the code omits.

**Done when**: Every `HIGH`- and `MEDIUM`-risk changed function has been traced with boundary inputs in **risk-first** order, every deleted/moved guard has been accounted for, and every returned candidate cites an exact `file:line` execution path.
