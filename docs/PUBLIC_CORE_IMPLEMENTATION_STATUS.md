# Public Core Implementation Status

Status: RELEASE CANDIDATE IN PROGRESS

Date: 2026-11-17

## Implemented in this alpha

- Generic Markdown front-matter parsing and validation.
- Explicit rejection of secret-prohibited canonical content.
- Provider-neutral request and response data contracts.
- Explicit-authentication gate for transport boundaries.
- Nonce-delimited untrusted-content fencing and fence neutralization.
- Deterministic local evidence hashing and manifest verification.
- Rebuildable SQLite FTS5 local retrieval index.
- Public tests, package metadata, lockfile, CI, dependency audit, and secret scan.

## Not implemented in this alpha

- Private J-Jones policy, identity, entitlement, approval, or governance runtime.
- Provider adapters, provider credentials, disclosure ledgers, or remote inference.
- Private persistence models or migration chain.
- Hosted services, deployment, signing, installers, or commercial licensing.
- Canonical knowledge mutation or an approval workflow.

The alpha is a public implementation slice. Passing local checks does not prove
that a future application integration, packaged artifact, provider, or hosted
deployment is validated.
