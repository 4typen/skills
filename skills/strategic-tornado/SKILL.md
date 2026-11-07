---
name: strategic-tornado
description: "Strategic programming (Ousterhout): deep modules, information hiding, and preparatory refactoring at agent speed. Use when implementing features, changing module boundaries, refactoring, or when the user says 'strategic', 'strategic tornado', 'deep module', or 'design it twice'."
---

# Strategic Tornado

Operate at tornado speed with a strategic investment mindset: the primary output of every change is a cleaner system design; working code is only the baseline. Optimize for the system's complexity after the change, not the size of the diff.

## Steps

### 1. Locate the seam
Read the target module and its callers. Identify the **information leakage**—where internal details leak, responsibilities are misplaced, or callers share assumptions and repeat wiring across files.
- **Done when:** You can name the exact boundary and the complexity that belongs behind it.

### 2. Design it twice
Before editing, sketch two contrasting designs for the change (silent unless the trade-off needs user judgement):
1. The natural local change.
2. A **deep module** alternative: a simpler, narrower interface hiding more functionality and edge cases behind it (**define errors out of existence**, **pull complexity downward**).

Pick the design that leaves the system simplest to understand and change, even if its diff is larger. Prefer fewer caller-facing assumptions over fewer lines of code.
- **Done when:** The chosen interface has fewer or simpler entry points and caller assumptions than the alternative.

### 3. Make the change easy, then make the easy change
When the existing structure resists the chosen design, perform a **preparatory refactoring** first so the new behaviour slots in as a natural extension. Fold the new behaviour into the right abstraction rather than stacking a special-case branch or wrapper on the outside. Create a new abstraction when no existing one owns the concept.

If the refactoring changes a shared contract or significantly expands scope, present the strategic and tactical options with their costs and ask before proceeding.
- **Done when:** The change lands without adding caller-facing special cases, pass-through methods, or temporal coupling, and all affected callers and tests pass.

### 4. Boy Scout check
End your reply with a two-line strategic ledger:
- **Pulled downward:** Which complexity or special case was absorbed into the module, or what remains unresolved.
- **Interface delta:** How the boundary facing callers became simpler, stayed flat, or grew—and why.
