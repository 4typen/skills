# Lens: UI Behavior, Client State & Accessibility (`ui-state-a11y`)

Inspect changed frontend surfaces as a keyboard/screen-reader user on a slow, lossy connection with rapid interactions, route changes, and non-default locales. Preserve **blind quarantine**.

## Inspection protocol

1. **Trace state lifecycle**: Follow every component input, store/signal/selector, async effect, and form control from initial load through pending, empty, error, rapid re-trigger, and component teardown.
2. **Walk interaction & assistive tree**: Trace keyboard tab/focus flow, ARIA semantics, accessible names, and localization keys across changed templates and styles.

## Hunting vectors

- **Async UI races & stale state**: Earlier slow HTTP responses overwriting newer selections (`mergeMap`/`concatMap` where `switchMap` or abort is required), double-submission while a save is in flight, optimistic state left corrupted when the request fails, mutated store/signal references breaking change detection (`OnPush`/memoized selectors), and subscriptions firing after destroy.
- **Incomplete UI states & form traps**: Missing or misleading loading, empty-result, partial-failure, offline, or permission-denied states; validation errors swallowed or stuck after field reset; unsaved user input silently discarded on dialog close, filter change, or route navigation.
- **Keyboard, focus & WCAG 2.2 gaps**: Click handlers bound to `div`/`span` without `<button>` semantics or keyboard activation, icon-only controls or form inputs missing programmatic accessible names (`aria-label`/`label`), focus lost or trapped improperly when modals/drawers/menus/rows open or delete, and dynamic errors/toasts unannounced to assistive tech (`aria-live`/`role="alert"`).
- **Localization, layout overflow & client security**: Hardcoded user-facing text, translation keys missing in one or more locale files, broken plural/date/number formatting, long translated labels overflowing/clipping action buttons without responsive wrap, and unsanitized HTML/URL bindings.

**Done when**: Every changed component, store/signal/effect, form flow, template interaction, and translation key has been traced across async race paths, UI error/empty states, WCAG keyboard/focus/name rules, and locale completeness.
