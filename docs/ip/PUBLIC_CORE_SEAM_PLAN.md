# Public Core Seam Plan

Status: `OWNER APPROVED FOR PLANNING`

Evidence status: `OBSERVED` from current source inspection plus `PROPOSED`
public interfaces. Proposed interfaces in this document do not exist yet and
must not be treated as implemented.

This document defines how a future public J-Jones Core can coexist with the
private J-Jones Desktop product without importing private governance,
provider, licensing, identity, disclosure, or canonical-mutation behavior.

Related documents:

- [PUBLIC_CORE_MECHANISM_REGISTER.yaml](PUBLIC_CORE_MECHANISM_REGISTER.yaml)
- [PUBLIC_CORE_CLAIM_MODULE_MAP.md](PUBLIC_CORE_CLAIM_MODULE_MAP.md)

## 1. Objective

The public Core should provide a useful local-first foundation containing:

- local note and evidence structures;
- deterministic local retrieval;
- rebuildable derived indexes;
- local-only Strict Clone behavior;
- generic provider-neutral interfaces;
- generic file, hash, manifest, journal, and transaction utilities;
- screened public export interfaces;
- public documentation and public contract tests.

The public Core must not provide the private implementation of:

- canonical proposal approval;
- model-derived claim admission;
- policy-controlled canonical mutation;
- private provider disclosure and context transformation;
- authentication fallback and mode authority;
- private evidence-to-canonical lineage;
- private ORM governance schema;
- private provider adapters or commercial configuration;
- private prompts and policy YAML;
- private MCP, ACP, Claude Code, or multimodal behavior;
- private licensing, release, signing, or deployment behavior.

## 2. Proposed architecture

The intended relationship is:

```text
                    PUBLIC CORE

 public domain contracts and data types
                 |
                 v
 public ports and protocols
                 |
       +---------+----------+
       |                    |
       v                    v
 public local         public derived
 implementations     indexes and views
       |                    |
       +---------+----------+
                 v
       public Core runtime

                    PRIVATE J-JONES

 private policy, authority, provider, disclosure, proposal, audit,
 licensing, identity, and canonical-mutation services
                 |
                 v
 private adapters may implement public protocols
```

The dependency arrow must point toward public contracts:

```text
private adapter -> public protocol
```

It must not point from public Core code into private implementation modules:

```text
public Core module -X-> private policy or runtime implementation
```

## 3. Proposed public protocols

The names below are proposed design names. They are not current repository
symbols and are not implemented by this document.

### 3.1 Clock and identifier ports

```python
class Clock(Protocol):
    def now(self) -> datetime: ...


class IdFactory(Protocol):
    def new_id(self) -> str: ...
```

Purpose:

- deterministic tests;
- no hidden time source;
- no hidden random identifier source;
- replaceable public implementation.

Private J-Jones services may adapt their existing clock and ID services to
these ports. The public Core must not depend on private runtime identity or
correlation behavior.

### 3.2 Note document port

```python
class NoteDocumentPort(Protocol):
    def parse(self, text: str) -> NoteDocument: ...
    def render(self, document: NoteDocument) -> str: ...
    def validate(self, document: NoteDocument) -> tuple[ValidationIssue, ...]: ...
```

Public responsibility:

- parse bounded front matter;
- render generic notes;
- validate generic structural fields.

Private exclusions:

- J-Jones claim authority;
- private note taxonomy;
- private sensitivity policy;
- canonical admission;
- proposal state;
- private review thresholds.

Current source candidate:

```text
src/jjones/memory/notes.py
```

Required action: split generic parsing and validation from J-Jones-specific
rules. Do not copy the current module unchanged if its global note rules are
private.

### 3.3 Evidence capture port

```python
class EvidenceCapturePort(Protocol):
    def capture_file(self, path: Path, request: CaptureRequest) -> EvidenceRecord: ...
    def capture_bytes(self, data: bytes, request: CaptureRequest) -> EvidenceRecord: ...
    def capture_text(self, text: str, request: CaptureRequest) -> EvidenceRecord: ...
```

Public responsibility:

- bounded input capture;
- content hashing;
- generic manifest creation;
- journaled persistence;
- duplicate detection through a public repository port.

Private exclusions:

- J-Jones secret policy;
- private quarantine rules;
- private retention tombstones;
- private audit implementation;
- private provider disclosure;
- evidence-to-claim admission.

Current source candidate:

```text
src/jjones/evidence/capture.py
```

Observed current private imports that must be removed from a public
implementation include policy, audit, metrics, retention, path-security, and
secret-provider modules.

### 3.4 Hash, manifest, and journal ports

