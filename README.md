# Agent Skills

A collection of agent skills for AI coding agents, covering bug fixing, refactoring, code review, planning, and presentations. Works with Pi, GitHub Copilot, and other agents that support the [Agent Skills](https://agentskills.io/) format.

## Skills

- **bugfix** : Investigates and fixes a bug, regression, or crash with evidence and regression checks.
- **grilling** : Stress-tests a plan, decision, or idea by interviewing you until you share an understanding.
- **i-have-adhd** : Shapes output for readers with ADHD: next action first, numbered steps, visible wins. User-invoked.
- **keynote-storytelling** : Builds or reviews presentations and slides around one message per slide and a 5-second test.
- **monte-carlo-forecasting** : Probabilistic delivery forecasts (P50/P85/P95) from historical throughput and cycle time.
- **prototype** : Builds a throwaway prototype to answer a design question.
- **refactoring** : Plans and executes structural changes that preserve observable behavior.
- **retro** : Runs a retrospective on a coding session. User-invoked.
- **tornado** : Strategic programming: deep modules, information hiding, and preparatory refactoring.
- **tracer-bullet-slicing** : Slices a feature into blocker tickets, one tracer bullet, and vertical slices. User-invoked.
- **trust-calibrated-code-review** : Risk-calibrated, three-level code review with a coverage ledger and evidence-graded findings. User-invoked.
- **writing-for-agents** : Guidance for writing skills, `AGENTS.md`, and `CLAUDE.md` files.

## Install

```bash
npx skills add 4typen/skills -g
```

The CLI lists the skills and lets you pick them. `-g` installs them for all projects.

## Update

```bash
npx skills update -g
```

## License

MIT. See [LICENSE](LICENSE).
