---
name: jira-outcome-work-management
description: Organize SaaS development work in Jira using outcome-oriented Epics and precise Stories, Tasks, Bugs, and Spikes. Use when capturing new requirements, choosing issue types, refining an issue, splitting or merging Stories/Epics, cleaning up a backlog, detecting duplicates, moving ideas into delivery, reviewing issue quality, or preparing Jira issue changes. Avoid sprint planning, boards, velocity, and Jira administration unless explicitly requested.
author: André Schubert
date: 2026-10-15
updated: 2026-10-15
---

# Jira Outcome Work Management

## Purpose

Make Jira a trustworthy representation of **why work matters, what will change, and how completion can be checked**. Prevent catch-all Epics, technical-layer Stories, pseudo-hierarchies, unnecessary tickets, and a permanent dumping-ground backlog. Optimize for SaaS products, including AI-assisted engineering.

This skill provides **product-work conventions**, not universal Jira or Scrum rules. Apply local policy when it is explicit; identify conflicts instead of silently overriding it. Default language: respond in the user's language; write Jira artifacts in the project's established language. Use short, precise sentences and terms.

## Scope

Use this skill for:
- Capturing new feature requests, customer feedback, maintenance work, defects, technical initiatives, and investigations.
- Classifying and creating Epic, Story, Task, Bug, and optional Spike proposals.
- Drafting acceptance criteria and outcome-based issue titles.
- Reviewing, splitting, merging, closing, linking, or relocating issues and Epics.
- Triage of a noisy backlog; distinguishing ideas from delivery commitments.
- Reviewing whether proposed AI-generated work is necessary and safe.

Out of scope by default: sprints, boards, workflow column design, estimations, velocity, release management, and Jira permissions/configuration. Mention only when needed for context or if asked.

## Operating contract

1. **Understand before creating.** Determine the underlying problem, beneficiary, expected behavior, urgency, evidence, and whether related work already exists.
2. **Search before duplicating.** When Jira/search access exists, inspect likely duplicates, existing Epics, product areas, and current behavior. Never claim a search occurred unless a tool returned evidence.
3. **Choose the smallest useful artifact.** An isolated Story or Task does not need a decorative Epic. Do not create implementation subtasks by default.
4. **Separate problem, outcome, and solution.** State assumptions, unverified claims, and open decisions explicitly.
5. **Write an independently testable completion condition.** Use measurable criteria where the product needs them; avoid invented thresholds.
6. **Distinguish parentage from links.** A child belongs to the Epic's delivery scope; a dependency or related incident is only linked.
7. **Preserve history.** Never delete, bulk-close, move, or rewrite Jira issues without explicit authorization. Prepare a change plan, mapping, and reversible steps first.
8. **Human review for consequential actions.** Treat AI-suggested classifications, prioritization, scope, and generated code as drafts. Never claim completion, release, testing, or customer impact without evidence.
9. **Minimal data, minimal tickets.** Avoid unnecessary fields and exposing credentials, personal data, tenant data, support attachments, or secrets to unapproved AI tools.

## Routing: what to do for common requests

| User intent | Procedure | Read |
|---|---|---|
| Capture a new requirement | Intake -> search -> classify -> draft -> gaps -> recommendation | `references/issue-taxonomy.md`, `references/intake-and-backlog.md`, `references/templates.md` |
| Create or improve an Epic | Outcome + boundaries -> child scope -> completion -> links | `references/issue-taxonomy.md`, `references/templates.md` |
| Create or improve a Story | One testable behavior -> acceptance criteria -> dependencies | `references/issue-taxonomy.md`, `references/templates.md` |
| Classify maintenance work or a defect | Actual vs expected -> choose Bug, Task, Story, or Spike | `references/issue-taxonomy.md`, `references/edge-cases.md` |
| Restructure an Epic or Stories | Inventory -> map outcomes -> split/merge -> preserve links -> migration plan | `references/restructure.md`, `references/edge-cases.md` |
| Clean backlog | Inventory -> group duplicates -> decide active, discovery, archive -> review | `references/intake-and-backlog.md`, `references/restructure.md` |
| Audit ticket quality | Evaluate rubric -> propose minimal edits and questions | `references/quality-gates.md` |
| AI-assisted ticket generation | Propose only necessary issues -> flag assumptions -> enforce review | `references/ai-guidance.md` |

Read relevant reference files before executing a complex case. For a simple request, follow the abbreviated rules below.

## Core taxonomy: authoritative defaults

| Type | Defining question | Completion evidence | Typical children |
|---|---|---|---|
| **Epic** | What coherent larger product or technical capability will exist after delivery? | Explicit capabilities and scope delivered and checked | Related Stories, Tasks, sometimes delivery Bugs |
| **Story** | What specific user, external consumer, or system behavior will change? | Acceptance criteria demonstrate the new behavior | Only optional implementation subtasks |
| **Task** | What necessary technical, operational, or documentation work must be performed? | Concrete work product or technical end state | Only optional subtasks |
| **Bug** | How does actual behavior differ from established expected behavior? | Problem fixed, verified, regression risk addressed | Usually none |
| **Spike** *(optional)* | What specific uncertainty must we resolve? | Documented evidence, decision/recommendation, time boundary | None |

An **Initiative/Outcome** describes strategic intent. An **Opportunity** describes a customer problem or unmet need. They are conceptual upstream objects, not necessarily standard Jira issue types. Use the available product-discovery system or links. Do not assume Jira license-specific custom hierarchy exists.

