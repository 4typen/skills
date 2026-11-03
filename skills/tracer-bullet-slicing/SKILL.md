---
name: tracer-bullet-slicing
description: Break down a requirement of any format - PRD, epic, spec, RFC, ticket, feature request - into vertical Tracer Bullets, Enablers, and thin deliverable slices with clear preconditions, zero external blockades, and agent-executable execution capsules. Use when users want to slice a requirement or PRD, break down a large feature, define a Tracer Bullet, cut vertical user stories from a spec or ticket, or prepare work packages for coding agents.
disable-model-invocation: true
author: André Schubert
date: 2026-09-24
updated: 2026-09-24
---

# Tracer Bullet Slicing

Slice a requirement into deliverable vertical slices anchored by a **Tracer Bullet** (a production-grade, minimal end-to-end traversal of the whole system).

The requirement may arrive in any format: PRD, epic, technical spec, RFC, ticket, feature request, bug cluster, or a verbal description. Format does not change the method; only how much normalization is needed up front.

A core principle of this slicing approach is: **Developers and coding agents must never be blocked during implementation by missing upstream data, unclarified third-party APIs, or unaligned downstream contracts.**

Do not confuse a Tracer Bullet with a disposable prototype or an MVP:
- A **prototype / spike** is throwaway code or research answering an isolated question.
- An **MVP** is the smallest product cut that tests a business learning loop with users.
- A **Tracer Bullet** is production code: it establishes the enduring architectural skeleton, from the entry point through real durable state to the real delivery pipeline, on the simplest happy path. It stays in the codebase and grows.

---

## Normalize the Requirement First

Before slicing, restate the source in these terms:
- **Actor:** who or what initiates the behavior.
- **Trigger:** the concrete event that starts it.
- **Observable outcome:** what is visibly true afterwards, and for whom.
- **Rules & constraints:** invariants, validations, permissions, compliance limits.
- **Boundaries touched:** external systems, other teams' services, upstream data, downstream consumers.

Thin sources (tickets, chat messages, one-line feature requests) usually answer two of these. Ask for the missing ones instead of inventing them. Slice only what can be stated.

**Stop gate.** A question is blocking if a different answer would change the Tracer Bullet, a boundary, or a phase order. With one or more blocking questions, **no proposal is produced.** Emit only the normalized requirement and the questions, then stop. Never fill a blocking gap with an assumption, and never ship a proposal with a caveat list attached.

---

## The Readiness Imperative: Clear Preconditions Ahead of Time

The biggest trap in agile projects is dragging unfulfilled preconditions and external dependencies into individual user stories. When a story says *"Requires upstream data X"* or *"Pending API contract with Team Y"*, the developer or coding agent will hit a wall mid-sprint.

### The Phased Resolution Rule:
1. **Preconditions belong in Phase 0 (Prerequisites & Enablers):**
   - All external blockers, missing upstream data sources, and unready integrations are addressed **before** the Tracer Bullet or functional stories begin.
   - If an external system or upstream data source is not yet available, Phase 0 creates a clean internal **Port / Interface** and a **Test Fake / Fixture**.
2. **User Stories (Phase 2+) are Zero-Blocker by definition:**
   - Once Phase 0 and the Tracer Bullet (Phase 1) are complete, subsequent user stories carry **no external blockade** - nothing pending from another team, a third party, or an unfinished upstream feature.
   - **Internal build order is legitimate and must be stated, not hidden.** A slice that consumes another slice's domain ground records it as `Builds on: [slice]`. This is an ordering fact the team resolves itself - it is never a precondition in the Phase 0 sense.
   - Litmus test: could the team finish this story today if it chose to? Yes -> internal order. No -> external blockade -> belongs in Phase 0.

---

## Agentic Coding Slicing: Working with Coding Agents in the Loop

In an agentic workflow, a developer operates and steers coding agents (e.g. Pi, Claude Code, Copilot) to implement slices. Stories should be formatted for this developer-agent collaboration:

1. **Goal-Oriented over Step-by-Step (Goal over Method):**
   - Define the **declarative goal (Objective)**: what is the desired observable state of the system?
   - Do **not** pre-chew the implementation steps, class designs, or file edits. The developer and agent discover existing patterns dynamically (e.g. via code search and MCP tools).
