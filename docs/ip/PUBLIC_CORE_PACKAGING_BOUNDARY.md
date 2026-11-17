# Public Core Packaging Boundary

Status: `OWNER APPROVED FOR PLANNING`

Evidence status: `REVIEW_REQUIRED`. This document does not change package
metadata, licensing, lockfiles, CI, signing, or release configuration.

## 1. Public package requirements

The public Core needs independent:

```text
package name
versioning
pyproject metadata
dependency set
lockfile policy
test commands
CI workflows
documentation
release artifacts
license declaration
```

The public package must not be created by copying private release metadata and
deleting a few dependencies.

## 2. Public package contents

Candidate public contents:

```text
public domain models and protocols
local evidence utilities
deterministic FTS
Strict Clone
public export interfaces
generic backup crypto interface
public settings
public tests
public documentation
```

## 3. Private package contents

Keep private:

```text
provider adapters
provider credentials and secret providers
private disclosure ledger
proposal and approval services
private policy and prompts
identity, grants, elevation, and modes
private ORM and migrations
private release/signing configuration
private deployment configuration
commercial entitlement and licensing implementation
private integrations
```

## 4. Files requiring review

```text
pyproject.toml
uv.lock
packaging/*
.github/*
scripts/windows/*
release and signing files
installer configuration
```

These files may contain private package names, provider dependencies, release
URLs, signing assumptions, deployment paths, or commercial configuration.

## 5. Dependency policy

Public dependencies must be:

- necessary for public functionality;
- license-compatible with the proposed public license;
- free of private provider or runtime coupling;
- pinned or bounded under a documented policy;
- covered by public security checks.

The public package must not depend on a private package merely to obtain a
helper that can be implemented generically.

## 6. CI boundary

Public CI should run only public checks, including:

```text
format and lint
type checks
public unit and contract tests
public property tests
public database tests
dependency-boundary tests
secret scanning
license/dependency review
packaging smoke test
```

Private CI must remain responsible for:

```text
private policy tests
proposal and approval tests
provider and disclosure tests
private migrations
private release and signing
commercial entitlement
private deployment
```

## 7. Licensing boundary

No license is selected or changed by this planning artifact. Licensing requires
an explicit owner decision and legal review where appropriate.

## 8. Status

```text
PUBLIC_PACKAGING_BOUNDARY: OWNER APPROVED FOR PLANNING
PUBLIC_PACKAGE_METADATA: IMPLEMENTED_ALPHA_UNVALIDATED
PUBLIC_LICENSE_DECISION: APACHE-2.0_APPROVED_BY_OWNER
PUBLIC_CI: IMPLEMENTED
PUBLIC_RELEASE: RELEASE_CANDIDATE_IN_PROGRESS
```
