# Lens: Blast Radius, Contracts & Untouched Siblings (`blast-radius`)

Hunt defects that live **outside** the diff because a contract shifted or a parallel code path was left behind. Preserve **blind quarantine**: derive behavior strictly from the before/after code and the **Repo Invariants Brief**, leaving commit logs and PR prose unread.

## Inspection protocol

1. **Extract shifted surfaces**: List every changed function signature, return value/nullability, thrown error/result type, event/DTO shape, route, configuration key, or behavioral invariant in `HIGH`- and `MEDIUM`-risk files.
2. **Trace outward**: Use code-intelligence and call-graph tools first (LSP references, `trace_path`, `search_graph`), falling back to `grep`/`glob`, to inspect **real callers, consumers, and sibling implementations** outside the diff.
3. **Audit repository invariants**: Check each rule in the **Repo Invariants Brief** against actual imports, module boundaries, and generated artifacts.

## Hunting vectors

- **Caller & consumer breakage**: Unchanged callers passing arguments under old semantics, ignoring newly possible `null`/empty/error results, assuming prior sort order or mutability, or catching the wrong exception type.
- **Untouched siblings (omission bugs)**: Parallel handlers, command/query twins, enum/union `switch` sites, mappers, serializers, validators, projections, CLI/seeders, or platform adapters that implement the same pattern as the changed file and still carry the unpatched bug or stale contract.
- **Cross-boundary & codegen drift**: Backend endpoint/DTO edits missing OpenAPI or generated frontend client/mock regeneration; producer event/message changes out of sync with consumers; config writers out of sync with readers; new UI translation keys missing from locale bundles.
- **Architecture & layer violations**: Dependency-direction breaches (domain importing infrastructure/UI, cross-module internal leaks), bypassed domain entry points, or hidden coupling via shared mutable globals/config.
- **Rolling deploy & rollback skew**: Wire formats, routes, feature flags, or persisted contracts that break when old and new instances run side-by-side or after a rollback.

**Done when**: Every changed public/shared contract has been traced to its external callers and consumers, **untouched siblings** have been searched across the codebase, and every applicable rule in the Repo Invariants Brief has been checked against real files.
