# Risk tagging, repo invariants, and specialist routing

Use this guide in Phase 0 to order files **risk-first**, extract repository rules, and activate specialist lenses deterministically without building a narrative walkthrough.

## 1. Fast file risk tagging (`HIGH` / `MEDIUM` / `LOW`)

Assign each changed or untracked file the highest tier its diff hunks warrant:

- **`HIGH`**:
  - AuthN/AuthZ, permissions, tenant isolation, crypto, secrets, or untrusted input parsing.
  - Domain aggregates/invariants, state machines, financial/time/scheduling calculations, persistence writes, migrations, event contracts/projections, or caches.
  - Public/cross-service APIs, shared schemas, concurrency/async coordination, retries, or destructive infrastructure/CI workflow changes.
  - Any non-trivial production logic change lacking direct test updates or touching unfamiliar/critical core paths.
- **`MEDIUM`**:
  - Internal application handlers, UI components/state/forms, client integrations, non-destructive build/config updates, or behavioral refactors backed by tests.
- **`LOW`**:
  - Pure documentation, comments, static assets, formatting-only diffs, mechanical renames verified across compilation/tests, or auto-generated/vendored artifacts (such as OpenAPI/Orval client outputs or snapshot dumps — tag `[generated]` so `blast-radius` checks regeneration parity and consumers while code lenses focus on hand-written sources).

Treat uncertain files (`UNKNOWN` context or deleted/moved guards) as **`HIGH`** until a lens inspects them. Within every file, inspect high-consequence lines first: guards, queries, state mutations, serialization, error/cleanup paths, bounds/time math, and async boundaries.

## 2. Repo Invariants Brief extraction

Check for repository guidance in this order (read only files that exist and bear on touched areas):

1. `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`
2. `.github/instructions/*.md` matching changed file globs, and any repo-local review skill (such as `.github/skills/code-review/SKILL.md`)
3. Architecture test projects, linter/OpenAPI/codegen scripts in manifests (`package.json`, `*.sln`, `Makefile`, `pyproject.toml`)

Distill at most **10 concrete, checkable invariants** relevant to the diff (for example: layer dependency direction, event-sourcing replay/upcaster rules, required API client codegen after backend contract edits, i18n key completeness, or required review language). Omit generic style prose.

## 3. Specialist lens trigger table

Activate **every** specialist lens that matches at least one path or diff construct signal. Record the matched file/signal for Phase 1 scoping and Phase 3 reporting; leave unmatched specialist lenses off.

| Specialist lens | Activate when changed paths or diff hunks touch any of: |
| --- | --- |
| `security-trust` | Auth/session/JWT/RBAC/tenant checks; HTTP/GraphQL/RPC/webhook/CLI entry points; raw SQL/command/path/URL/HTML/template/regex/deserialization sinks; secrets, PII/PHI, logging/error payloads, CORS/CSRF, crypto. |
| `data-evolution` | Database schemas, migrations, repositories, ORM/SQL queries; domain events, event sourcing, projections, snapshots, upcasters; message queues/outbox; cache keys/TTLs; persisted or wire DTO serialization; multi-step transactions or seeders. |
| `concurrency-perf` | `async`/await/promises/streams/RxJS/channels/locks/threads/workers; background jobs, schedulers, retries, timeouts, cancellation tokens; shared/singleton/static state; loops over queries/IO (N+1), pagination/batching, large payload/memory paths, hot-path caches. |
| `ui-state-a11y` | Frontend components, templates, JSX/HTML/CSS; client stores, reducers, effects, signals, reactive forms, routers/guards; ARIA/focus/keyboard interactions; user-facing copy, i18n/translation files, loading/empty/error states. |
| `infra-ci-deps` | `.github/workflows/**`, CI pipelines, GitHub Actions/scripts; package manifests or lockfiles (`package.json`, `pnpm-lock.yaml`, `*.csproj`, `Directory.Packages.props`, `pyproject.toml`, `go.mod`, `Cargo.toml`); Dockerfiles, Compose, Helm, Terraform/IaC, cloud/provisioning or runtime env config. |
