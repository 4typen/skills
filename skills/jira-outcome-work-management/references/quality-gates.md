# Issue quality review

## Mandatory checks by type

Epic: bounded outcome, purpose, in/out scope, observable delivery completion, coherent child work, independent impact measurement if relevant.

Story: one clear change in behavior, observable acceptance checks, relevant errors/permissions, no needless technology prescription, independent vertical slice where practical.

Task: necessity, intended work product, verifiable completion, no duplicate implementation tracking.

Bug: actual vs expected, evidence/repro, environment/scope, impact/severity, verification and regression prevention where appropriate.

Spike: clear question, bounded investigation, written decision/evidence as completion.

## Review rubric: 0/1/2 per dimension

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Purpose | Unclear | Partial | Explicit and relevant |
| Correct type | Misclassified | Ambiguous | Fits intended artifact |
| Boundaries | Catch-all | Some limits | Coherent finite scope |
| Testability | Vague | Partly verifiable | Observable completion |
| Traceability | No source/relations | Partial | Enough relevant links/source |
| Essential risks | Key risks ignored | Mentioned | Relevant constraints addressed or open questions explicit |

12 maximum. Score is **diagnostic guidance**, not a mandated Jira field or universal gate. If key facts are missing, do not hallucinate them to increase the score. Prefer 1-3 highest-value changes. Ask a follow-up question only when the answer materially affects scope, expected behavior, or safety; otherwise state assumptions and provide a draft.

## Security and operations relevance checklist

Consider selectively for SaaS: authentication, authorization, multi-tenant boundaries, data privacy/retention, data migrations, audit trails, backwards-compatible APIs, feature flags, retry/idempotency, rate limiting, failure modes, observability, performance/capacity, accessibility, rollback and incidents. Do not add every item to every issue.

## Readiness

Ready means: understandable intent, relevant acceptance/completion criteria, no unresolved decision that makes start unsafe, important dependencies visible, scope reasonably bounded. This is a lightweight quality standard, **not a pseudo-Sprint or mandatory checklist of 25 fields**.

## Definition of done reminder

Completion means acceptance met; suitable tests and code review performed; relevant security/privacy standards met; implementation integrated and verified in agreed environment; necessary monitoring/docs updated. Whether production deployment or user activation is required depends on team policy and feature flags. Do not infer release from Jira status.
