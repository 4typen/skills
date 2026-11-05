---
name: tracer-bullet-slicing
description: Slice a feature into blocker-removal tickets, one Tracer Bullet, and fanned-out vertical slices.
disable-model-invocation: true
author: André Schubert
date: 2026-09-24
updated: 2026-11-05
---

# Tracer Bullet Slicing

Slice a feature into tickets that never block the developer. Find blockers and hidden complexity first and give each its own ticket. Then cut one Tracer Bullet, then thin vertical slices.

**Leading rule: zero blockade.** After stage 1, the developer builds the Tracer Bullet without waiting for another team, a third party, or an unfinished upstream feature. After stage 2, the same is true for every stage 3 slice.

> Make the change easy, then make the easy change.

A **Tracer Bullet** is production code: the thinnest real path through the whole system. It stays in the codebase and grows.

## 1. Normalize the requirement

State the **actor**, the **trigger**, the **observable outcome**, the **rules and constraints**, and the **boundaries touched** (external systems, other teams, upstream data, downstream consumers). Mark missing points as unclear. Look for the answers in the codebase first; section 3 decides which ones to ask.

If the requirement adds no new behavior, say so in one line and stop. This applies to a pure structural change, a defect fix, or an investigation. Vertical slices need new behavior.

## 2. Audit against the codebase

Record which repositories you need and whether you can access them. Probe each category:

1. Upstream data and events
2. Downstream consumers and contracts
3. External systems and third parties
4. Persistence and data lifecycle
5. Identity, permissions, and compliance
6. Runtime and infrastructure (environments, queues, secrets, configuration, feature toggles)
7. Delivery and verification (pipeline, test infrastructure, test data)

Give each finding a verdict: **ready**, **blocked**, or **unclear**. Ready and blocked need a code finding or a named external confirmation. An assumption or missing access gives unclear. Name the evidence for each finding.

**Shared path:** if the feature changes an existing shared path, check all existing callers, background jobs, and test setups. Fix what breaks before or in the ticket that changes the path.

## 3. Blocking questions

For each unclear point, play through 2–3 plausible answers. The question is **blocking** if the answers lead to a different ticket list, port contract, Tracer Bullet path, acceptance criteria, or security and permission rules. If not, record it as an open decision on the affected ticket and state the assumed answer.

With one or more blocking questions, give only the normalized requirement and the questions, then stop. For each question, use this format:

**Recommended:** [answer and reason]
**Alternative:** [one other answer]

If nobody can answer a question now, recommend how to clarify it, then stop. Slice again when the answer is known.

## 4. Stage 1 · Make the change easy

Every blocked finding becomes a ticket here that removes or isolates the blocker. Every stage 1 ticket is work the team can do itself. If a blocker needs work by another team, isolate it behind a port with fake; the real work goes to "Waiting for trigger". If a blocker cannot be isolated, name it and stop. Internal groundwork comes here only if it blocks the Tracer Bullet or at least two slices and has a measurable done criterion; otherwise it stays inside the slice that needs it. Each stage 1 ticket names what it unlocks. Split a large restructuring into tickets that can each be verified alone. Typical tickets:

- **Port with fake:** an external source is not ready, for example events that another module does not send yet. Derive the port from how its callers will use it, and check that the real producer can deliver this data; if that is unclear, apply section 3. Data from the fake stays apart from real user data and causes no real external side effects. Results based on the fake stay invisible to real users until the real source is verified.
- **Missing mechanism:** for example, the requirement asks for a feature toggle, but there is no toggle mechanism.
- **Restructuring:** the existing structure makes the feature hard to build.
- **Migration or provisioning** that the team can do itself.

A ticket is never a layer such as "schema", "endpoints", or "screens".

## 5. Stage 2 · Tracer Bullet

Make one path real: trigger → contract → logic → persistence → observable result → delivery. Every station is real or N/A with a one-line reason. Only a stage 1 port may use its fake.

- **Lower bound:** every station is real, and the bullet touches the biggest architectural risk of the feature.
- **Upper bound:** one trigger, one input, one rule, one path. Everything else is a variant and belongs in a slice.
- **Test:** if you remove something, a station is no longer real. If you add something, it is a variant.
- **Deliverable at any time:** mergeable and deployable, with tests and lint green. A toggle may hide it from users.

On the ticket card, list the stations under **Result**.

The Tracer Bullet is the **anchor** for stage 3. If the feature has no new end-to-end path, the anchor is the thinnest vertical slice. Say why in one line. Do not invent an artificial Tracer Bullet.

## 6. Stage 3 · Make the easy change

If the Tracer Bullet already covers the whole requirement, leave out stage 3 and say so in one line.

Cut the remaining scope along five dimensions:

1. **Data variance:** default → dynamic → multiple entities → batch
2. **Business rules:** structural validation → hard invariants → soft warnings
3. **Interaction depth:** basic control → loading, error, and empty states → rich interaction
4. **Edge cases:** concurrency, retry, recovery, conflict, undo
5. **Reach:** more actors, permissions, bulk paths, export

Each slice has one goal in one sentence and moves one dimension. Put a "must not" rule in the same slice as the behavior it limits. Slices build on stage 1 and the anchor, so slices fan out by default. If several slices need the same groundwork, move it to stage 1. If a slice needs the result of another slice for business reasons, a chain is allowed; state the reason under "Builds on". Map every rule, constraint, and outcome from section 1 to an acceptance criterion or to an exclusion with a reason. Existing guarantees that the feature touches, such as documented response times or SLAs, stay valid and become acceptance criteria. Plan new quality attributes such as performance or monitoring only when the requirement names them. They become acceptance criteria of the slice that needs them.

## 7. Waiting for trigger

Every fake gets exactly one ticket that replaces it with the real source. The ticket names its **trigger**, for example "module X sends event Y in staging", and the fake ticket it replaces under **Context**. The ticket is done when contract tests against the real system cover success and failure cases, the port contract is unchanged, the affected slice tests still pass, and the restriction that hid fake-based results from real users is removed. These tickets are blocked by definition, so keep them apart from stages 1–3.

## Output

Write in the user's language, including headings, field labels, and Given / When / Then, and follow ASD-STE100: short sentences, one idea per sentence, active voice, one term for each concept.

1. **Normalized requirement**
2. **Audit:** only the findings that lead to a ticket or a question, plus one line: "Checked, no finding: [categories]".
3. **Stage 1, stage 2, stage 3, waiting for trigger.** Separate the sections with `---`. Number the tickets `1.1`, `2.1`, `3.1`, `W.1`, and so on.

Use one ticket card for all tickets. Leave empty fields out.

- **Title:** [actor/system] can [behavior], or [technical result]
- **Context:** why the ticket is needed
- **Result:** the one capability or technical end state
- **Acceptance criteria:** Given / When / Then, plus error, permission, and compatibility cases when relevant
- **Constraints / non-goals:** only the important ones
- **Builds on:** earlier tickets
- **Open decisions:** non-blocking only, with the assumed answer

Mark every assumption as an assumption. Describe the observable result, not files, classes, or lines; the developer and the agent find these in the code. Name affected modules, contracts, and entry points when the audit found them.
