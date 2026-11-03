# Heuristic risk model

Score each changed file on six axes (`0–3`, or `?` when evidence is unavailable) to order review attention:

| Axis | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Impact / blast radius | isolated display/docs | local behavior | shared workflow/data | critical or systemwide behavior |
| Security / privacy / safety | none | low exposure | privileged or sensitive path | auth/trust boundary, sensitive data, safety-critical path |
| Logic / behavior complexity | trivial | simple branch | multiple states/edge cases | concurrency, distributed coordination, subtle algorithm |
| Compatibility / coupling | internal only | narrow caller | shared interface/schema | public API/protocol/migration/backward compatibility |
| Evidence gap | thorough relevant tests | partial tests | weak/unclear tests | no checks / unknown behavior |
| History / volatility | well understood | routine area | churn or fragile ownership | rarely changed critical code, prior incidents, or regression-prone churn |

## File risk label

- **`HIGH`**: Security/safety = `3`, demonstrable systemwide blast radius, any single axis = `3` with weak tests, or multiple `2+` axes.
- **`MEDIUM`**: Moderate exposure, shared workflow impact, or unresolved `?` axes.
- **`LOW`**: Low scores across all axes backed by direct test evidence.
- **`UNKNOWN`**: Insufficient context to score; treat with `HIGH`-risk caution until inspected.

Cite paths, callers, tests, or git history for each score; mark `?` when history is unavailable. Treat scores as attention heuristics (high change frequency is context, not low risk).

## Line-level priority (Risk-per-line)

Within each file, inspect first: auth/permission guards, input parsing, queries/SQL, serialization, state/cache transitions, concurrency/locks, network/IO boundaries, retries/fallbacks, arithmetic/bounds, feature flags, and error/cleanup paths.
