# Public Core Schema Split

Status: `OWNER APPROVED FOR PLANNING`

Evidence status: `OBSERVED` for the current private schema and `PROPOSED` for
the public schema. This document is an architecture plan, not a migration and
not permission to alter the current database.

Related documents:

- [PUBLIC_CORE_MECHANISM_REGISTER.yaml](PUBLIC_CORE_MECHANISM_REGISTER.yaml)
- [PUBLIC_CORE_CLAIM_MODULE_MAP.md](PUBLIC_CORE_CLAIM_MODULE_MAP.md)
- [PUBLIC_CORE_SEAM_PLAN.md](PUBLIC_CORE_SEAM_PLAN.md)

## 1. Decision summary

The public Core should use:

```text
separate package
separate SQLite database
separate ORM metadata root
separate Alembic migration history
separate test database fixtures
separate backup/export scope
```

The public Core must not import the private ORM metadata or share the private
J-Jones database merely to avoid duplicating tables.

The private J-Jones Desktop product may consume public Core interfaces or
public data through an explicit adapter. The public Core must not consume the
private database, private migrations, or private governance services.

## 2. Current private schema observed

The current private ORM base is:

```text
src/jjones/persistence/orm.py
Base(DeclarativeBase)
```

Observed private or review-sensitive ORM classes include:

### Identity and authority

```text
OwnerAccountORM
OwnerSessionORM
ModeSessionORM
RecipientGrantORM
DeviceTrustORM
WebAuthnCredentialORM
ApprovalEnrollmentORM
```

### Evidence and source control

```text
EvidenceORM
CaptureActivityORM
ImportSourceORM
```

### Canonical governance and audit

```text
ProposalORM
AuditEventORM
```

### Provider, disclosure, and commercial state

```text
ProviderConfigurationORM
DisclosureReceiptORM
DisclosureItemORM
DisclosureOutcomeORM
ProviderSpendORM
```

### Derived and operational state

```text
QuestionORM
NoteEmbeddingORM
SyncReplayORM
OperatorFocusORM
PulseDiagnosticHistoryORM
PulseHistoryReceiptORM
PulseHistoryReservationORM
```

These current tables remain private or review-required until a separate
public schema is implemented and tested.

## 3. Current database integrity observed

The current database layer is implemented in:

```text
src/jjones/persistence/db.py
```

Important current functions include:

```text
create_sqlite_engine
create_session_factory
init_schema
run_migrations
migration_head_revision
snapshot_sqlite_database
session_scope
```

Observed protections include:

- SQLite foreign keys enabled.
- Write-ahead logging.
- Busy timeout.
- Alembic migration execution.
- Migration-head inspection.
- Pre-migration database snapshots where applicable.
- Commit on successful session scope.
- Rollback on exception.
- Session closure after operation.
- ORM constraints and indexes.
- SQLite triggers for selected immutable grant behavior.

The public Core must retain the generic transaction and integrity properties,
but it must not reuse private table metadata or private migration history.

## 4. Proposed public Core tables

The following table names are proposed and are not implemented. They are
deliberately generic and must be finalized before a public migration is written.

### 4.1 Public source documents

```text
core_documents
```

Proposed purpose:

- Store public Core-owned note or document metadata.
- Store a stable public document identity.
- Store relative public paths or content references.
- Store document status needed for local retrieval.

Proposed fields:

```text
document_id
title
document_type
relative_path
content_hash
created_at
updated_at
status
public_sensitivity
```

Prohibited fields:

```text
private proposal IDs
private claim authority states
private provider IDs
private disclosure receipt IDs
private owner/session IDs
private entitlement IDs
```

### 4.2 Public evidence records

```text
core_evidence
```

Proposed purpose:

- Record public Core evidence identity.
- Bind an evidence record to a content hash.
- Record generic capture metadata.
- Preserve a generic source relationship.

Proposed fields:

```text
evidence_id
source_type
original_name
storage_path
content_hash
mime_type
size_bytes
captured_at
captured_by
public_sensitivity
status
```

The public schema must not store raw secret content or private provider
responses merely because an evidence row exists.