**Epic ≠ product area.** Long-lived categories such as "Authentication", "Frontend", "Customer Management", or "Tech Debt 2026" belong in product area/component/taxonomy fields, not Epics. **Story ≠ technical layer.** Do not automatically create one Story each for frontend, backend, database, and tests. **Task ≠ inferior Story.** Legitimate technical work does not need a fictional user persona. **Bug ≠ new wish.** A new feature request without prior expected behavior is not a defect.

## Decision flow

1. Is there **observed deviation** from an established expectation? -> **Bug**, with evidence and impact. If discovered inside an unfinished Story, usually fix inside that Story unless independent tracking is needed.
2. Is the work mainly **learning to resolve a specific uncertainty**? -> **Spike** (or labeled Task if Spike is not available).
3. Is the deliverable **a new/changed testable behavior** for a person, API client, service, or external system? -> **Story**.
4. Is it **necessary work without an independently useful behavior change**, such as runtime upgrade, migration preparation, standalone performance test, or documentation cleanup? -> **Task**.
5. Does the request encompass **multiple coherent, independently checkable pieces** required for a larger bounded end state? -> **Epic** with only the currently needed children.
6. Is it **unvalidated / not chosen for delivery**? -> **Idea/Opportunity in discovery**, not an automatically committed Engineering issue.
7. Unclear? Give a recommended type, reasoning, assumptions, and at most the smallest set of questions needed for a useful draft.

Size is a signal, never the definition. Avoid fixed day counts or Story Point cutoffs. Small features can be single Stories. Technical transformations can be Epics. Outcomes need not promise a measurable business KPI, but Epics do need concrete **delivery completion criteria**. Distinguish achieved delivery from measured post-release product impact.

## Standard procedure: new requirement

1. Summarize the source and problem in one to three plain sentences; distinguish the requester's solution from observed need.
2. Record evidence and context: affected role/tenant/integration; current behavior; desired behavior; urgency; constraints; scope; links. Do not fabricate data.
3. Check duplicates, parent candidates, and whether the work belongs in discovery or delivery. If access unavailable, mark this check `Not verified`.
4. Recommend one Issue type and explain why in one sentence. If necessary, propose an Epic and *only* immediately useful child Stories.
5. Draft the appropriate artifact using `references/templates.md`. Use precise outcome titles and clear, observable acceptance criteria. Explicitly list unknown decisions.
6. Check quality using `references/quality-gates.md`; look for role/permission errors, multi-tenant isolation, security, privacy, backwards compatibility, failure states, auditability, performance, monitoring, and migrations only when relevant. Never add irrelevant boilerplate.
7. Return a ready-to-copy Jira draft, proposed parent/links, concise rationale, and unresolved questions. Creation/updates require permission and available Jira tools.

## Standard procedure: restructure existing work

1. Inventory existing Epic, children, links, statuses, known customer commitments, and relevant artifacts. If no Jira access, work from provided content and label gaps.
2. Detect smell types: evergreen Epic; multiple unrelated outcomes; split by layers; duplicate Stories; tasks posing as Stories; stale speculative work; bugs attached solely by product area.
3. Define target Epic outcomes and completion boundaries. Map every existing issue to **keep**, **move**, **split**, **merge**, **link only**, **convert**, **discovery**, or **archive candidate**. Prefer preserving issue keys and audit trail.
4. Explain risks: existing dependencies, PR links, customer references, status semantics, automation, reports, and duplicates. Do not silently discard historic context.
5. Return a **before -> after mapping table** with reasons, suggested new artifacts, links, and an implementation sequence. Ask for approval before applying bulk or destructive changes.

## Output modes

For a **new requirement**, return:
- **Recommendation:** classification + discovery/delivery placement.
- **Jira draft:** title, problem/context, expected outcome or behavior, acceptance/completion criteria, in/out of scope where needed, relevant constraints, parent/links.
- **Checks:** duplicates/search status, dependencies, security/data risks when relevant, assumptions/open questions.

For **restructuring**, return:
- **Findings:** structural problems, with concrete examples.
- **Target model:** bounded outcomes/Epics and issue hierarchy.
- **Migration mapping:** old key -> action -> new parent/type -> reason.
- **Risks and approval points.**

For **quality review**, return the short rubric result, changes ordered by impact, and an improved draft; do not only provide abstract feedback.

## Non-goals and pitfalls

- Do not optimize for issue count, Epic count, Story Point totals, or AI-produced code volume.
- Do not write a Story per component/layer by default, or a Bug for an unapproved feature request.
- Do not require every Story/Task/Bug to have an Epic.
- Do not use the active backlog as an infinite idea archive.
- Do not enforce rigid "As a ... I want ... so that ..." phrasing when a clear descriptive title is better.
- Do not create separate "write tests" work by default; tests usually belong in completion criteria of the behavior delivered.
- Do not treat "Done" on the Epic as proof of business impact. Record impact separately when evidence exists.
- Do not prescribe project configuration or assume paid Jira features; focus on artifact semantics.

## Reference files

- `references/issue-taxonomy.md` - exact definitions, acceptance boundaries, examples.
- `references/intake-and-backlog.md` - ideas, opportunities, prioritization, archive policy.
- `references/templates.md` - ready-to-copy Epic, Story, Task, Bug, Spike drafts.
- `references/restructure.md` - detailed refactoring and migration procedure.
- `references/edge-cases.md` - difficult SaaS classification cases.
- `references/quality-gates.md` - scorecards and issue review questions.
- `references/ai-guidance.md` - AI safety, context, duplication and governance.
- `examples/scenarios.md` - end-to-end SaaS examples, including a before/after Epic transformation.
