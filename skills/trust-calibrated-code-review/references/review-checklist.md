# Review coverage checklist

Mark every category `checked`, `not verified`, or `not applicable`. Report only evidence-backed findings.

1. **Intent & scope**: Acceptance criteria met, unrequested behavior, partial implementation, feature flags, user-visible regressions.
2. **Correctness**: Boolean/branch logic, null/empty handling, bounds/off-by-one, numeric/timezone/locale handling, idempotency, state transitions, invariants, cleanup, regressions from deleted/moved code.
3. **Architecture & contracts**: Caller/callee contracts, layer/domain boundaries, shared state, config coupling, public surface, migration/deployment/rollback compatibility.
4. **Security**: AuthN/AuthZ boundaries, IDOR, tainted input/injection (SQL, command, template, XSS), SSRF, path traversal, deserialization, secrets/logging, crypto, CORS/CSRF, supply-chain/script actions. Require a concrete attack path and prerequisite.
5. **Privacy, safety & compliance**: Data minimization, retention/deletion, consent, auditability, regulated/safety-critical controls. State what remains unverified outside code.
6. **Data integrity**: Transactions, atomicity, schema/migration compatibility, concurrent updates, duplicate/out-of-order events, partial writes, precision/type loss, rollback safety.
7. **Concurrency & distributed systems**: Deadlocks, races, async error propagation, cancellation, timeouts, bounded retries/backoff, stale reads, resource contention, pagination/cursors.
8. **Performance & scalability**: Algorithmic complexity, N+1 queries, unbounded memory/work/payloads, hot-path blocking, cache invalidation, I/O amplification.
9. **Reliability & operations**: Failure modes, graceful degradation, health/readiness, structured observability (logs/metrics/traces), actionable errors, rate limits/quotas, safe config defaults.
10. **Dependencies & APIs**: Lockfile/version alignment, exact API signatures against local types/docs, breaking changes, runtime/toolchain compatibility.
11. **Tests & verification**: Behavioral assertions over snapshot mirrors, negative/boundary/adversarial cases, preserved existing protections, flake risk.
12. **Maintainability**: Accidental complexity, broken abstractions, hidden coupling, dead code, inconsistent error handling. Skip subjective style nitpicks.
13. **UI & accessibility** *(when applicable)*: Loading/error/empty states, keyboard navigation, focus management, ARIA/labels, contrast, i18n, responsive layout.
14. **CI & infrastructure** *(when applicable)*: Workflow permissions, secret exposure, pinned actions, artifact provenance, environment drift, reproducible builds.
15. **LLM-specific failure modes**: Persuasive rationale masking wrong code, hallucinated/deprecated APIs, placeholder/stubbed logic, swallowed errors, tautological tests that test the mock or mirror the bug, cross-file drift.