### 4.3 Public manifests

```text
core_evidence_manifests
```

Proposed purpose:

- Track generic manifest identity.
- Bind manifest records to public evidence IDs.
- Support verification and rebuild.

Proposed relationship:

```text
core_evidence_manifests.evidence_id
    -> core_evidence.evidence_id
```

### 4.4 Public capture journal

```text
core_capture_journal
```

Proposed purpose:

- Record bounded in-progress capture state.
- Support recovery from interrupted writes.
- Prevent incomplete capture from appearing complete.

The journal must not store raw private content or full prompts.

### 4.5 Public index state

```text
core_index_state
```

Proposed purpose:

- Track indexed public source paths.
- Store content hash, size, and modification state.
- Support deterministic synchronization.
- Detect when a rebuild is necessary.

Proposed relationship:

```text
core_index_state.document_id
    -> core_documents.document_id
```

The FTS table itself is derived and may be recreated. It must not become the
source of canonical truth.

### 4.6 Public export staging state

This table is optional and should not be added until the public export contract
is approved.

```text
core_export_previews
```

If implemented, it may contain:

```text
preview_id
selection_hash
bundle_hash
destination_class
expires_at
status
```

It must not contain private principal identifiers, private receipt IDs, private
canonical fields, or full private export content.

## 5. Tables explicitly excluded from the public Core

The following table classes remain private:

### Authority and identity

```text
owner accounts
owner sessions
mode sessions
recipient grants
device trust
WebAuthn credentials
approval enrollment
```

### Canonical governance

```text
proposals
proposal transitions
canonical-write state
private audit events
claim authority projections
private source-to-claim lineage
```

### Provider and disclosure

```text
provider configuration
provider spend
disclosure receipts
disclosure items
disclosure outcomes
context compilation receipts
```

### Private import and operational state

```text
private import-source consent
private sync replay
private pulse history
private operator focus
private provider-specific diagnostics
private embedding and vector state
```

The exclusion is based on the meaning of the state, not merely its table name.

## 6. Foreign-key and referential-integrity boundary

### Public database-enforced references

The public Core may enforce direct foreign keys such as:

```text
core_evidence_manifests.evidence_id
    -> core_evidence.evidence_id

core_index_state.document_id
    -> core_documents.document_id
```

### Public application-enforced references

The public Core may validate:

```text
document path remains within public root
content hash matches source content
manifest refers to an existing public evidence record
index row refers to an existing public document
export selection refers only to public documents
```

### References that must not cross the boundary

The public database must not contain foreign keys or application references to:

```text
private proposal IDs
private claim IDs
private derivation roots
private disclosure receipt IDs
private owner/session IDs
private grant IDs
private provider configuration IDs
private entitlement IDs
private audit event IDs
```

If the private product needs to associate a private proposal with a public
document, that relationship must remain in a private adapter or private
database. It must not be added as a public Core foreign key.

## 7. Migration boundary

The public Core requires a separate migration root:

```text
public-core/migrations/
```

It must have:

```text
independent Alembic environment
independent migration revisions
independent metadata target
independent database URL
independent test database setup
```

The public migration chain must not import:

```text
src/jjones/persistence/orm.py
private migration revisions
private settings loaders
private installation-role logic
```

The first public migration should create only the approved public tables. It
must not create empty placeholders for private tables merely to preserve an
old schema shape.

## 8. Database file and path boundary

The public Core should use a distinct database path and configuration key from
the private J-Jones Desktop application.

The public Core must not default to:

```text
private data directory
private runtime database
private production database
private workspace database
```

The public Core must not infer the private repository root by searching parent
directories.

The public database path must be:

- explicit or derived only from public settings;
- safe to display in a redacted summary;
- independent from private provider and licensing configuration;
- easy to back up and delete as a standalone public Core data set.

## 9. Backup and restore implications

The public backup scope must be separate from private J-Jones backup scope.

### Public backup candidates

```text
public Core database
public Core documents
public Core evidence metadata
public Core manifests
public Core journal state where recovery requires it
public Core configuration that contains no secrets
```

### Private backup exclusions

