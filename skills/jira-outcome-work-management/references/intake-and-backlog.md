# Intake, discovery, and backlog hygiene

## Three distinct inventories (logical, not necessarily three Jira projects)

**Idea repository:** Feedback, requests, hypotheses and opportunities with uncertain value or no delivery commitment. Capture source, problem, evidence, requester need, date, links. Do not demand engineering detail.

**Product backlog:** Reviewed product opportunities and proposed increments with clearer value, options, owners/decision authority, and relative priority. It can contain uncertainty and discovery tasks. Not everything is approved to build.

**Engineering backlog:** Chosen, prioritized delivery work with enough context to act: coherent Epic/Story/Task/Bug, owner of decisions, verifiable completion, important constraints and dependencies. Keep it intentionally small; an initial heuristic is a few planning cycles of plausible upcoming work, never a hard universal quota.

A production incident, critical vulnerability, or contractual obligation may require a fast path. Do not force urgent operational work through long discovery.

## Intake policy

1. Capture problem and evidence, not only a stakeholder's proposed solution.
2. Check whether it duplicates or extends existing entries.
3. If outcome unknown, keep in discovery instead of creating 20 development tickets.
4. Decide if work should be pursued; record reason for accept/defer/decline.
5. When chosen for delivery, create only the near-term detail needed.

## Backlog triage labels (decisions, not mandatory Jira statuses)

- **Active delivery:** selected and relevant for upcoming implementation.
- **Needs discovery:** worthwhile but ambiguous; move to product decision space.
- **Deferred:** known and potentially valuable; no current commitment.
- **Duplicate:** link canonical issue, then close duplicate with rationale.
- **Obsolete / won't do:** close with reason; keep searchable.
- **Special obligation:** retain and review for legal/security/contract needs even when aged.

Age alone never mandates deleting an issue. Never infer 'not important' from inactivity when compliance or customer commitments are involved. Preserve source references and decision rationale. Archive/close in batches only with accountable approval; allow reactivation on new evidence.

## Prioritization

Do not invent a single mathematical score as objective truth. Use customer impact, strategic contribution, frequency, urgency, business/regulatory obligations, effort/risk, and uncertainty. Distinguish severity and delivery priority. Be transparent about missing evidence.

## Suggested simple intake draft

- Reported need / problem:
- Source and evidence:
- Affected role, tenant or integration:
- Existing behavior / known constraints:
- Desired result or hypothesis:
- Related issue / duplicate check:
- Initial disposition: idea, product backlog, delivery, incident/security fast path:
- Open questions / decision owner:

## Anti-patterns

- A ticket for every sentence in a meeting transcript.
- Refining two years of speculative work in detail.
- Keeping rejected requests in the active engineering backlog.
- Making "Ready for development" mean "in a special pseudo-Sprint". This skill does not design sprints; readiness is an attribute of issue quality, not a storage bucket.