```python
class ContentHasher(Protocol):
    def hash_bytes(self, data: bytes) -> str: ...
    def hash_file(self, path: Path) -> str: ...


class ManifestStore(Protocol):
    def write(self, record: EvidenceRecord) -> Path: ...
    def read(self, path: Path) -> EvidenceRecord: ...
    def list(self) -> Sequence[Path]: ...


class JournalStore(Protocol):
    def begin(self, record: EvidenceRecord, started_at: datetime) -> Path: ...
    def clear(self, evidence_id: str) -> None: ...
    def unreadable(self) -> Sequence[Path]: ...
```

Current source candidates:

```text
src/jjones/evidence/hashing.py
src/jjones/evidence/manifest.py
src/jjones/evidence/journal.py
src/jjones/evidence/verify.py
```

These are among the cleanest public seams. They must remain generic and must
not embed J-Jones-specific canonical, claim, provider, or audit assumptions.

### 3.5 Search and derived-index ports

```python
class SearchIndexPort(Protocol):
    def rebuild(self, source_root: Path) -> int: ...
    def sync(self, source_root: Path) -> SyncReport: ...
    def search(self, query: str, options: SearchOptions) -> Sequence[SearchResult]: ...
```

Public guarantees:

- the index is derived;
- the index is rebuildable;
- source data remains authoritative;
- index corruption does not mutate source data;
- results do not grant canonical-write authority.

Private exclusions:

- J-Jones evidence resolution;
- private sensitivity filtering;
- private knowledge-region semantics;
- private supersession ordering;
- private provider context selection.

Current source candidate:

```text
src/jjones/retrieval/search.py
```

The current module combines generic FTS behavior with private provenance and
canonical-ordering behavior. It requires a split or carefully isolated public
implementation.

### 3.6 Local-answer port

```python
class LocalAnswerPort(Protocol):
    def answer(self, question: str, results: Sequence[SearchResult]) -> LocalAnswer: ...
```

Public guarantees:

- no external provider call;
- no commercial entitlement requirement;
- no canonical mutation;
- bounded local evidence use;
- applicable redaction before presentation.

Current source candidate:

```text
src/jjones/pipeline/strict_clone.py
```

The current `StrictCloneAnswer` and `answer_from_local_evidence` are public
candidates, but their mode and retrieval dependencies must be replaced with
public contracts.

### 3.7 Provider-neutral model port

```python
class ModelProvider(Protocol):
    def generate(self, request: ProviderRequest) -> ProviderResponse: ...


class AskTransportCheckpoint(Protocol):
    def before_transport(self, request: ProviderRequest) -> None: ...
```

Current source candidate:

```text
src/jjones/providers/base.py
```

Public responsibility:

- describe a provider-neutral request and response;
- provide a transport checkpoint hook;
- remain replaceable.

Private exclusions:

- provider factory;
- provider allowlists;
- credentials;
- classification policy;
- disclosure receipt implementation;
- commercial spend and entitlement behavior.

### 3.8 Prompt-fencing port

```python
class PromptFencingPort(Protocol):
    def fence(self, content: UntrustedContent) -> FencedContent: ...
```

Current source candidate:

```text
src/jjones/providers/prompt.py
```

The public implementation may provide generic untrusted-content fencing. It
must not import the private J-Jones policy engine or publish private prompt
templates.

### 3.9 Public export ports

```python
class PublicProjectionPort(Protocol):
    def project(self, documents: Sequence[NoteDocument]) -> PublicBundle: ...


class PublicExportPort(Protocol):
    def preview(self, selection: ExportSelection) -> ExportPreview: ...
    def publish(self, preview_id: str, confirmation: str) -> ExportResult: ...
```

Current source candidates:

```text
src/jjones/pipeline/okf_export_content.py
src/jjones/pipeline/okf_export_files.py
src/jjones/pipeline/okf_export.py
```

Public responsibilities:

- explicit public classification;
- secret and local-locator screening;
- bounded files and archives;
- source revalidation before publication;
- explicit human confirmation.

Private exclusions:

- private principals;
- private presence implementation;
- private export receipt persistence;
- private canonical metadata;
- private workspace paths.

### 3.10 Generic backup crypto port

```python
class BackupCipherPort(Protocol):
    def encrypt(self, source: BinaryIO, destination: BinaryIO, key: bytes) -> None: ...
    def decrypt(self, source: BinaryIO, destination: BinaryIO, key: bytes) -> None: ...
```

Current source candidate:

```text
src/jjones/backup/crypto.py
```

This port does not include keyring lookup, key-file discovery, workspace scope,
restore promotion, evidence rebinding, or private backup policy.

### 3.11 Public settings port

```python
class PublicSettingsPort(Protocol):
    def load(self) -> PublicSettings: ...
    def safe_summary(self) -> Mapping[str, str]: ...
```

Current source candidate:

```text
src/jjones/config/settings.py
```

The public implementation must not import private provider configuration,
secret-provider resolution, installation-role logic, licensing, or private
approval settings.

