# Jira-ready templates

Use the minimal version that helps the recipient. Remove empty optional sections; never manufacture details to fill them.

## Epic

**Title:** [Deliverable capability or end state]

**Problem / context:** [Who is affected; why does it matter; relevant evidence]

**Desired delivery outcome:** [What will be possible or true when complete]

**Completion criteria:**
- [Observable end-state criterion]
- [Relevant security/operational criterion]

**In scope:** [Bounded list]

**Out of scope:** [Explicit exclusions]

**Links / references:** [Discovery item, design, architecture, source feedback]

**Optional impact measure:** [How to observe whether customer/business impact occurs after delivery; no invented targets]

**Open decisions:** [Unresolved questions and owners]

## Story

**Title:** [Actor/system] can [specific behavior] / [new observable system behavior]

**Context:** [Why this behavior is needed]

**Expected behavior:** [The single primary capability]

**Acceptance criteria:**
- Given [context], when [action], then [observable result].
- [Relevant permission / tenant isolation / error behavior]
- [Relevant compatibility or audit criterion]

**Constraints / non-goals:** [Only material constraints]

**Parent Epic (if applicable):** [Epic key]

**Dependencies / references:** [Issue and source links]

**Open decisions:** [Do not invent unspecified behavior]

## Task

**Title:** [Action] + [target technical/operational outcome]

**Purpose:** [Why this work matters]

**Work result:** [Artifact, configuration, migration, decision, or technical end state]

**Verification / done:** [Tests, review, rollout or evidence appropriate to the work]

**Constraints / dependencies:** [When needed]

**Parent Epic:** [Only if in scope]

## Bug

**Title:** [What fails] + [condition / impact]

**Observed behavior:** [What happens]

**Expected behavior:** [What should happen and basis]

**Affected environment and scope:** [Version, integration, tenant category, timestamps if relevant]

**Reproduction / evidence:** [Steps or logs/traces/screenshots without sensitive data]

**Impact / severity:** [Effect and urgency; severity separate from priority]

**Resolution verification:** [Behavior fixed, regression test, additional audit if needed]

**Links:** [Incident, related Stories, duplicate canonical issue]

## Spike

**Question:** [One decision-blocking unknown]

**Context:** [Why answer is needed]

**Time boundary:** [Agreed research limit; do not invent]

**Expected output:** [Findings, options, risks, evidence, decision/recommendation]

**Exit criterion:** [Named uncertainty resolved enough to decide]

## Example end-to-end Epic and Story

**Epic:** "Administrators can deactivate multiple user accounts in one action"
- Problem: Enterprise admins currently deactivate accounts one by one.
- Delivery outcome: Role-authorized bulk deactivation with confirmation and traceable changes.
- Scope: select accounts, confirm, perform action, handle partial errors, audit changes.
- Out of scope: scheduled deactivation, imports, role redesign.
- Impact hypothesis: lower admin effort and fewer support requests; measure separately.

**Story:** "An administrator can select several active accounts and deactivate them"
- Given admin permission and a selection, when bulk deactivation is confirmed, then selected accounts are deactivated and recorded in the audit log.
- Unauthorized users cannot perform the action.
- Partial failure displays which accounts failed without falsely reporting success.
- Does not require frontend/backend/testing Stories by default.
