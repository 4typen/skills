# SaaS classification edge cases

| Scenario | Default recommendation | Reason / exception |
|---|---|---|
| "Authentication" with years of mixed work | Product area, not Epic | Split into bounded outcomes and separate existing bugs and maintenance work. |
| One small customer-visible enhancement | Story without Epic | Do not manufacture hierarchy. |
| Bulk user deactivation | Epic with vertical Stories, if several coherent behaviors | One Story may suffice for tiny scope. |
| Frontend + backend + database for one user behavior | One Story | Technical layers are not separate customer outcomes. |
| Tests for a new Story | Part of Story completion | Separate Task only for independent regression/test infrastructure effort. |
| New API endpoint | Story when consumed API behavior is the product result | Method-only implementation within other Story is not a standalone Story. |
| Database index for known SLA breach | Bug or Task | Bug if correcting deviation from established expectation; Task for preventive optimization. |
| SDK/runtime upgrade | Task | Technical state. Technical Epic if a large multi-service transformation. |
| Legacy billing datastore retirement | Technical Epic | Bounded end state spanning migration, parity, cutover and verification. |
| Passkey feasibility | Spike | Output is evidence and a decision, not a promised feature. |
| Already released feature fails | Bug | Reference expected behavior and reproduce or provide evidence. |
| Problem found while original Story unfinished | Fix within Story by default | Separate Bug if independent tracking/security/incident policy requires. |
| Customer asks for absent feature | Opportunity or Story | Not a Bug without existing behavior contract. |
| Intermittent payment webhook failure | Bug | Logs, trace IDs and impact substitute for deterministic reproduction. |
| Security vulnerability | Bug/security finding or Task per policy | Apply security workflow; lack of observed exploit does not negate vulnerability. |
| Multiple customer reports of same root failure | One Bug, linked reports | Deduplicate without losing evidence or stakeholders. |
| Two Stories need the same library | Link dependency or one reusable Task | Avoid double-implementing or artificially sharing Epic parents. |
| Cross-team change for one business behavior | One Story if coordination manageable | May need linked technical Tasks; choose traceability over dogmatic slicing. |
| Feature delivered, KPI not improved | Close delivered Epic if criteria met, create follow-up decision | Delivery success is not impact proof. |
| Add many extras to near-finished Epic | Scope review, likely new Epic/Story | Protect agreed completion boundary. |
| Customer-specific customization | Story, Epic, or Opportunity depending approval/scope | Validate tenancy, maintenance and product strategy first. |
| API pagination migration/breaking contract | Epic or Task/Stories depending scope | Include versioning, migration, compatibility and adoption criteria. |
| AI-generated code/PR | Not automatically a Jira issue | Track the intended outcome, link implementation evidence. |
| AI-generated natural-language issue | Draft only | Validate provenance, privacy, duplication, and assumptions. |
| Feature hidden behind flag | Story may be done when verified in agreed environment | Activation/rollout may need separate work or criteria per policy. |
| Ticket called "miscellaneous fixes" | Split, classify, or close | No coherent completion outcome. |

## When type is ambiguous

Classify by **what is being tracked**, not by which engineering technique will be used. For a latency issue, an established performance promise breached suggests Bug; a new speed goal suggests Story/Epic; adding an index as planned preventive work suggests Task. Explain the chosen interpretation.

## When not to split

Avoid splitting one coherent behavior only to keep every issue tiny; avoid an independent "Add validation", "Write tests", "Build UI" trio when they jointly define one acceptance outcome. Split if each slice has separate acceptance evidence, release value, review ownership, or risk requiring individual tracking.