## 4. Current module action plan

| Current module | Action | Reason |
|---|---|---|
| `src/jjones/evidence/hashing.py` | Candidate for direct extraction | Narrow, generic content identity behavior. |
| `src/jjones/backup/crypto.py` | Extract behind a public crypto module | Generic cryptographic stream behavior is separable from private key and restore policy. |
| `src/jjones/pipeline/audio.py` | Extract media detection only | Sensitivity defaults and transcription policy remain private. |
| `src/jjones/providers/base.py` | Extract public protocol | Provider implementations and routing remain private. |
| `src/jjones/memory/notes.py` | Split | Current generic parsing is mixed with J-Jones note rules. |
| `src/jjones/providers/prompt.py` | Split or rewrite | Current prompt code imports private policy behavior. |
| `src/jjones/evidence/capture.py` | Split or rewrite | Current capture service imports private policy, audit, retention, and secret controls. |
| `src/jjones/evidence/manifest.py` | Extract generic manifest layer | Domain model and private lineage must be separated. |
| `src/jjones/evidence/journal.py` | Extract generic journal layer | Keep private recovery consequences out. |
| `src/jjones/evidence/verify.py` | Split | Generic integrity report may be public; J-Jones reconciliation may not be. |
| `src/jjones/persistence/db.py` | Rebuild for public schema | Current module imports private ORM metadata and migration paths. |
| `src/jjones/retrieval/search.py` | Split | Generic FTS is mixed with private evidence and canonical ordering. |
| `src/jjones/pipeline/strict_clone.py` | Rebuild against public ports | Current implementation imports current mode and retrieval internals. |
| `src/jjones/pipeline/okf_export_content.py` | Split or rewrite | Current projection imports private models, projection, and secret policy. |
| `src/jjones/pipeline/okf_export_files.py` | Extract generic safe-file layer | Current path policy is private and workspace-specific. |
| `src/jjones/pipeline/okf_export.py` | Rebuild public service | Current service imports private identity, presence, and receipts. |
| `src/jjones/cli/okf_*.py` | Rebuild as public adapters | Current commands build private context and use private authorization. |
| `src/jjones/config/settings.py` | Rebuild public settings | Current settings load private secrets, paths, installation, and provider behavior. |
| `src/jjones/cli/context.py` | Exclude | Private composition root. |
| `src/jjones/persistence/orm.py` | Exclude from public implementation | Private schema and governance tables. |
| `src/jjones/policies/*` | Exclude | Private policy YAML and policy engine. |
| `src/jjones/proposals/*` | Exclude | Private canonical mutation and approval. |
| `src/jjones/pipeline/context_compilation.py` | Exclude | Private classification and provider-disclosure behavior. |
| `src/jjones/pipeline/disclosure.py` | Exclude | Private disclosure ledger and receipt verification. |
| `src/jjones/security/*` | Exclude except future generic ports | Private identity, authority, elevation, secrets, and path policy. |
| `src/jjones/mcp/*` | Exclude from first public Core | Private governed integration behavior. |
| `src/jjones/acp/*` | Exclude from first public Core | Private local agent authority behavior. |
| `src/jjones/pipeline/claude_code_*` | Exclude | Private external-session ingestion. |
| `src/jjones/pipeline/video.py` | Defer | Multimodal provider and processing boundary is not required for first Core. |
| `src/jjones/retrieval/hybrid.py` | Defer or exclude | Vector and embedding privacy boundary is unresolved. |

## 5. Forbidden public imports

The following imports are prohibited in a public Core implementation:

```text
jjones.policies.engine
jjones.proposals.service
jjones.proposals.workflow
jjones.pipeline.modes
jjones.runtime.mode_activation
jjones.pipeline.context_compilation
jjones.pipeline.disclosure
jjones.security.principal
jjones.security.ask_authority
jjones.security.elevation
jjones.security.secret_provider
jjones.providers.factory
jjones.persistence.orm
jjones.persistence.okf_export_receipts
jjones.cli.context
jjones.licensing.product
jjones.mcp
jjones.acp
jjones.pipeline.claude_code_sessions
jjones.pipeline.claude_code_snapshots
```

These are implementation-boundary rules, not a request to delete or alter the
current private modules.

## 6. Public-to-private adapter rules

Private J-Jones may adapt to public protocols in these directions:

```text
private CaptureService -> public EvidenceCapturePort
private provider adapter -> public ModelProvider
private search adapter -> public SearchIndexPort
private Strict Clone wrapper -> public LocalAnswerPort
private export wrapper -> public PublicExportPort
private backup wrapper -> public BackupCipherPort
private settings adapter -> public PublicSettingsPort
```

The adapter must:

