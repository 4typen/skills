# Findings-first report, severity, and verdict specification

## Severity rubric

Grade surviving findings by verified impact, and merge shared root causes into one finding listing all affected `file:line` sites:

- **`P0` Critical**: Exploitable security/tenant compromise, irreversible data corruption or loss, broken event/migration replay blocking recovery, or safety-critical failure.
- **`P1` High**: Demonstrable or strongly supported functional breakage, auth/trust bypass, race/state corruption, breaking API/schema/codegen drift, or serious regression on a realistic path.
- **`P2` Medium**: Edge-case or operational defect (boundary, timezone, partial failure, retry, accessibility, N+1/resource hazard), architecture-boundary violation, or missing test protection on a `HIGH`-risk branch.
- **`P3` Low**: Localized defect, misleading contract/error handling, or concrete maintainability hazard with clear blast radius.

## Grading tokens

- **Confidence**: `confirmed` (reproduced by test/tool or unambiguous single-path trace) · `strongly supported` (concrete multi-hop trace without compensating guard) · `plausible` (realistic failure mode depending on an unverified runtime input or deployment state).
- **Evidence grade**: `observed` (direct code trace or executed command output) · `inferred` (reasoned interaction across callers/states) · `unverified` (requires runtime/external proof; keep only under Residual Risks unless paired with a concrete code trace).

## Merge verdict gates

- **`BLOCK`**: Any `confirmed` or `strongly supported` `P0` or `P1` finding.
- **`CHANGES REQUESTED`**: Material `P2` findings, or a `plausible` `P0`/`P1` hazard awaiting verification.
- **`CONDITIONAL`**: Zero `P0`–`P2` findings in static inspection, while required build/test checks could not run locally.
- **`READY TO MERGE (within reviewed scope)`**: Zero `P0`–`P2` findings and relevant verification checks ran and passed.
- **`INCONCLUSIVE`**: Missing diff base, unreadable target, or insufficient repository context prevents reliable inspection.

---

## Findings-first report template

Render section headings in the user's conversation language; keep verdict tokens, `P0`–`P3`, confidence/evidence tokens, code identifiers, and `file:line` paths verbatim.

### 1. Verdict & scope
- **Verdict**: `BLOCK` | `CHANGES REQUESTED` | `CONDITIONAL` | `READY TO MERGE (within reviewed scope)` | `INCONCLUSIVE` — one-sentence justification.
- **Scope**: `<target / base...head>` · `<N> files (<H> HIGH, <M> MEDIUM, <L> LOW)` · `<tests executed | static-only>`
- **Findings**: `P0: <n> · P1: <n> · P2: <n> · P3: <n>` *(raw candidates: `<total>` -> rejected by counterevidence: `<rejected>`, merged: `<merged>`)*
- **Intent vs. diff**: 1–3 sentences contrasting requested behavior with actual code changes (explicitly mark inferred intent or unrequested scope).

### 2. Verified findings (ordered `P0 -> P3`)

**[F-01] P1 · `<lens or domain>` · `confirmed` | `strongly supported` | `plausible`** — `path/to/file.ext:lineStart-lineEnd` *(+ related `file:line` sites)*
- **Trigger**: Concrete input, call sequence, state transition, concurrency interleaving, or deployment/replay condition.
- **Impact**: Expected invariant vs. actual failure, data/security exposure, or regression.
- **Evidence (`observed` | `inferred`)**: Exact code path and caller trace, plus why nearby guards or tests do not prevent it.
- **Fix**: Minimal code change and regression test to close the root cause.

*(When zero diff findings survive triage, state: `No substantiated defects found in the changed paths.` If triage uncovered material pre-existing bugs outside the diff's causal path, list them briefly under a separate **Pre-existing issues (outside diff)** note without blocking the verdict unless the diff amplifies them.)*

### 3. Lens coverage, verification & residual risks

| Lens | Trigger / scope | Raw -> Kept | Key area verified |
| --- | --- | --- | --- |
| `blind-correctness` | core (blind diff) | `2 -> 1` | Domain state transitions & boundary guards |

| Check command | Exit | Result |
| --- | --- | --- |
| `<exact command or static-only>` | `0` / `not run` | `<concise outcome or sandbox limitation>` |

- **Residual risks**: 1–3 concrete bullets naming paths, external contracts, or runtime behaviors that static inspection and local checks could not verify.
