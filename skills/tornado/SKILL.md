---
name: tornado
description: "Strategic programming (Ousterhout): deep modules, information hiding, and preparatory refactoring at agent speed. Use for nontrivial feature work, module-boundary changes, refactoring, or when the user says 'strategic', 'strategic tornado', 'deep module', or 'design it twice'."
---

# Strategic Tornado

Move at tornado speed with a strategic investment mindset: deliver correct behavior while leaving the system no harder to understand. Optimize for complexity after the change, not diff size; keep structural changes proportional to their benefit and risk.

## Steps

### 1. Locate the seam

Read the target module and its callers. Find information leakage: implementation details callers must know, repeated wiring, misplaced responsibilities, or shared assumptions. If the boundary already fits, keep the change local.

**Done when:** You can name the exact boundary and caller burden to remove, or explain why no boundary change is needed.

### 2. Design it twice

Before editing, compare two designs (silently unless the trade-off needs user judgment):

- The natural local change.
- A deep-module alternative: a focused interface that hides more behavior and edge cases, eliminates avoidable error states without hiding real failures, and pulls complexity downward.

Choose the design with the lowest overall complexity, accounting for coupling, migration cost, and regression risk. Fewer methods and smaller diffs are not goals in themselves.

**Done when:** You can explain why the chosen design is simpler to understand and change, including its costs.

### 3. Make the change easy, then make the easy change

If the chosen design needs a cleaner seam, refactor it first; then place new behavior in the module that owns it rather than adding caller-side special cases, pass-through wrappers, or temporal coupling. Avoid speculative refactors whose cost or risk outweighs their benefit.

If a refactor changes a shared contract or materially expands scope, present the strategic and tactical options with their costs and ask before proceeding. Run relevant tests for affected callers; report anything not verified.

**Done when:** Behavior is verified as far as practical and no avoidable caller-facing complexity was added.

### 4. Boy Scout check

End your reply with a two-line strategic ledger:

**Pulled downward:** Which complexity was absorbed, or why none was.
**Interface delta:** Whether the caller-facing boundary became simpler, stayed flat, or grew, and why.
