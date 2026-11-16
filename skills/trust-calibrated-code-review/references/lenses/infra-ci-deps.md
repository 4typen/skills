# Lens: Infrastructure, CI/CD & Dependencies (`infra-ci-deps`)

Evaluate changed workflows, manifests, containers, and IaC against clean CI runners, supply-chain attacks, and live production rollouts. Preserve **blind quarantine**.

## Inspection protocol

1. **Trace build-to-deploy pipeline**: Follow changed workflow triggers, permissions, secrets, package manifests/lockfiles, container stages, and IaC resources from PR check through production rollout and rollback.
2. **Verify cross-file config parity**: Cross-check every added/renamed script, environment variable, secret, port, path filter, or package version across manifests, CI YAML, Docker/IaC, and application readers.

## Hunting vectors

- **CI/CD security & silent green builds**: Untrusted GitHub/PR metadata (`${{ github.event.pull_request.title }}`, branch names, commit bodies) interpolated directly into shell `run:` blocks instead of `env:` variables; `pull_request_target` checking out untrusted PR heads with write tokens or secrets; over-scoped `permissions:`; unpinned third-party actions/containers; `|| true`, missing `set -euo pipefail`, or narrow path filters causing failing or new projects/tests to be skipped silently.
- **Dependency & lockfile drift**: Package manifests edited without matching lockfile updates, major/breaking transitive upgrades, runtime vs `devDependencies`/`PrivateAssets` misplacement shipping test/build bloat into production, target-framework/engine version mismatches, or newly introduced deprecated/vulnerable packages.
- **Container, IaC & runtime config hazards**: Environment variable or secret names mismatched between app config and Helm/Terraform/Compose/CI; unsafe production defaults when an env var is unset (debug enabled, auth disabled, localhost URLs); Dockerfiles running as `root`, leaking build secrets into layers, or busting dependency cache layers on every code edit; Terraform/cloud changes triggering destructive resource replacement (stateful DB/storage/queue recreation) instead of in-place update.

**Done when**: Every changed CI workflow, manifest/lockfile pair, container definition, IaC resource, and runtime config key has been checked for injection/permission safety, silent check bypasses, lockfile parity, and rollout destructiveness.
