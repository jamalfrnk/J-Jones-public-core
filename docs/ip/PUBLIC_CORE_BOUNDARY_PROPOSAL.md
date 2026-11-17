# Public Core Boundary Proposal

Status: `OWNER APPROVED FOR PLANNING`

Evidence status: `OBSERVED` for current repository paths and `PROPOSED` for
the target repository boundary. No source files are moved by this document.

Related documents:

- [PUBLIC_CORE_MECHANISM_REGISTER.yaml](PUBLIC_CORE_MECHANISM_REGISTER.yaml)
- [PUBLIC_CORE_CLAIM_MODULE_MAP.md](PUBLIC_CORE_CLAIM_MODULE_MAP.md)
- [PUBLIC_CORE_SEAM_PLAN.md](PUBLIC_CORE_SEAM_PLAN.md)
- [PUBLIC_CORE_SCHEMA_SPLIT.md](PUBLIC_CORE_SCHEMA_SPLIT.md)

## 1. Proposed repository relationship

The recommended long-term arrangement is:

```text
J-Jones Public Core repository
  local-first generic infrastructure
  deterministic retrieval
  Strict Clone
  public export interfaces
  public protocols and tests

J-Jones Desktop private repository
  private policy and governance
  canonical proposal and approval
  private identity and modes
  provider disclosure and adapters
  private audit and licensing
  private integrations and release infrastructure
```

The private product may depend on a released public Core package or a reviewed
public Core commit. The public Core must never depend on the private product.

## 2. Proposed public repository contents

```text
public Core package
public domain contracts
public evidence and hashing utilities
public FTS retrieval
public Strict Clone
public export interfaces
public generic backup crypto interface
public public-only settings
public migration history
public contract and security tests
public documentation
public package metadata and CI
```

## 3. Explicitly private repository contents

```text
proposal service and approval workflow
claim authority and epistemic admission
policy engine and policy YAML
private prompts
context compilation and disclosure ledger
authentication fallback and browser boundary
principal, grants, elevation, and mode authority
private ORM and migrations
provider factory, allowlists, credentials, and spend
private backup key resolution and restore
private imports and source consent
MCP, ACP, Claude Code, and multimodal integrations
private tests and fixtures
private packaging, signing, deployment, and licensing
```

## 4. File-level disposition

| Current area | Public disposition | Required action |
|---|---|---|
| `src/jjones/domain` | Selected types only | Create public domain types; exclude authority-bearing models. |
| `src/jjones/memory/notes.py` | Public seam | Split generic parser from private taxonomy and policy. |
| `src/jjones/evidence/hashing.py` | Public candidate | Extract or copy after API and license review. |
| `src/jjones/evidence/manifest.py` | Public seam | Remove private lineage and use public evidence models. |
| `src/jjones/evidence/journal.py` | Public seam | Keep generic journal semantics only. |
| `src/jjones/evidence/capture.py` | Public seam | Replace private policy, audit, retention, and secret dependencies. |
| `src/jjones/retrieval/search.py` | Public seam | Separate FTS from private evidence and canonical ordering. |
| `src/jjones/pipeline/strict_clone.py` | Public candidate | Rebuild against public search and redaction contracts. |
| `src/jjones/providers/base.py` | Public interface | Publish provider-neutral contracts only. |
| `src/jjones/providers/prompt.py` | Public seam | Publish generic fencing, not private prompts or policy. |
| `src/jjones/backup/crypto.py` | Public interface | Separate cryptographic stream format from key and restore policy. |
| `src/jjones/pipeline/okf_*` | Public seam | Rebuild public projection, file safety, and CLI adapters. |
| `src/jjones/pipeline/audio.py` | Public utility subset | Publish media detection only. |
| `src/jjones/config/settings.py` | Public rewrite | Create public settings without private secret/provider loading. |
| `src/jjones/persistence/orm.py` | Private | Do not copy. Create independent public metadata. |
| `src/jjones/persistence/db.py` | Public rewrite | Create independent public engine and migration boundary. |
| `src/jjones/cli/context.py` | Private | Create a separate public composition root. |
| `src/jjones/proposals` | Private | Do not publish implementation. |
| `src/jjones/policies` | Private | Do not publish private policy YAML. |
| `src/jjones/security` | Private except future generic ports | Do not copy authority implementation. |
| `src/jjones/mcp`, `src/jjones/acp` | Deferred/private | Exclude from first public Core. |

## 5. Proposed package dependency rules

Public modules may depend on:

```text
public domain types
standard library
approved public third-party libraries
public persistence models
public protocols
public local adapters
```

Public modules may not depend on:

```text
private policy engine
private proposal service
private mode runtime
private authentication fallback
private principal implementation
private provider factory
private disclosure ledger
private private ORM metadata
private licensing implementation
private J-Jones composition root
```

## 6. Data movement rules

Allowed:

```text
public source -> public derived index
public source -> screened public export
public bundle -> public evidence or draft
private adapter -> public protocol
public Core -> private product through explicit reviewed import
```

Prohibited:

```text
public Core -> private database
public Core -> private proposal approval
public Core -> private disclosure receipts
public Core -> private provider credentials
public Core -> private canonical brain writes
public index -> canonical mutation
public import -> direct private canonical mutation
```

## 7. Recommended first public vertical slice

The first public release should be limited to:

```text
public note parsing
generic evidence hashing
generic manifests and journals
deterministic local FTS
Strict Clone local-only answering
public-only export screening
```

Do not include external provider dispatch, Full AI, vector retrieval, MCP,
ACP, private sessions, or private canonical mutation in the first slice.

## 8. Required approvals before implementation

Owner decisions still required:

```text
public package name
separate public database path
public schema field stability
public migration root
public export format stability
Strict Clone first-release scope
public API and CLI commands
public test and fixture selection
license and packaging boundary
tokenless loopback behavior
```

## 9. Boundary status

```text
PROPOSED_PUBLIC_REPOSITORY: documented
PRIVATE_REPOSITORY_BOUNDARY: documented
SOURCE_MOVES: NOT STARTED
DATABASE_MOVES: NOT STARTED
PACKAGE_SPLIT: NOT STARTED
LICENSE_CHANGE: NOT REQUESTED
PUBLIC_RELEASE: NOT APPROVED
```

The next implementation decision must be a public package and database
boundary approval, not a file move.
