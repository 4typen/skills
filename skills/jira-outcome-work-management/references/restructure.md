# Restructure Epics, Stories, and backlogs safely

## Goal

Replace container-driven groupings with outcome-driven work, while preserving history, links and commitments.

## Diagnostic signs

- Evergreen Epic named for product module, team, calendar year, or miscellaneous domain.
- Epic with no completion statement, unbounded inflow or dozens of unrelated tickets.
- Stories representing frontend/backend/database/test layers rather than testable behavior.
- Different issues describing same need or root defect.
- Single development ticket that lists multiple unrelated outcomes.
- Old Bugs under a closed Epic only because they share product area.
- Active backlog full of speculative, obsolete, duplicate, or unowned items.

## Procedure

1. **Inventory:** Export issue keys, titles, descriptions, types, parents, statuses, links, issue ownership, project/team, external references, PRs, known contractual/security constraints and customer communications. Mark unknowns. If possible, include modification history before planning changes.
2. **Cluster by outcome:** Group based on customer/system result, not technical layer. Keep stable product area tagging separate.
3. **Propose target Epics:** Each has a title, problem, explicit completion, in/out scope. Do not create new Epics without evidence that hierarchy is useful.
4. **Classify each child:** Keep, move, split, merge, convert type, link only, move to discovery, close/archive candidate. Determine whether child is still active or delivered.
5. **Check dependencies:** A Story with two conceptual Epics has one delivery parent and links to the other; never duplicate just to place under both.
6. **Protect history:** Prefer moving/reparenting existing keys over deletion. When merging, select canonical issue, link duplicates, preserve unique evidence and customer references, and only then close duplicates with rationale.
7. **Propose execution order:** Create target Epic(s) -> set taxonomy -> prepare mapping -> update links/parents in small batches -> verify -> archive container Epic with explanation. Communicate changes to affected teams and stakeholders.
8. **Approval:** Obtain explicit human approval before executing create/update/bulk close/move/archive operations; respect permission and change policies.
9. **Validate:** Every previously active issue is accounted for; no lost customer commitment, backlink, incident trail, PR, or unresolved dependency; new Epics have finite outcomes.

## Migration map output

| Existing key | Existing type/parent | Proposed action | New type/parent or link | Reason | Risk / evidence |
|---|---|---|---|---|---|
| PROJ-101 | Epic: User Management | Replace/close after mapping | Product area: Identity & Access | Evergreen container | Preserve historical links |
| PROJ-113 | Story under PROJ-101 | Move | Epic: Bulk deactivate users | Coherent behavior | Existing PR link |
| PROJ-150 | Bug under PROJ-101 | Link only / make independent | No parent; product area Identity & Access | Production defect unrelated to current delivery | Incident reference |

Do not invent actual keys in live operations. The keys above are examples.

## Splitting oversized Stories

Start with the end-to-end behavior, then split along user scenarios, business rules, permissions, input classes, happy path vs complex variants, operational capabilities, or data sizes **only if each produces verifiable value**. Preserve cross-cutting security and quality in all relevant slices. Do not split into UI/API/DB as the default.

## Merging duplicates

Choose canonical issue by completeness, active implementation links and stakeholder traceability, not simply oldest key. Transfer missing criteria/evidence, mark duplicates and their source references, preserve comments and history as permitted. Do not assume Jira supports lossless merging; usually link and close duplicates rather than deleting records.