```text
private brain
private proposals
private disclosure ledger
private provider configuration
private owner and session state
private passkeys and elevation state
private licensing state
private private audit records
```

The public Core must not restore into a private J-Jones workspace by default.

The private product may import a public bundle only through an explicit,
screened, evidence-first path. Public import must not become a direct private
canonical-write path.

## 10. Export and import implications

### Public export

Public export should read only explicitly public data:

```text
public document
    -> public projection
    -> screen secrets and local locators
    -> bounded archive
    -> explicit publication confirmation
```

### Public import

Public import should follow:

```text
external bundle
    -> parse
    -> screen
    -> preview
    -> capture as public evidence or draft
    -> optional local review
    -> no direct canonical mutation
```

The public schema must not create a proposal table merely because imported
content may eventually be reviewed by the private J-Jones product.

## 11. ORM and model boundary

The public Core requires a new metadata root, for example:

```python
class PublicCoreBase(DeclarativeBase):
    pass
```

This is a proposed design, not an implementation instruction yet.

Public ORM models must not inherit from or import the private:

```python
jjones.persistence.orm.Base
```

Public domain models should remain independent of SQLAlchemy. Public
repositories should translate between public domain models and public ORM
models.

The public ORM layer must not contain private authority behavior in model
constructors, SQLAlchemy events, triggers, or import-time registration.

## 12. Derived-index boundary

The public FTS index and any future public embedding index are derived state.

Required properties:

- delete and rebuild without losing canonical source data;
- deterministic rebuild from public source data;
- content hash or generation tracking;
- no reverse mutation from index into source;
- no private evidence or claim IDs;
- no provider disclosure by indexing alone;
- no canonical authority inferred from rank or score.

Vector and embedding support is deferred from the first public schema because
its provider, retention, privacy, and reconstruction implications are not yet
approved.

## 13. Public test database boundary

Public tests must use a public-only database fixture.

The fixture must not:

- import private ORM classes;
- run private migrations;
- create private governance tables;
- use private runtime environment variables;
- load private credentials;
- point at the private workspace database.

Public database tests should cover:

```text
foreign-key enforcement
rollback on failure
manifest-to-evidence relationships
index-to-document relationships
rebuild after index deletion
public export preview expiry
public import evidence-first behavior
```

## 14. Proposed migration sequence

No migration should be written until this sequence is approved:

1. Define public domain records.
2. Define public ORM metadata root.
3. Define public tables and direct foreign keys.
4. Define public application-level references.
5. Define public FTS/index tables as derived state.
6. Define public SQLite engine settings.
7. Define public migration environment.
8. Add initial public migration.
9. Add public database contract tests.
10. Add rebuild and rollback tests.
11. Verify no public module imports private ORM or migration modules.
12. Re-audit backup, export, and import paths.

## 15. Stop gates

### Schema Gate A

Every public table has an owner, purpose, sensitivity, and rebuildability
classification.

### Schema Gate B

Every foreign key is either public-to-public or removed. No private table is a
public dependency.

### Schema Gate C

The public migration chain has an independent metadata root and environment.

### Schema Gate D

Public backup, export, import, and restore paths do not cross into private
canonical state without an explicit private adapter.

### Schema Gate E

Public database tests pass without private settings, credentials, migrations,
or runtime databases.

## Current status

```text
PUBLIC_CORE_SCHEMA_SPLIT: IMPLEMENTED / UNVALIDATED
PUBLIC_TABLES: PROPOSED
PRIVATE_TABLE_EXCLUSIONS: OBSERVED / PROPOSED BOUNDARY
PUBLIC_FOREIGN_KEYS: PROPOSED
PUBLIC_MIGRATION_CHAIN: NOT STARTED
PUBLIC_DATABASE_IMPLEMENTATION: NOT STARTED
PUBLIC_BACKUP_SCOPE: PROPOSED
PUBLIC_RELEASE: NOT APPROVED
```

The next artifact should be:

```text
docs/ip/PUBLIC_CORE_BOUNDARY_PROPOSAL.md
```

That document should combine the mechanism register, module map, seam plan,
and schema plan into one file-by-file public/private repository boundary.
