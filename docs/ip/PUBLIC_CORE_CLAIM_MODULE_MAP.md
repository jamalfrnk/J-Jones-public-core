# Public Core Claim Module Map

Status: `OWNER APPROVED FOR PLANNING`

Evidence status: `OBSERVED` from current repository source inspection. This
document is not a patent claim chart, legal opinion, or release approval.

The purpose of this map is to identify which current J-Jones Desktop modules
could contribute to a public Core, which modules require a new public seam, and
which modules must remain private or deferred.

The public Core is not created by copying the current repository and deleting a
few private directories. The public Core needs its own composition root,
dependency direction, database boundary, migration chain, tests, packaging,
and documentation.

Related register:

- [PUBLIC_CORE_MECHANISM_REGISTER.yaml](PUBLIC_CORE_MECHANISM_REGISTER.yaml)

## Boundary rule

The public Core may expose generic interfaces and local-first behavior. It may
not expose the private J-Jones implementation of:

- canonical proposal approval;
- model-derived claim admission;
- provider disclosure and context transformation;
- authentication fallback and mode authority;
- private evidence-to-canonical lineage;
- private governance tables and migrations;
- provider adapters and commercial provider configuration;
- private prompts and policy YAML;
- private MCP, ACP, Claude Code, or multimodal behavior;
- private release, signing, deployment, or licensing behavior.

The desired dependency direction is:

```text
public interfaces and local data types
                    |
                    v
public local implementations and derived indexes
                    |
                    v
public Core composition root
```

Private J-Jones services may implement a public protocol, but public modules
must not import the private composition root, private policy engine, private
provider factory, private ORM schema, or private authority services.

## Classification vocabulary

| Treatment | Meaning |
|---|---|
| `include_candidate` | Candidate for direct public implementation after normal review. |
| `generic_interface` | The public interface may be released, but the current implementation must be split, reduced, or replaced. |
| `review_required` | The boundary is not proven and must not be treated as public. |
| `exclude_from_public_core` | Keep private or remove from the public release. |
| `deferred` | Not required for the first public Core. |

## Module classification matrix

| Register ID | Current module | Main symbols | Treatment | Boundary action |
|---|---|---|---|---|
| PCM-001 | `src/jjones/memory/notes.py` | `parse_front_matter`, `render_note`, `validate_note_metadata`, `validate_note_file` | `generic_interface` | Extract a generic note schema layer. Keep J-Jones taxonomy, authority, and sensitivity rules private. |
| PCM-002 | `src/jjones/providers/prompt.py` | `UntrustedContent`, `build_prompt`, `build_image_prompt` | `generic_interface` | Define a public fencing contract. Remove private policy-engine calls and private prompt wording. |
| PCM-003 | `src/jjones/providers/base.py` | `ProviderImage`, `ProviderRequest`, `ProviderResponse`, `ModelProvider` | `generic_interface` | Strongest provider seam candidate. Keep adapters, routing, credentials, and disclosure policy private. |
| PCM-004 | `src/jjones/evidence/capture.py` | `CaptureService`, `capture_file`, `capture_bytes`, `capture_text` | `generic_interface` | Split generic capture from policy, audit, retention, secret, and private path services. |
| PCM-005 | `src/jjones/evidence/hashing.py` | `hash_bytes`, `hash_file` | `include_candidate` | Likely portable with ordinary API and security review. |
| PCM-006 | `src/jjones/evidence/manifest.py`, `verify.py` | `write_manifest`, `read_manifest`, `verify_all`, `IntegrityReport` | `generic_interface` | Keep generic manifest verification; separate J-Jones evidence lineage and reconciliation consequences. |
| PCM-007 | `src/jjones/evidence/journal.py` | `JournalEntry`, `write_entry`, `clear_entry`, `read_entry` | `generic_interface` | Extract bounded journal and atomic-write contracts. |
| PCM-008 | `src/jjones/persistence/db.py` | `create_sqlite_engine`, `session_scope`, `run_migrations` | `generic_interface` | Create a public persistence module; do not reuse private ORM metadata or migration history. |
| PCM-009 | `src/jjones/retrieval/search.py` | `SearchResult`, `rebuild_index`, `sync_index`, `search` | `include_candidate` | Split generic lexical search from private evidence resolution, supersession ordering, and knowledge regions. |
| PCM-010 | `src/jjones/retrieval/search.py` | `_derived_state_ready`, `_reindex_candidates`, `rebuild_index` | `generic_interface` | Preserve rebuildability and source-authoritative behavior in the public index. |
| PCM-011 | `src/jjones/pipeline/strict_clone.py` | `StrictCloneAnswer`, `answer_from_local_evidence` | `include_candidate` | Rebuild against public search/result contracts; no private mode or provider composition. |
| PCM-012 | `src/jjones/backup/crypto.py` | `ArtifactHeader`, `EncryptingWriter`, `DecryptingReader` | `generic_interface` | Separate cryptographic streaming format from private key resolution, workspace scope, and restore. |
| PCM-013 | `src/jjones/pipeline/okf_export_content.py` | `screen_text`, `public_note`, `prepare_documents`, `archive_documents` | `generic_interface` | Create a public projection contract; keep private canonical fields and receipt behavior out. |
| PCM-014 | `src/jjones/pipeline/okf_export_files.py` | `no_links`, `read_local_file`, `destination`, `publish` | `generic_interface` | Extract generic safe-file access; configure public roots independently. |
| PCM-015 | `src/jjones/pipeline/okf_export.py` | `ExportPreview`, `ExportResult`, `OkfExportService` | `generic_interface` | Keep a public export contract but remove private principal, presence, receipt, and composition dependencies. |
| PCM-016 | `src/jjones/cli/okf_*.py` | `export_okf`, `import_okf`, `import_okf_bundle` | `generic_interface` | Rebuild as thin public adapters over public services. |
| PCM-017 | `src/jjones/pipeline/audio.py` | `audio_suffixes`, `is_audio`, `media_type_for` | `generic_interface` | Portable media detection only. Exclude sensitivity and transcription policy. |
| PCM-018 | `src/jjones/config/settings.py` | `Settings`, public settings models, `safe_summary` | `generic_interface` | Create standalone public settings; do not reuse private provider, secret, approval, or installation loading. |
| PCM-019 | `docs/ip/PUBLIC_CORE_MECHANISM_REGISTER.yaml` | register and public boundary metadata | `include_candidate` | Keep public documentation separate from private architecture and patent material. |

