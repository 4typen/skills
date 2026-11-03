# Review report, severity, and verdict specification

## Severity rubric

Grade by evidence-backed impact:

- **P0 Critical**: Exploitable security compromise, irreversible data corruption/loss, or immediate safety/integrity failure.
- **P1 High**: Demonstrable or strongly supported major functional failure, security vulnerability, data loss path, serious regression, or breaking contract change.
- **P2 Medium**: Realistic defect under edge/operational conditions, material reliability/maintainability hazard, or missing test on a high-risk path.
- **P3 Low**: Localized defect or maintainability issue with concrete impact.

Deduplicate root causes into a single finding covering all affected locations.

## Merge verdict gates

- **`BLOCK`**: Any unresolved `confirmed` or `strongly supported` P0/P1 finding.
- **`CHANGES REQUESTED`**: Material P2 findings or unresolved high-risk uncertainty.
- **`CONDITIONAL`**: Code inspection is clean, but required test/build verification could not be executed locally.
- **`READY TO MERGE (within reviewed scope)`**: No blocking findings and required checks were executed and observed passing.
- **`INCONCLUSIVE`**: Missing diff, base, or context prevents reliable review.

---

## Report template

### 1. Executive summary
- **Scope**: repo/PR/commit, `base -> head`, file count, review mode (`tests executed` / `static-only`).
- **Intent vs. actual diff**: 2–5 sentences contrasting requested behavior with observed changes (flag inferred intent).
- **Verdict**: `BLOCK` | `CHANGES REQUESTED` | `CONDITIONAL` | `READY TO MERGE (within reviewed scope)` | `INCONCLUSIVE`
- **Finding counts**: P0 / P1 / P2 / P3.

### 2. Level 1 — Architectural walkthrough
- Changed modules, control/data flow, affected external callers/contracts, and key invariants.
- Requirement -> semantic chunk -> test/evidence mapping (and any gaps).

### 3. Level 2 — File risk map & checklist coverage
| File | Risk (`HIGH`/`MEDIUM`/`LOW`/`UNKNOWN`) | Rationale (axes) | Depth | Test evidence |
| --- | --- | --- | --- | --- |
| `path/to/file` | `HIGH` | Security=3, Evidence=2 | deep | unit test passed / not run |

- **Checklist summary**: list checked categories and any category marked `not verified` with reason.

### 4. Level 3 — Semantic chunks
| Chunk | Files & lines | Invariant / requirement | Failure modes checked | Status |
| --- | --- | --- | --- | --- |

### 5. Findings (ordered P0 -> P3)
**[F-01] P1 · Category · `confirmed` | `strongly supported` | `plausible`** — `path/to/file.ext:lineStart-lineEnd`
- **Trigger**: Concrete input, state, or call sequence.
- **Expected vs. actual**: Expected invariant vs. actual behavior and blast radius.
- **Evidence**: Code trace, caller, or test result (`observed` / `inferred` / `unverified`).
- **Fix & regression test**: Minimal code change and test to lock it in.

*(If none: `No actionable findings in inspected scope; residual risk remains in unverified areas below.`)*

### 6. Verification & coverage ledger
| Command / check | Executed? | Exit code & result | Limitations |
| --- | --- | --- | --- |

| Changed path | Change type | Final ledger status | Notes |
| --- | --- | --- | --- |

### 7. Remaining risks & merge recommendation
- Unverified paths, missing requirements, operational/rollback risks, and why the verdict matches the evidence.