- enforce private policy before calling the public protocol;
- avoid exposing private state through public return values;
- avoid passing private canonical IDs unless the public contract requires them;
- avoid using public interfaces as a canonical-write authority path;
- preserve audit and disclosure behavior inside the private adapter.

## 7. Data and referential-integrity seams

### Public references

Public Core may use:

```text
public note IDs
public evidence IDs
content hashes
public manifest paths
public index source references
public export bundle identities
```

### Private references

Public Core must not depend on:

```text
proposal IDs
private source-to-claim IDs
private derivation roots
private disclosure receipt IDs
owner/session IDs
recipient grant IDs
private audit event IDs
private provider configuration IDs
private entitlement IDs
```

### Foreign-key boundary

The public Core needs its own metadata root and migration history. It must not
reuse private `Base` metadata or import private ORM models merely to satisfy a
foreign key.

### Derived-index boundary

Public FTS or cache tables may reference public note and evidence IDs, but they
must be rebuildable and must not be used as the authority source.

## 8. Inheritance and composition rules

The public Core should use composition and protocols rather than subclassing
private application services.

Allowed:

```text
public data model -> generic validation base
public adapter -> public protocol
public exception -> public generic exception
```

Not allowed:

```text
public service -> private ProposalService
public service -> private ModeSessionService
public service -> private AskExecutionService
public provider -> private provider adapter
public ORM -> private ORM Base
```

If the current implementation depends on a private base class, define a
public protocol or public base contract and write a separate implementation.

## 9. Public test seams

Each public protocol requires tests at three levels:

### Contract tests

Verify that any implementation satisfies the public interface:

```text
hashing contract
manifest contract
journal contract
search-index contract
provider-port contract
local-answer contract
public-export contract
backup-crypto contract
```

### Security and privacy tests

Verify that public behavior:

- rejects unsafe paths;
- rejects secrets in public exports;
- rejects local and private-network locators;
- does not make provider calls in Strict Clone;
- does not mutate canonical state;
- does not treat index rows as canonical truth;
- does not import private modules;
- does not expose credentials or private database paths.

### Property and integration tests

Verify that:

- indexes rebuild from source;
- hashes and manifests round-trip;
- journal recovery is bounded;
- public export is deterministic within its contract;
- public import cannot bypass evidence or proposal boundaries;
- public backup crypto detects tampering;
- public local answering remains usable without external AI.

Private tests must not be copied into the public repository until the test and
fixture map is approved.

## 10. Implementation order after approval

Do not begin by moving files. Use this sequence:

1. Approve this seam plan.
2. Create the public Core package and migration design documents.
3. Define public domain types and protocols without private imports.
4. Add import-boundary checks that fail if public modules import forbidden private modules.
5. Extract the pure hashing and media-detection utilities.
6. Extract generic manifest and journal behavior.
7. Build the independent public persistence metadata and migration chain.
8. Build the public FTS index against public source types.
9. Build Strict Clone against public retrieval contracts.
10. Build public export projection and safe-file contracts.
11. Add public contract, security, property, and integration tests.
12. Create public packaging and documentation.
13. Run the complete public Core checks.
14. Re-audit imports, secrets, paths, policy leakage, and license boundaries.
15. Only then decide whether any implementation can be copied rather than rewritten.

## 11. Stop gates

### Stop Gate A: interface approval

No source split until public protocol names, fields, error behavior, and
authority limitations are approved.

### Stop Gate B: database approval

No public persistence implementation until public tables, foreign keys,
derived indexes, migrations, and private-table exclusions are approved.

### Stop Gate C: import-boundary enforcement

No public package extraction until automated checks reject forbidden imports.

### Stop Gate D: test-boundary approval

No test copying until public tests and private tests/fixtures are classified.

### Stop Gate E: release-boundary approval

No public release artifact, publication, or open-source announcement until the
public package, license, documentation, and security boundary are separately
approved.

## Current status

```text
PUBLIC_CORE_MECHANISM_REGISTER: IMPLEMENTED / UNVALIDATED
PUBLIC_CORE_CLAIM_MODULE_MAP: IMPLEMENTED / UNVALIDATED
PUBLIC_CORE_SEAM_PLAN: IMPLEMENTED / UNVALIDATED
PUBLIC_PROTOCOLS: PROPOSED / NOT IMPLEMENTED
PUBLIC_SCHEMA: NOT STARTED
PUBLIC_MIGRATIONS: NOT STARTED
PUBLIC_SOURCE_SPLIT: NOT STARTED
PUBLIC_TEST_SPLIT: NOT STARTED
PUBLIC_RELEASE: NOT APPROVED
```

The next artifact is:

```text
docs/ip/PUBLIC_CORE_SCHEMA_SPLIT.md
```

That document must define the public tables, private tables, foreign keys,
application-level references, derived indexes, migration boundary, and restore
or export implications before any database or source split begins.