## Import findings and required seams

### 1. Modules close to public-ready

These modules have relatively narrow dependencies and are the best starting
points for a public implementation:

```text
src/jjones/evidence/hashing.py
src/jjones/backup/crypto.py
src/jjones/pipeline/audio.py
src/jjones/providers/base.py
```

They still require ordinary API, dependency, security, and license review.
`backup/crypto.py` requires additional cryptographic review before being
released as a supported public feature.

### 2. Modules that require a public seam

These current modules contain useful public behavior but also import private
services or private policy:

```text
src/jjones/evidence/capture.py
src/jjones/evidence/manifest.py
src/jjones/evidence/verify.py
src/jjones/evidence/journal.py
src/jjones/retrieval/search.py
src/jjones/pipeline/strict_clone.py
src/jjones/pipeline/okf_export_content.py
src/jjones/pipeline/okf_export_files.py
src/jjones/pipeline/okf_export.py
src/jjones/config/settings.py
```

They must not be copied unchanged into a public repository.

### 3. Private dependencies observed in public candidates

The current implementation has these private or review-sensitive imports:

| Public candidate | Current private dependency | Required public action |
|---|---|---|
| `evidence/capture.py` | `policies.engine`, `observability.audit`, `observability.metrics`, `retention.tombstones`, `security.paths`, `security.secrets` | Define public capture ports and move policy, audit, retention, and secret behavior behind private adapters. |
| `providers/prompt.py` | `policies.engine`, `domain.ids` | Define a public fencing function that does not import the private policy engine. |
| `persistence/db.py` | `persistence.orm`, private migration paths | Create a public ORM metadata root and independent migration chain. |
| `retrieval/search.py` | `memory.notes`, private logging, evidence resolution in the same module | Split lexical indexing from private provenance and canonical ordering. |
| `pipeline/strict_clone.py` | `domain.modes`, retrieval-specific restricted placeholder | Define a public local-answer contract and public redaction policy. |
| `pipeline/okf_export_content.py` | `domain.models`, `memory.notes`, `pipeline.okf`, `okf_projection`, `security.secrets` | Create a public projection model and public screening contract. |
| `pipeline/okf_export_files.py` | `pipeline.okf`, `security.paths` | Extract generic safe-file operations and public root configuration. |
| `pipeline/okf_export.py` | `security.presence`, `security.principal`, `persistence.okf_export_receipts` | Define public confirmation and receipt ports; keep J-Jones identity and receipt persistence private. |
| `config/settings.py` | `installation`, `paths`, `security.secret_provider`, provider settings | Create standalone public settings and secret-free configuration loading. |
| `cli/okf_*.py` | `cli.context`, private principal/presence, private database session | Rebuild as thin public adapters over public services. |

## Proposed public package shape

This is a proposed target, not an implementation instruction yet:

