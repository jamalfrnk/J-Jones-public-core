# Public Core Documentation Map

Status: `OWNER APPROVED FOR PLANNING`

Evidence status: `REVIEW_REQUIRED`. Existing documentation must be classified
before it is copied into a public repository.

## 1. Public documentation to create or rewrite

```text
PUBLIC_CORE_README.md
PUBLIC_CORE_ARCHITECTURE.md
PUBLIC_CORE_SECURITY_BOUNDARY.md
PUBLIC_CORE_DATA_MODEL.md
PUBLIC_CORE_PROVIDER_INTERFACE.md
PUBLIC_CORE_BUILD.md
PUBLIC_CORE_LIMITATIONS.md
PUBLIC_CORE_CONTRIBUTING.md
```

These documents should describe the public Core only.

## 2. Public topics allowed

```text
local-first operation
public note format
generic evidence capture
hashes and manifests
rebuildable indexes
Strict Clone local-only behavior
public export screening
provider-neutral interfaces
public database and migrations
public security limitations
public test and build commands
```

## 3. Topics that require private rewrite or exclusion

```text
private proposal approval sequence
private claim authority rules
private disclosure ledger details
private provider allowlists
private mode and entitlement semantics
private authentication fallback
private database table relationships
private prompts and policy YAML
private MCP and ACP behavior
private Claude Code ingestion
private release, signing, and deployment
patent strategy or claim language
```

## 4. Existing documents requiring review

```text
ARCHITECTURE.md
THREAT_MODEL.md
TEST_STRATEGY.md
AUTONOMY_POLICY.md
VISION.md
docs/**
README files
examples/**
```

No existing document should be copied into the public repository solely
because it is documentation.

## 5. Documentation claims policy

Public documentation must distinguish:

```text
implemented
tested
validated
not tested
not proven
planned
deferred
```

It must not claim:

```text
patentability
legal novelty
production readiness
provider zero retention without evidence
local-only behavior when remote inference is possible
canonical truth for derived indexes
```

## 6. Status

```text
PUBLIC_DOCUMENTATION_MAP: IMPLEMENTED / UNVALIDATED
PUBLIC_DOCUMENTATION: IMPLEMENTED_ALPHA_UNVALIDATED
PRIVATE_DOCUMENTATION_AUDIT: NOT STARTED
PUBLIC_RELEASE: RELEASE_CANDIDATE_IN_PROGRESS
```
