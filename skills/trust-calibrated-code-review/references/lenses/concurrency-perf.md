# Lens: Concurrency, Async Lifecycles & Performance (`concurrency-perf`)

Stress changed paths under concurrent requests, slow/failing I/O, mid-flight cancellation, and realistic production cardinalities ($10^3$–$10^6$ records rather than 3-item test fixtures). Preserve **blind quarantine**.

## Inspection protocol

1. **Mark interleaving & scaling points**: Locate every `await`/promise/observable/thread hop, shared state access, lock, retry/timeout boundary, and loop/query over variable-sized data.
2. **Interleave two actors**: Walk two concurrent callers executing the same path simultaneously, plus one caller cancelling or timing out halfway through.

## Hunting vectors

- **Check-then-act races (TOCTOU) & lost updates**: Reading state, validating a rule (quota, uniqueness, schedule slot, version), and writing back without optimistic concurrency tokens, atomic conditional updates, row locks, or unique DB constraints; mutating shared singletons, static caches, or request-unsafe fields across concurrent requests.
- **Async, stream & cancellation leaks**: Fire-and-forget tasks/promises dropping exceptions, missing `CancellationToken`/`AbortSignal` forwarding into DB/HTTP calls, sync-over-async blocking (`.Result`/`.Wait()`), deadlocks from lock ordering or async-inside-lock, and unclosed streams, timers, or RxJS/event subscriptions.
- **Unbounded fan-out, retries & failure storms**: `Task.WhenAll`/`Promise.all` without concurrency caps over user/DB-sized lists; outbound I/O without explicit timeouts; retries wrapping non-idempotent writes or lacking backoff/jitter; fallback caches serving stale or cross-principal entries.
- **Algorithmic & I/O amplification**: N+1 queries or RPC calls hidden inside loops/mappers, loading full tables/streams into memory before filtering/paging, quadratic $O(n^2)$ lookups inside loops (repeated `.find`/`.includes` instead of `Map`/`Set`), and cache invalidation misses or stampedes on write paths.

**Done when**: Every async boundary, shared mutable structure, retry/timeout path, and data-proportional loop/query in the matched scope has been evaluated for concurrent interleavings, cancellation safety, and production scale.
