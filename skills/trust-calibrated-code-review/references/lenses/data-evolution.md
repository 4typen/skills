# Lens: Data Integrity, Persistence & Evolution (`data-evolution`)

Inspect state persistence assuming production stores already hold historical records, concurrent writers, and rolling deployments. Preserve **blind quarantine** (code, schemas, events, and Repo Invariants Brief only).

## Inspection protocol

1. **Inventory persisted contracts**: Identify every touched entity, table/migration, SQL/ORM query, domain event, aggregate `Apply`/projection, cache entry, or serialized payload.
2. **Replay historical & mixed-version state**: Trace how data written **before** this change is read, replayed, migrated, or deserialized **after** this change — and vice versa during a rolling deploy or rollback.

## Hunting vectors

- **Event-sourcing & wire evolution**: Changed or newly required fields on persisted domain events, snapshots, or queue payloads read without an upcaster, version handler, or safe default when replaying historical streams; projections assuming event fields or ordering guarantees that older streams lack.
- **Destructive or locking schema migrations**: Dropping, renaming, or tightening nullability/types on columns still read or written by live old application nodes; unindexed foreign keys or full-table rewrites/locks on large tables; missing backfill or broken down/rollback behavior.
- **Transaction & atomicity splits**: Multi-aggregate or multi-table writes lacking a single transaction boundary; database state committed before/after an external publish or HTTP call without an outbox or idempotent recovery path, leaving split-brain state on partial failure.
- **Idempotency, duplicates & ordering**: Message consumers, background jobs, retries, or API endpoints that double-apply mutations, insert duplicates, or regress newer state when at-least-once or out-of-order events arrive.
- **Query & mapping fidelity**: Missing soft-delete or tenant predicates on new queries, timezone/date-truncation mismatches between app and DB, cascade deletes or orphaned rows, silent string truncation, or decimal/enum precision loss in persistence mappers.

**Done when**: Every touched schema, query, transaction boundary, cache key, and persisted/event contract has been traced against historical data compatibility, partial-failure atomicity, and replay/retry idempotency.
