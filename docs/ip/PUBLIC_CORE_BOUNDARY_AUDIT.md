# Public Core Boundary Audit

Status: `OWNER APPROVED PLANNING AUDIT`

Evidence status: `OBSERVED` from current source paths and planning artifacts.
This audit does not claim security certification, patentability, or release
readiness.

## 1. Artifacts reviewed

```text
private mechanism inventory (not included in public artifacts)
docs/ip/PUBLIC_CORE_MECHANISM_REGISTER.yaml
docs/ip/PUBLIC_CORE_CLAIM_MODULE_MAP.md
docs/ip/PUBLIC_CORE_SEAM_PLAN.md
docs/ip/PUBLIC_CORE_SCHEMA_SPLIT.md
docs/ip/PUBLIC_CORE_BOUNDARY_PROPOSAL.md
docs/ip/PUBLIC_CORE_LOOPBACK_THREAT_MODEL.md
docs/ip/PUBLIC_CORE_TOKENLESS_DECISION.md
docs/ip/PUBLIC_CORE_TEST_AND_FIXTURE_MAP.md
docs/ip/PUBLIC_CORE_PACKAGING_BOUNDARY.md
docs/ip/PUBLIC_CORE_DOCUMENTATION_MAP.md
```

## 2. Boundary findings

### Finding A — public candidates are not currently isolated

Several current public candidates import private policy, security, audit,
secret, ORM, or composition modules. A source copy would leak private
dependencies or create an accidental public path into private behavior.

Status: `OBSERVED`

Required action: create public seams or rewrite the modules.

### Finding B — public and private databases must be separate

The current ORM and migrations contain identity, authority, proposal,
disclosure, provider, and commercial state. Public Core must use independent
metadata and migrations.

Status: `OWNER_APPROVED_FOR_PLANNING`

### Finding C — Strict Clone is the best first public runtime

Strict Clone can provide local-only retrieval and answering without external
provider dispatch or commercial AI entitlement, subject to public redaction and
retrieval contracts.

Status: `OBSERVED CANDIDATE`

### Finding D — tokenless loopback is explicitly disabled by default

The owner approved explicit authentication for public-Core planning. The public
Core must not infer owner authentication merely from loopback reachability.

Status: `OWNER_APPROVED_OPTION_A_EXPLICIT_AUTHENTICATION`

### Finding E — public tests must be rebuilt around public state

Private tests may reveal policy, prompts, governance transitions, provider
routing, private fixtures, and private schema. They cannot be copied wholesale.

Status: `OWNER_APPROVED_FOR_PLANNING`

### Finding F — packaging and licensing remain implementation and release gates

The public package, license, lockfile, CI, signing, and release boundary are
approved as planning boundaries, but still require implementation-specific and
legal/release validation before publication.

Status: `OWNER_APPROVED_FOR_PLANNING`

### Finding G — current public candidates cross private imports

The current source inspection observed these private imports in modules that
are otherwise public candidates:

```text
src/jjones/providers/prompt.py -> jjones.policies
src/jjones/evidence/capture.py -> jjones.policies
src/jjones/persistence/db.py -> jjones.persistence.orm
src/jjones/pipeline/okf_export.py -> jjones.security.principal
src/jjones/cli/okf_export.py -> jjones.security.principal
src/jjones/cli/okf_export.py -> jjones.persistence.okf_export_receipts
src/jjones/cli/okf_export.py -> jjones.cli.context
src/jjones/cli/okf_import.py -> jjones.security.principal
src/jjones/cli/okf_import.py -> jjones.cli.context
src/jjones/cli/okf_bundle_import.py -> jjones.security.principal
src/jjones/cli/okf_bundle_import.py -> jjones.cli.context
src/jjones/config/settings.py -> jjones.security.secret_provider
```

Status: `OBSERVED`

Required action: split or rewrite these modules before treating them as public
Core implementations. A public interface may still be retained, but the
current private import graph must not be carried into the public repository.

## 3. Security and privacy audit result

```text
private canonical data exposed by new artifacts: NOT OBSERVED
private patent content copied into public artifacts: NOT OBSERVED
credentials or tokens added: NOT OBSERVED
source code moved: NO
database changed: NO
public provider dispatch enabled: NO
public canonical mutation enabled: NO
public external release performed: NO
```

## 4. Completion boundary for planning phase

The planning phase is owner-approved when:

- the public mechanism register is accepted;
- the claim module map is accepted;
- the seam plan is accepted;
- the schema split is accepted;
- the boundary proposal is accepted;
- tokenless loopback is decided;
- public test and fixture boundaries are accepted;
- packaging and licensing boundaries are accepted.

## 5. Current owner-approved boundaries

The owner approved these planning boundaries on 2026-11-16. They still require
implementation-specific validation before a public release:

```text
tokenless loopback disabled by default; explicit authentication required
non-loopback public Core requires explicit authentication and security validation
public package, schema, export, API, CLI, license, and packaging boundary
```

## 6. Current status

```text
PLANNING_ARTIFACTS: IMPLEMENTED / UNVALIDATED
SOURCE_SPLIT: NOT STARTED
PUBLIC_DATABASE: NOT STARTED
PUBLIC_MIGRATIONS: NOT STARTED
PUBLIC_TESTS: NOT STARTED
PUBLIC_PACKAGING: NOT STARTED
PUBLIC_RELEASE: NOT APPROVED
```