2. **No Volatile Code Details in Stories:**
   - Avoid hardcoding specific file paths, line numbers, or internal class names in stories. Codebases evolve, causing static references to become stale immediately.
3. **Guardrails & Invariants (MUST / MUST NOT):**
   - Provide the guardrails the agent must strictly respect (e.g. *an append-only log stays append-only*, *the project's architecture and dependency rules stay green*, *published schemas stay backward compatible*).
4. **Observable Acceptance Criteria:**
   - Focus on clear, testable behavior (Given/When/Then, expected state transitions) that the developer and agent can verify together.

---

## Process

### 1. Perform Feasibility & Readiness Audit (Requirement vs. Codebase)
Probe the normalized requirement against the actual repository and surrounding systems. The probe list is closed: **every category produces at least one audit row, or the explicit entry "none — [one-line reason]".** A silently skipped category is a defect, not a shortcut.

1. **Upstream data & events** - entities, IDs, calculations, and events the feature reads.
2. **Downstream consumers & contracts** - receivers, topics, schemas, owning teams.
3. **External systems & third parties** - partner APIs, vendors, licenses, sandboxes.
4. **Persistence & data lifecycle** - storage structures, migrations, existing data, backfill.
5. **Identity, permissions & compliance** - authn/authz, roles, tenancy, PII and legal gates.
6. **Runtime & infrastructure** - environments, queues, secrets, configuration, feature flags.
7. **Delivery & verification** - pipeline, test infrastructure, test data, the environment to verify in.

Each row carries exactly one of three verdicts:
- **ready** - verified to exist today. Requires code or external evidence (see the evidence rule below).
- **blocked** - verified to be missing or unready -> Phase 0 item (enabler, or port + fake).
- **unknown** - status not established. `unknown` is a legitimate result and must never be resolved by guessing. Route it:
  - a different answer would change the Tracer Bullet, a boundary, or phase order -> **blocking question, stop gate applies**;
  - otherwise -> **Phase 0 clarification enabler** with a timebox and the single decision that ends it.

**Evidence rule.** Every row states how its status was established: code finding, external confirmation, or assumption. An `assumption` may never yield the verdict `ready`; it yields `unknown`. Ground every row in the repository or in a named external confirmation before assigning a status.

Categorize every `blocked` row by origin:
- **Blocker (External):** missing upstream data or external partner dependency -> Phase 0 enabler, or port + fake.
- **Enabler (Internal):** first-party foundational plumbing (e.g. a new core entity, base route, auth policy, storage structure).

### 2. Extract Foundational Enablers (Phase 0: Story 0s & Boundary Fakes)
Identify all technical and data prerequisites missing from the architecture.

**Admission test - all three must hold:**
1. The Tracer Bullet or at least two later slices cannot be built without it.
2. The blockade originates outside the slice and cannot be created inside it.
3. It has a measurable completion criterion.

If a single slice could carry it, it is absorbed into that slice. An enabler is never a layer ("create the schema", "build the endpoints", "design the screens") - it is a port, a fake, a migration, or a provisioning step.

- **Boundary Isolation:** If an external system (e.g. a partner API, another team's service, an unfinished upstream feature) is not ready, define an internal **Port / Interface** and a **Test Fake / Stub**. The feature slices must be 100% buildable and testable against this port.
- Every fake created here creates a matching **boundary realization** item in the cross-cutting track (step 7).
- *Sizing bound:* Phase 0 stays below the Tracer Bullet's own size. If it grows larger, the boundary was drawn too wide - redraw it.
- When Phase 0 is complete, all preconditions for the feature are permanently resolved.

### 3. Isolate the Happy Path Core Loop
Find the single narrowest actor action that completes an end-to-end cycle. Strip 80% of the requirement's complexity (variants, batching, multi-field validations, complex error recovery, presentation polish).
*Completion criterion:* The action can be described in one simple sentence:
*Actor triggers X -> System processes X -> State persists X -> Actor observes X.*
*Single-trigger test:* the sentence names exactly one trigger. Two triggers are two loops - pick the one that carries more architectural risk and defer the other to a slice.

### 4. Define the Tracer Bullet (Phase 1: The Architectural Skeleton)
Specify the minimal end-to-end slice that traverses **every station** of the system. Stations are functional roles, not architecture layers - name them with the project's own vocabulary:

| Station | Web application | CLI / library | Data pipeline / async |
|---|---|---|---|
| **Trigger / entry point** | Minimal control in the UI | Command invocation | Schedule or incoming message |
| **Boundary contract** | Endpoint with typed payload | Argument or function signature | Input schema of the record/event |
| **Core decision / logic** | Single handler, one state transition | Core function | Single transform step |
| **Durable state** | Real write in the real datastore | File or committed artifact | Real write to the sink |
| **Observable result** | Rendered confirmation | Exit code / stdout output | Record readable downstream, run status |
| **Delivery** | Real build, tests green, deployable | Packaged release, tests green | Orchestrated run, tests green |

Rules for the traversal:
- **Every station is real.** Nothing is mocked or simulated, except a boundary explicitly declared as a Phase 0 port.
- **A station the project genuinely does not have is marked N/A** with a one-line reason (e.g. a stateless service has no durable state), never silently skipped.
- **One of everything:** one input, one rule, one path, no variants, no polish.
- *Sizing bound:* one pullable unit, 3-5 dev days max.
- *If it does not fit:* the core loop in step 3 was not narrow enough - return to step 3 and strip further. Mocking a station is never the answer.

### 5. Slice Remaining Scope along 5 Vertical Dimensions
Decompose all deferred requirements into independent, vertically testable stories with **Zero Blockade** guarantees:
1. **Data variance & complexity:** Hardcoded / default values -> dynamic ranges -> multiple entities -> batching.
2. **Business rules & guardrails:** Unconditional acceptance (Tracer) -> structural validation -> hard blocking invariants -> soft warnings.
3. **Interaction depth:** Primitive control -> state feedback (loading, error, empty) -> rich interaction (inline editing, drag & drop, shortcuts, streaming output).
4. **Edge cases & resilience:** Concurrency and locking, retry and recovery, conflict resolution, undo.
5. **Reach & integration:** Additional actors, permissions, real external adapters, bulk paths, export and reporting.

**Sizing rule for slices.** A slice whose goal cannot be stated as one observable end state in one sentence must be split. A slice that moves two of the five dimensions at once must be split along the dominant one. If the requirement yields more slices than a team can order meaningfully, the requirement itself is too large - split the requirement first, not the slices.

### 6. Organize into Deliverable Milestones
Only the first three phases are fixed, because they are structurally motivated:
- **Phase 0:** Prerequisites & Enablers (ports, fakes, migrations, infrastructure, data stubs).
- **Phase 1:** Tracer Bullet (architectural proof, verified pipeline).
- **Phase 2:** Functional Core - the first genuinely usable capability (core rules, essential validation, baseline interaction). A rule the source states as a prohibition ("must not") belongs here together with the behavior it constrains - never in a later phase, and never split from the feedback that makes the refusal comprehensible.

**Phase 3 and beyond carry no fixed labels.** They are further vertical slices, named after the dimension from step 5 that dominates them (e.g. *"Data variance: multi-entity input"*, *"Resilience: concurrent edits"*), and ordered by risk and value - highest uncertainty and highest value first. Numbers beyond Phase 2 express ordering, not categories. Produce only the phases the requirement actually needs.

### 7. Schedule Cross-Cutting Work as a Separate Track
Some work is genuinely horizontal. It belongs in its own track, not at the end of the phase ladder.

**Admission test - all three must hold:**
1. It cannot be assigned to a single slice without duplicating it arbitrarily across slices.
2. It only becomes decidable once several slices exist, or once an external precondition changes.
3. It has a measurable completion criterion.

If one slice could carry it, it belongs inside that slice.

**Class catalog.** Each class fixes four things that the item template does not: when it fires, which guardrail is characteristic for it, which proof it owes beyond regression, and what done looks like.

- **Boundary realization** - replaces a Phase 0 port or fake with the real adapter, including contract tests against the real system.
  - *Trigger:* the external system becomes available. Every Phase 0 fake produces exactly one of these.
  - *Characteristic guardrail:* the port contract must not widen while the implementation is swapped; no permanent dual path.
  - *Class-specific proof:* real failures and timeouts surface as the port's declared errors, with no transport exception leaking.
  - *Done looks like:* contract suite green against the real system; the fake referenced from test code only.
- **Consistency sweep** - unifies error, empty and loading behavior, terminology, permission model, i18n or accessibility across slices that each solved it on their own.
  - *Trigger:* the same concern is handled differently in two or more shipped slices.
  - *Characteristic guardrail:* no new functional behavior; the convention lives in exactly one place.
  - *Class-specific proof:* a newly built surface inherits the convention without extra work.
  - *Done looks like:* every surface in scope routes through the shared mechanism; no local variant remains.
- **Operability** - observability, metrics, alerting, runbooks, and migration or backfill of existing data.
  - *Trigger:* the first slice reaches a real environment with real users or real data.
  - *Characteristic guardrail:* no sensitive data in signals; every alert has a named owner and a defined action; migrations are repeatable.
  - *Class-specific proof:* someone who did not build the feature reaches a diagnosis by following the runbook.
  - *Done looks like:* the alert verified by an intentionally triggered failure; the runbook walked end to end once.
- **Load, scale & performance** - indexing, bulk paths, caching, streaming throughput.
  - *Trigger:* a measured value crosses a stated threshold - record the number, the date and the environment. Never a guess.
  - *Characteristic guardrail:* no correctness traded for speed; no optimization without a baseline; every cache states its invalidation rule.
  - *Class-specific proof:* identical results before and after the change at the stated volume.
  - *Done looks like:* a reproducible load test committed; baseline and post-change numbers recorded side by side.

Every item - whatever its class - is written out with the same rigor as a slice story (goal, scope, guardrails, acceptance criteria) and additionally names its **class**, its **trigger** and its **admission rationale**. One template covers all classes; see the output template and the worked example. An item is scheduled as soon as its trigger fires, interleaved with vertical slices rather than queued behind all of them.

---

## Strict Slicing Rules

- **Zero External Blockades in Stories:** Never write a user story that cannot be finished because an external API, third-party contract, or upstream feature is pending. Isolate all dependencies in Phase 0.
- **No Precondition Drift:** *External* preconditions belong in Phase 0. Stories in Phase 2+ must be pullable without waiting on anything outside the team; internal build order is stated via `Builds on`, never as a precondition.
- **Vertical over horizontal:** Never produce stories such as "create the storage schema", "build the backend endpoints", or "design the screens". Every user-facing story must deliver observable behavior across the required stations.
- **Goal over Implementation:** Describe what observable state must be achieved, not which lines or files to edit.
- **Production standards from day one:** A Tracer Bullet carries automated tests, linter compliance, and type safety. It is not throwaway code.
- **Cross-cutting work never defers slice quality:** Every slice ships production-grade for the scope it claims. A cross-cutting item may only lift a property across slices; it must never supply quality a slice owed for its own scope.
- **Derive Acceptance Criteria directly from the source:** Map the requirement's sections, bullets, or ticket acceptance notes (validation, error states, permission checks) 1:1 to story acceptance criteria.

---

## Before You Emit

Every line must be true. A false line is a defect, not a nuance.

- [ ] No blocking open question remains (otherwise the stop gate applies).
- [ ] Every Tracer Bullet station is either real or marked N/A with a one-line reason.
- [ ] No slice in Phase 2+ names an external blockade; internal order is stated via `Builds on`.
- [ ] All seven probe categories appear in the audit - each with rows or an explicit "none — reason".
- [ ] Every boundary named in the normalized requirement has at least one audit row.
- [ ] Every `blocked` or `unknown` row resolves into exactly one Phase 0 item or one blocking question - count them.
- [ ] Every Phase 0 item traces back to at least one audit row; an item without a row is unmotivated.
- [ ] No row holds verdict `ready` on evidence `assumption`.
- [ ] The audit has at least as many rows as boundaries plus Tracer Bullet stations; fewer is incomplete by construction.
- [ ] Every Phase 0 fake has exactly one boundary-realization item in the cross-cutting track - count them.
- [ ] All four cross-cutting classes were considered; for each, either an item exists or its trigger is recorded as not yet fired.
- [ ] Every cross-cutting item passes all three admission criteria.
- [ ] Every acceptance criterion names an observable subject and a decidable outcome. Every number carries unit, threshold, and measurement point.
- [ ] No slice title or goal names a file, a class, or a line.
- [ ] No slice is a layer ("schema", "endpoints", "screens").
- [ ] Each phase beyond 2 is named after its dominant dimension and states its risk/value rationale.
- [ ] Every phase, the cross-cutting track, and the deferred section is visibly separated; each phase starts with a one-sentence exit condition.
- [ ] Every pullable item has a stable identifier and its one-sentence objective, core loop, or goal directly below its title; its prescribed labelled details follow in the template's order.
- [ ] The initial response contains the full audit and complete detail for every pullable item; a summary never substitutes for a phase or item specification.

---

## Human-Readable Phase Layout

A complete proposal is a hand-off document, not a narrative. Keep its full audit and every pullable item in the first answer—do not replace detail with an executive overview or defer it to a later turn. Make each phase the reading unit, so a human can locate a phase, understand its exit condition, and then drill into a single item without searching through one continuous block.

- Separate Phase 0, Phase 1, every Phase 2+, the cross-cutting track, and deferred work with `---`.
- Give only phase and track headings one semantic icon. Do not decorate prose, bullets, or every acceptance criterion; labels must carry the meaning without the icon.
- Start every phase with a one-sentence **Exit condition**: the observable state that lets the reader move on. Later phases also state **Why now**.
- Give every pullable item a stable identifier: `0.1`, `1.1`, `2.1`, `3.2`, or `CC-1`. Put its one-sentence objective, core loop, or goal in a blockquote directly below its title.
- Keep each card's prescribed labelled fields in the template's visual order. For slice and cross-cutting cards, that is context, scope, guardrails, then proof. Use short labelled blocks; render acceptance criteria as checkboxes so they are easy to scan and verify.
- Give phase and track headings one semantic icon; the audit verdict is the only other emoji use. Do not decorate prose, bullets, or every acceptance criterion; labels must carry meaning without an icon.

## Output Template

> Use this as the proposal structure. Keep Phase 0, Phase 1, and Phase 2; add later phases only when needed. Emit every section below in the first complete proposal. All Phase 2+ slices are ready to implement without pending prerequisites.

```markdown
# Slicing Proposal: [Feature or Requirement Name]

## Normalized Requirement
- **Source:** [reference]
- **Actor / trigger / observable outcome:** [...]
- **Rules & constraints:** [...]
- **Boundaries touched:** [...]
- **Open questions (non-blocking only):** [..., or "none"]
  *Blocking questions stop the process - see the stop gate.*

## Readiness & Dependency Audit
| Probe | Dependency | Status | Evidence | Verdict | Mitigation / enabler |
|---|---|---|---|---|---|
| [1–7] | [...] | [missing / partial / exists / none] | [code finding / external confirmation / assumption] | [🟢 ready / 🔴 blocked / 🟡 unknown / ⚪ n/a] | [port + fake / enabler / blocking question / none] |

*Use one full row for every audit finding. A probe category with no finding gets its own row: Dependency `none — [reason]`, Status `none`, Verdict `⚪ n/a`. Never encode an absence as `🟢 ready`. An `assumption` never yields `🟢 ready` either.*

---
## 🧱 Phase 0 — Prerequisites & Enablers
> **Exit condition:** Every external precondition is resolved or isolated behind its declared port and test fake.

### 0.1 — [Enabler title]
> **Objective:** [capability, port, fake, migration, or infrastructure]
- **Audit rows:** [probe category and dependency this item resolves]
- **Blockade resolved:** [...]
- **Boundary-realization follow-up:** [cross-cutting item, or "none"]
**Done when**
- [ ] [completion criterion]

---
## 🎯 Phase 1 — Tracer Bullet
> **Exit condition:** One production-grade, minimal happy path crosses every real station and is verified end to end.

### 1.1 — [short tracer-bullet title]
> **Core loop:** [Actor triggers X → system processes X → state persists X → actor observes X]
- **Boundary strategy:** [real boundary or Phase 0 port/fake]
**Real traversal**
1. **Trigger / entry point:** [...]
2. **Boundary contract:** [...]
3. **Core decision / logic:** [...]
4. **Durable state:** [real write, or N/A + reason]
5. **Observable result:** [...]
6. **Delivery:** [build, automated test, deployable artifact]
**Sizing:** one pullable unit, 3–5 dev days maximum

*Phase 2 is the Functional Core. Add a later phase only when the requirement needs it; name it after the dominant vertical dimension.*

---
## 🚀 Phase [number] — [Functional Core | dominant dimension]
> **Why now:** [required for Phase 2; otherwise risk/value rationale]
> **Exit condition:** [observable capability established when this phase is complete]

### [phase].[item] — [Slice title]
> **Goal:** [one declarative, observable end state]
**Builds on:** [earlier slice, or "nothing"]
**Scope**
- **In:** [...]
- **Deferred:** [...]
**Guardrails**
- **MUST:** [...]
- **MUST NOT:** [...]
**Acceptance criteria**
- [ ] [Given / When / Then happy path]
- [ ] [Given / When / Then validation, error, or boundary behavior]

---
## 🧭 Cross-Cutting Track — scheduled by trigger
> Include only work that passes the admission test. Every Phase 0 fake has one boundary-realization item.

### CC-1 — [title]
> **Goal:** [declarative, observable shared end state]
- **Class:** [Boundary realization | Consistency sweep | Operability | Load, scale & performance]
- **Trigger:** [concrete fact that schedules it]
- **Admission rationale:** [why it spans slices and was not decidable earlier]
**Scope**
- **In:** [affected slices/surfaces and shared mechanism]
- **Deferred:** [capability]
**Guardrails**
- **MUST:** [...]
- **MUST NOT:** [class guardrail plus item constraint]
**Acceptance criteria**
- [ ] [primary proof]
- [ ] [class-specific proof]
- [ ] [regression: affected slice criteria still pass]
**Definition of done:** [one measurable closing condition]

---
## ⏸ Explicitly Deferred / Out of Scope
- [aspect and rationale]
```


## After a Complete Proposal: Offer Persistence

After emitting a complete proposal, offer to turn its pullable items into a durable backlog. This is a next step, not part of slicing: never create a file or tracker item until the user explicitly confirms the destination and creation.

Apply this only when the stop gate did not fire. Infer the source from its explicit URL, key, and issue type, then make one concise offer in the user's language:
- **Jira Epic:** offer to create linked Jira **Stories** under that Epic.
- **Jira Story:** offer to create Jira **Sub-Tasks** under that Story.
- **GitHub Issue:** offer to create GitHub **sub-issues** under that issue. `sub-issues` is GitHub's term; do not call them GitHub subtasks.
- **Any other or ambiguous source:** ask whether to save the proposal as Markdown or use a destination the user selects.

When the user confirms a tracker destination, create one work item for each pullable Phase 0 enabler, Tracer Bullet, Phase 2+ slice, and admitted cross-cutting item. Preserve the parent-child relationship and record `Builds on` ordering where the destination supports it. Do not create items for explicitly deferred or out-of-scope work. If direct tracker creation is unavailable, return creation-ready item text and state that it has not been created.

---

## Worked Example: One Cross-Cutting Item

*Illustrates the expected level of specificity - named slices, named errors, real dates, measurable gates. It is not part of the output; never emit it verbatim.*

```markdown
### CC-1 — Replace the pricing-API fake with the real adapter
> **Goal:** Every production path that prices an order runs against the real partner API; the fake survives only as a test double.
- **Class:** Boundary realization
- **Trigger:** Partner pricing API reachable in the staging environment since 2026-03-04, sandbox credentials issued.
- **Admission rationale:** Slices 2.1, 3.2 and 4.1 all call the pricing port; each would otherwise carry its own switch from fake to real adapter. The real error behavior was unknown until the sandbox existed.
**Scope**
- **In:** Adapter for the existing pricing port, mapping of partner error codes and timeouts onto the port's declared errors, contract tests against the sandbox, per-environment configuration switch.
- **Deferred:** Bulk price lookup - the port exposes single lookups only; adding it is a vertical slice.
**Guardrails**
- **MUST:** The port interface stays unchanged; the fake stays usable in unit tests; prices observable to users are unchanged for the existing test data set.
- **MUST NOT:** Add partner-specific fields to the port while swapping the implementation; keep a runtime flag that allows the fake in production.
**Acceptance criteria**
- [ ] Given staging is configured against the sandbox, When an order is priced, Then the price originates from the partner API and appears in the order confirmation.
- [ ] Given the partner API returns 503 or exceeds the timeout, When an order is priced, Then the caller receives the port's declared `PricingUnavailable` error and no transport exception leaks.
- [ ] Given slices 2.1, 3.2 and 4.1, When their acceptance criteria run against the real adapter, Then they pass unchanged.
**Definition of done:** Contract test suite green against the sandbox in CI; the fake is referenced from test code only.
```
