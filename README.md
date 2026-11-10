# Agent Skills

My personal collection of reusable AI coding agent skills.

This repository is the central source of truth for skills used across different projects, machines, and coding agents.

Skills follow the [Agent Skills specification](https://agentskills.io/) and are managed with the [Skills CLI](https://skills.sh/).

## Supported Agents

The skills are designed to be reusable across coding agents, including:

- **GitHub Copilot**
- **Pi Coding Agent**
- Other agents compatible with the Agent Skills specification

Agent-specific extensions and configurations are maintained separately.

For Pi-specific extensions, prompts, and themes, see the separate `pi-toolkit` repository.

## Repository Structure

```text
skills/
├── skills/
│   ├── code-review/
│   │   └── SKILL.md
│   ├── refactoring/
│   │   └── SKILL.md
│   └── test-generator/
│       └── SKILL.md
└── README.md
```

Each directory inside `skills/` contains one independent skill.

A skill must include a `SKILL.md` file and can optionally contain supporting scripts, references, or templates.

## Prerequisites

- macOS
- Git
- Node.js 22.20 or newer
- GitHub access (SSH or HTTPS authentication)
- At least one compatible coding agent

Verify the required tools:

```bash
git --version
node --version
npx --version
```

The Skills CLI runs through `npx` and does not require a separate global installation.

## Installation

### Install skills globally

Install skills from this repository:

```bash
npx skills add 4typen/skills -g
```


The CLI discovers the available skills and lets you select which skills and supported agents to install.

The `-g` flag installs skills at user level, making them available across projects.

### Install from a private repository

For private GitHub repositories, SSH authentication is recommended:

```bash
npx skills add \
  git@github.com:4typen/skills.git -g
```

Ensure that your SSH key has access to the repository.

Verify GitHub authentication:

```bash
ssh -T git@github.com
```

The Skills CLI can also use configured Git or GitHub CLI credentials.

### Install all skills

To install every skill globally for all supported agents:

```bash
npx skills add 4typen/skills \
  --all -g
```

This skips interactive selection and targets all supported agents.

For a more controlled installation, use the interactive command without `--all`.

### Install selected skills

Install specific skills by name:

```bash
npx skills add 4typen/skills \
  --skill code-review \
  --skill refactoring \
  -g
```

### List available skills

Inspect the repository before installing:

```bash
npx skills add 4typen/skills --list
```

## Managing Skills

### List installed skills

Show globally installed skills:

```bash
npx skills list -g
```

### Check for updates

Check whether installed skills have updates:

```bash
npx skills check
```

### Update skills

Update globally installed skills:

```bash
npx skills update -g
```

Update one specific skill:

```bash
npx skills update code-review -g
```

Updates are retrieved from the configured skill source.

**Note:** GitHub changes are not synchronized automatically. Run the update command after pushing changes to the repository.

### Remove a skill

Remove an installed global skill:

```bash
npx skills remove code-review -g
```

## Creating New Skills

Skills are defined using a `SKILL.md` file.

### Create a skill

From the repository root:

```bash
npx skills init skills/my-new-skill
```

Alternatively, create the directory and file manually.

### Skill format

Example `skills/code-review/SKILL.md`:

```markdown
---
name: code-review
description: Review code for quality, readability, and maintainability.
---

# Code Review

Review the provided code.

## Instructions

1. Identify potential bugs.
2. Check readability and maintainability.
3. Identify unnecessary complexity.
4. Suggest concrete improvements.
5. Explain relevant trade-offs.

## Output

Provide findings ordered by severity.

Include actionable recommendations.
```

### Skill guidelines

Each skill should:

- Have a unique, descriptive name.
- Describe when the agent should use it.
- Focus on a clear task or workflow.
- Provide concise, actionable instructions.
- Avoid unnecessary dependencies.
- Remain independent of a specific project whenever possible.
- Follow the Agent Skills specification.

Use supporting files when instructions become too large for one `SKILL.md`.

## Development Workflow

Skills are maintained in this Git repository.

### 1. Clone the repository

```bash
git clone \
  git@github.com:4typen/skills.git

cd skills
```

### 2. Add or modify a skill

Edit an existing `SKILL.md` or create a new skill directory.

### 3. Test locally

Install a skill from the local repository:

```bash
npx skills add . \
  --skill my-new-skill \
  -g
```

Test the skill with the intended coding agent.

### 4. Commit and push

```bash
git add skills/
git diff --cached
git commit -m "feat: add new skill"
git push
```

### 5. Update other machines

On another machine:

```bash
npx skills update -g
```

Existing installed skills can be updated through the CLI.

For newly added skills, run `npx skills add` again to discover and install them.

## Using Multiple Machines

The repository is the central source of truth.

Each machine maintains its own installed skills.

```text
                 GitHub
              skills
                   |
          +--------+--------+
          |                 |
       MacBook A         MacBook B
          |                 |
      npx skills        npx skills
          |                 |
     Global Skills     Global Skills
          |                 |
     Pi / Copilot      Pi / Copilot
```

### Initial setup

Run once on each machine:

```bash
npx skills add \
  git@github.com:4typen/skills.git -g
```

### Regular updates

```bash
npx skills check
npx skills update -g
```

No manual file copying is required.

## Separation of Skills and Pi Extensions

This repository contains only reusable agent skills.

Pi-specific functionality is managed through a separate repository.

| Repository | Purpose | Installation |
|---|---|---|
| `skills` | Cross-agent skills | `npx skills add` |
| `pi-toolkit` | Pi extensions, prompts, themes | `pi install` |

This separation keeps reusable skills independent from agent-specific implementations.

Pi extensions should not be stored here unless they are converted into standard Agent Skills.

## Security and Privacy

This repository is intended for personal, reusable skills.

**Do not commit:**

- Company-confidential instructions or documents.
- Proprietary source code.
- Internal API specifications.
- Credentials, API keys, or tokens.
- Customer or employee data.
- Internal infrastructure details.
- Machine-specific secrets.

### Personal and work environments

Generic personal skills can be reused across environments only when permitted by the applicable company policies.

Company-specific skills should remain in separate, approved repositories.

Never copy confidential company information into this personal repository.

Review changes before committing:

```bash
git diff --cached
```

A private GitHub repository limits visibility but does not replace proper data classification and access controls.

### Third-party skill execution

Skills and supporting scripts can influence agent behavior or execute code.

Review skills before installation, especially when they come from external repositories.

Only install skills from trusted sources.

## Migration from Manual Symlinks

Earlier setups may use a direct symlink from `~/.agents/skills` to a local Git clone.

When switching to the Skills CLI:

1. Inspect the existing skill directory.
2. Back up locally maintained skills.
3. Remove or migrate the old symlink after verifying its contents.
4. Install skills through `npx skills add`.
5. Use `npx skills update` for subsequent updates.

Do not maintain both installation methods for the same skill directory.

The Skills CLI manages installation paths and symlinks for supported agents.

## Useful Commands

| Action | Command |
|---|---|
| Install globally | `npx skills add 4typen/skills -g` |
| List repository skills | `npx skills add 4typen/skills --list` |
| Install all skills | `npx skills add 4typen/skills --all -g` |
| List installed skills | `npx skills list -g` |
| Check updates | `npx skills check` |
| Update global skills | `npx skills update -g` |
| Remove a skill | `npx skills remove SKILL_NAME -g` |
| Create a skill | `npx skills init skills/SKILL_NAME` |

## References

- [Agent Skills Specification](https://agentskills.io/)
- [Skills CLI](https://skills.sh/)
- [Skills CLI GitHub Repository](https://github.com/vercel-labs/skills)
- [Skills CLI Reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).