```text
public-core/
├── pyproject.toml
├── docs/
│   └── public-core/
├── migrations/
│   └── public-core history only
├── src/
│   └── jjones_core/
│       ├── domain/
│       │   ├── clock.py
│       │   ├── errors.py
│       │   ├── ids.py
│       │   ├── notes.py
│       │   ├── evidence.py
│       │   └── retrieval.py
│       ├── evidence/
│       │   ├── capture.py
│       │   ├── hashing.py
│       │   ├── manifest.py
│       │   └── journal.py
│       ├── retrieval/
│       │   ├── search.py
│       │   └── strict_clone.py
│       ├── providers/
│       │   ├── base.py
│       │   └── prompt_fencing.py
│       ├── export/
│       │   ├── content.py
│       │   ├── files.py
│       │   └── service.py
│       ├── backup/
│       │   └── crypto.py
│       ├── persistence/
│       │   ├── db.py
│       │   └── models.py
│       ├── config/
│       │   └── settings.py
│       └── runtime/
│           └── public_core.py
└── tests/
    ├── contract/
    ├── unit/
    ├── property/
    └── integration/
```

The package name is provisional. Do not rename the current package or create
this layout until the seam and schema documents are approved.

## Proposed dependency direction

```text
jjones_core.domain
        |
        +--> jjones_core.evidence
        +--> jjones_core.retrieval
        +--> jjones_core.export
        +--> jjones_core.backup
        +--> jjones_core.persistence
        +--> jjones_core.providers.base
        |
        v
jjones_core.runtime.public_core
```

The following imports are prohibited in public Core modules:

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
private MCP or ACP runtime
private J-Jones composition root
```

The public Core may define protocols that private J-Jones services implement,
but the dependency must point from the private adapter toward the public
protocol, not from public code into private code.

## Public data and state boundaries

### Public candidate state

Potentially public after schema review:

```text
public note metadata
public local evidence metadata
content hashes
generic manifests
generic journal entries
rebuildable FTS state
public export projections
public-format import previews
generic backup artifact metadata
```

### Private state that must not be imported into the public Core

```text
proposal approval state
canonical-write state
disclosure receipts
provider configuration
provider spend
recipient grants
owner sessions
mode sessions
passkey and elevation state
private audit events
private import consent state
private source-to-claim lineage
private migration history
private licensing and entitlement state
```

### Derived-state rule

Public indexes, caches, and search tables must be rebuildable from public
source data. They must not become an alternate canonical store.

```text
public source data
        |
        v
rebuildable public index
        |
        v
public local retrieval
```

The reverse direction is prohibited:

```text
index row
    -X->
canonical truth
```

## Inheritance and composition boundary

The public Core should prefer composition and protocols over inheriting from
private services.

Permitted public inheritance candidates:

```text
generic dataclasses
generic Pydantic or validation models
generic public exceptions
generic protocol implementations
```

Prohibited public inheritance patterns:

```text
public class inheriting from ProposalService
public class inheriting from ModeSessionService
public class inheriting from private AskExecutionService
public provider adapter inheriting from a private provider implementation
public ORM model inheriting from the private ORM metadata root
```

If a public class currently depends on a private base class, create a public
protocol or public base contract and make the private implementation an adapter.

## Test boundary map

### Likely public test candidates

```text
generic hashing tests
generic note-parser tests
generic manifest and journal tests
deterministic FTS rebuild tests
Strict Clone local-only tests
public export screening tests
public path-safety tests
public provider-port contract tests
```

### Private tests that must not be copied into public Core unchanged

```text
proposal approval tests
disclosure ledger tests
provider egress tests
mode authority tests
passkey and elevation tests
private migration tests
private prompt and extraction tests
private canonical-lineage tests
private MCP and ACP tests
private Claude Code session tests
private release and signing tests
```

The exact test-file map remains `REVIEW_REQUIRED` until the public test and
fixture pass is completed.

## Required next decisions

Before moving code, resolve these questions in order:

1. Does the public Core use a new package name or remain a subpackage during
   the transition?
2. Does the public Core receive a separate SQLite database and migration
   history?
3. Which public note and evidence fields are stable enough to publish?
4. Which export format becomes a supported public contract?
5. Is Strict Clone the first supported public runtime path?
6. Which generic provider interfaces are public without enabling disclosure?
7. Which API and CLI commands are public read-only commands?
8. Which tests and fixtures can be published without revealing private policy?
9. Which documentation must be rewritten instead of copied?
10. Which packaging and licensing decisions require owner approval?

## Current stop gate

```text
PUBLIC_CORE_CLAIM_MODULE_MAP: IMPLEMENTED / UNVALIDATED
SOURCE_CODE_SPLIT: NOT STARTED
DATABASE_SPLIT: NOT STARTED
PUBLIC_MIGRATION_CHAIN: NOT STARTED
PUBLIC_TEST_SPLIT: NOT STARTED
PUBLIC_RELEASE: NOT APPROVED
```

The next artifact should be:

```text
docs/ip/PUBLIC_CORE_SEAM_PLAN.md
```

That document should define the exact public protocols, private adapters,
dependency direction, and forbidden imports before any source files are moved
or copied.
