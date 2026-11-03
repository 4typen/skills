# AI-assisted Jira work

## Good AI uses

- Extract underlying customer problems from feedback; summarize sources without losing provenance.
- Find candidate duplicates and existing Epics; mark uncertainty until confirmed.
- Suggest type and scope; identify structural anti-patterns.
- Improve measurable, testable acceptance criteria and relevant edge cases.
- Draft vertical Story splits and flag dependencies.
- Compare Jira requirements to linked architecture/coding/security standards.
- Review missing error handling, tenancy isolation, permissions, migrations, backward compatibility, logs and tests when applicable.
- Summarize post-delivery customer outcome evidence separately from delivery status.

## Unsafe or wasteful patterns

- Turning each meeting note into a ticket or each Story into ten AI-authored subtasks.
- Automatically generating Jira edits or assigning priority based on weak inferred urgency.
- Hallucinating an API, customer problem, technical constraint, or test result.
- Assuming the model has searched Jira, read an internal document, run tests or deployed without tool evidence.
- Sending production customer data, secrets, access tokens, employee information or restricted artifacts to an unapproved system.
- Granting an agent unrestricted mutation rights without human review, auditability and minimal permissions.

## Controls

1. Jira is the source of the **agreed work intent and completion criteria**, not a complete repository of internal implementation steps.
2. Link authoritative architecture, security, API contracts, designs and decisions; don't duplicate their full contents into dozens of tickets.
3. Separate `known fact`, `assumption`, `proposal`, and `needs decision` in generated drafts.
4. Cite exact issue keys and accessible source references when available.
5. For writes, show a proposed diff/change map and ask approval; validate result after execution. Follow the platform's permission model and audit trail.
6. Human owners approve scope, priority, security-sensitive changes and completion claims. AI is a reviewer/assistant, not autonomous product authority.
7. Evaluate success through flow quality, reduced rework, defects and customer outcomes, not ticket volume or lines of code.

## Prompt pattern for the AI agent

"Review this requirement as a SaaS Jira artifact. Find the user/system problem, proposed behavior, necessary constraints and open decisions. Check for duplicates if you have Jira access. Recommend Idea/Opportunity, Epic, Story, Task, Bug, or Spike, with reasons. Produce the smallest necessary Jira draft with verifiable completion criteria. Do not create speculative child tickets, do not claim tests or changes were made, and mark unknown information explicitly."
