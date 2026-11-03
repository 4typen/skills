# End-to-end examples

## 1. New customer request: "Export users to CSV"

**Intake:** Is the need a one-time export? Should filters apply? What data fields and permissions are allowed? Is this a GDPR/tenant data consideration? Search prior exports/requests (or mark search not verified).

**Recommended classification:** Opportunity if not chosen; Story if one small committed behavior; bounded Epic if multiple meaningful export capabilities will be delivered.

**Initial Story:** "Authorized administrators can export the currently displayed user list as CSV".

**Acceptance checks:** export returns rows within requesting tenant; permissions enforced; selected supported fields defined; CSV escaping works; failures visible; no secrets included. Specific size/performance limits need product agreement, not AI invention.

**Possible later Stories if needed:** Filters affect export; very large exports processed asynchronously. Avoid separate "Frontend button", "Backend endpoint", "Database query", "Tests" Stories.

## 2. Old container Epic: "User Management 2026"

**Before:** Contains onboarding, permission fixes, account deletion, UI polish, security bugs and a runtime update.

**After:** Product area stays "Identity & Access". Create bounded Epics only for coherent larger outcomes, e.g. "Administrators can bulk deactivate users" or "Users can self-serve expired invitations". Move selected delivery Stories under corresponding Epic. Keep independent production Bugs as Bugs with product-area tag and incident/reference links. Classify runtime update as independent Task unless a technical transformation Epic exists. Keep speculative account deletion request in discovery until chosen.

**Migration rule:** Do not close or delete original Epic until children and external links have been mapped and approved. Attach a migration summary in the old Epic and preserve searchability.

## 3. Billing performance issue

A customer reports invoice list slower than an agreed latency commitment under an observed workload. If evidence confirms a violated expectation, classify as **Bug** and record environment, dataset, latency, traces, and severity. If no performance contract existed and the product chooses to improve UX, use Story/Epic for an explicitly agreed new target. "Add database index" might be a Task inside the remediation plan but does not replace the externally observed outcome.

## 4. Legacy service migration

**Epic:** "Invoice processing no longer depends on legacy billing database".

**Completion:** migration strategy reviewed; new read/write path meets agreed parity; cutover verified; legacy access disabled; rollback/retention needs handled. Child work may be technical Tasks and behavior-oriented Stories. Close based on verified technical end state, not a forced customer-facing persona.

## 5. Security bug found during an unfinished feature

A missing authorization check is found in a Story under development. Usually fix and test within the Story. If it affects released routes or triggers incident/security tracking, create a separate security Bug and link it. Never understate severity because it was discovered by AI.

## 6. Spike: passkey support

**Question:** "Can the current identity provider support passkeys for all supported tenant policies?"

**Output:** verified provider capabilities, constraints, trade-offs, optional prototype evidence, and recommended next decision. Do not write delivery Stories until the option has been chosen.
