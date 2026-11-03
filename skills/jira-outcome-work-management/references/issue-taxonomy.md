# Artifact taxonomy and decision rules

## Epic

**Definition:** A coherent, bounded product or technical end state that takes multiple smaller, independently verifiable units of work to deliver.

**Rules:** (1) State beneficiary/problem and end state. (2) Set in/out scope. (3) Define verifiable delivery completion. (4) Group only children necessary for that end state. (5) Close when delivered, even if long-term impact data is pending. (6) Don't reuse as an evergreen category. (7) Don't create an Epic just to hold a single small Story. (8) New scope is a conscious change, not automatic inclusion.

Good: "Administrators can deactivate multiple accounts in one operation"; "Legacy billing store can be retired without interrupting invoice processing"; "Customer list loads within the agreed threshold at 10k records" (threshold must be specified by stakeholders).

Bad: "User Management"; "All frontend work"; "Tech Debt"; "2026 improvements"; "Misc backlog".

Epic KPIs: Separate **delivery criteria** (what was shipped/verified) from **product outcome measure** (did support requests fall?). Do not hold an Epic open indefinitely for a lagging KPI unless explicit policy requires it.

## Story

**Definition:** A small, independently checkable product/system behavior. May serve users, API consumers, administrators, automated systems, or support staff.

**Rules:** (1) Define expected behavior. (2) Observable acceptance criteria including relevant error and permission cases. (3) Prefer end-to-end vertical slice rather than separate frontend/backend/test tickets. (4) Link dependencies rather than inventing hierarchy. (5) A feature flag does not invalidate a Story if verifiable in the agreed environment. (6) Avoid needless implementation prescriptions. (7) No forced user-story sentence template.

Good: "Tenant admin can revoke an API key"; "Webhook consumers receive a payment-completed event"; "A user can retry a declined payment".

Bad: "Implement REST endpoint" without contract/consumer behavior; "Create table" as a feature Story; "Write unit tests" as an independent feature Story.

A cross-cutting technical component can live within a Story when it is needed for that behavior. If a reusable foundation is independently owned and verified, create a linked Task (or technical Epic if substantial).

## Task

**Definition:** Necessary work with a concrete technical, operational, architectural, or documentation output; not naturally expressed as a distinct feature behavior.

**Rules:** Give purpose, target artifact/end state, verification, and constraints; link to an Epic if it is in that scope. Valid independent tasks include runtime upgrades, infrastructure preparation, large one-off test execution, remediation, documentation cleanup, migration preparation, and CI improvements. Don't turn every code method into a Task.

Good: "Replace unsupported runtime for billing service and verify CI and deployment". Bad: "Create deactivateUser()" if merely a step in an existing Story.

## Bug

**Definition:** A supported discrepancy between observed and established expected behavior. Expected behavior can come from requirements, product contracts, normative security controls, or intended system guarantees.

**Required:** observed vs expected; environment/version/tenant scope where appropriate; evidence/repro or logs/trace; impact; proposed verification. Distinguish **severity** (impact) from **priority** (when to fix). Respect security/incident escalation policy.

Existing released feature broken -> Bug. New desired feature -> discovery/Story. Found before a Story is complete -> generally fix within Story; separate Bug if cross-cutting, independently tracked, or report/audit demands.

No reproducible steps? Accept event evidence and diagnostic plan for intermittent failures. Avoid rejecting legitimate incidents.

## Spike (optional)

**Definition:** Time-bounded attempt to resolve one clear uncertainty, with evidence, options, risks and recommendation as output. A prototype may be a means, not the default definition of completion. If no Spike type exists, use a labeled Task. "Research authentication" is too broad; "Can our identity provider support passkeys under our tenant policy?" is bounded.

## Parent vs link

Parent/child means part of a shared **delivery scope**. `blocks`, `depends on`, `relates to`, `caused by`, or `duplicates` represents an issue relationship. A production Bug discovered years later is not automatically a child of a closed delivery Epic. A Story should not have two parents; link cross-cutting work instead of cloning.

## Product area vs Epic

Use a stable product area/component taxonomy for Identity & Access, Billing, User Management, Data Export, Platform, etc. Epics come and go; the product area persists. Avoid ungoverned labels as pseudo-parent objects when a controlled field is available.
