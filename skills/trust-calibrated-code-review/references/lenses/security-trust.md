# Lens: Security, Auth & Trust Boundaries (`security-trust`)

Trace untrusted data and actor privileges from entry point to sensitive sink. Preserve **blind quarantine** (code and config only). Report only vulnerabilities with a concrete prerequisite, source-to-sink path, and security/privacy impact.

## Inspection protocol

1. **Map trust boundaries**: Locate every changed entry point (HTTP/GraphQL/RPC/webhook/CLI/message consumer/UI binding) and identify what comes from an untrusted caller versus verified server context.
2. **Trace guards & sinks**: Follow authorization checks, tenant/owner scoping, and data sanitization all the way to persistence, execution, outbound network, or response serialization.

## Hunting vectors

- **Broken access control & IDOR / BOLA**: Endpoints, commands, or queries checking authentication ("is signed in") while omitting role/permission checks, object ownership, or tenant scoping; trusting client-supplied `userId`/`tenantId`/`orgId`/`role` fields instead of authenticated principal context; mass assignment / over-posting into privileged fields.
- **Injection & unsafe interpretation**: Raw SQL concatenation or unvalidated sort/column identifiers, command/shell execution, path traversal or archive extraction outside base directories, SSRF via user-influenced URLs/webhooks, template/HTML/DOM XSS (`innerHTML`, `bypassSecurityTrust*`, `dangerouslySetInnerHTML`), unsafe deserialization, and catastrophic regex backtracking (ReDoS).
- **Secrets, PII/PHI & observability exposure**: Tokens, credentials, connection strings, personal/health data, or raw request payloads leaked into logs, exception messages, problem-details responses, telemetry spans, analytics, client bundles, or committed fixtures.
- **Session, CORS, CSRF, crypto & fail-open paths**: Wildcard/reflected CORS with credentials, state-changing routes missing CSRF/origin checks, weak randomness/hashing, JWT/signature validation shortcuts, and catch/fallback blocks that default to `allow` on failure.

**Done when**: Every changed entry point, authorization guard, external input parser, and sensitive sink in the matched scope has been traced from untrusted source to enforcement boundary and output sink.
