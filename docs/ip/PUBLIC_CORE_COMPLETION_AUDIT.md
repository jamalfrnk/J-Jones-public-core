# Public Core Split Planning Completion Audit

Status: `OWNER APPROVED FOR PLANNING`

Evidence basis: current worktree, current source inspection, YAML parsing, and
static public-artifact checks. No source split, database migration, public
release, or legal patent assessment has been performed.

## 1. Requirement-by-requirement audit

| Requirement | Evidence | Status |
|---|---|---|
| Private mechanism inventory exists outside public artifacts | private mechanism inventory (not included in public artifacts) | `IMPLEMENTED / UNVALIDATED` |
| Public mechanism register exists | `docs/ip/PUBLIC_CORE_MECHANISM_REGISTER.yaml` | `IMPLEMENTED / UNVALIDATED` |
| Public schema split is documented | `docs/ip/PUBLIC_CORE_SCHEMA_SPLIT.md` | `IMPLEMENTED / UNVALIDATED` |
| Public/private boundary is documented | `docs/ip/PUBLIC_CORE_BOUNDARY_PROPOSAL.md` | `IMPLEMENTED / UNVALIDATED` |
| Public/private module map exists | `docs/ip/PUBLIC_CORE_CLAIM_MODULE_MAP.md` | `IMPLEMENTED / UNVALIDATED` |
| Public protocol seams are documented | `docs/ip/PUBLIC_CORE_SEAM_PLAN.md` | `IMPLEMENTED / UNVALIDATED` |
| Loopback threat model exists | `docs/ip/PUBLIC_CORE_LOOPBACK_THREAT_MODEL.md` | `IMPLEMENTED / UNVALIDATED` |
| Tokenless-loopback decision is recorded | `docs/ip/PUBLIC_CORE_TOKENLESS_DECISION.md` | `OWNER_APPROVED_OPTION_A_EXPLICIT_AUTHENTICATION` |
| Public test and fixture boundary exists | `docs/ip/PUBLIC_CORE_TEST_AND_FIXTURE_MAP.md` | `IMPLEMENTED / UNVALIDATED` |
| Public packaging boundary exists | `docs/ip/PUBLIC_CORE_PACKAGING_BOUNDARY.md` | `IMPLEMENTED / UNVALIDATED` |
| Public documentation boundary exists | `docs/ip/PUBLIC_CORE_DOCUMENTATION_MAP.md` | `IMPLEMENTED / UNVALIDATED` |
| Dependency/privacy/security audit exists | `docs/ip/PUBLIC_CORE_BOUNDARY_AUDIT.md` | `IMPLEMENTED / UNVALIDATED` |
| No source files moved | current Git status | `OBSERVED` |
| No database or migrations changed | current Git status | `OBSERVED` |
| No public release performed | current Git status and task actions | `OBSERVED` |
| No private artifacts copied into public artifacts | public-artifact scan | `OBSERVED` |

## 2. Artifact validation evidence

The public mechanism register currently parses as valid YAML and contains:

```text
mechanisms: 19
next_artifacts: 11
missing_next_artifacts: 0
```

The public planning artifact directory contains the required files:

```text
private mechanism inventory (not included in public artifacts)
PUBLIC_CORE_MECHANISM_REGISTER.yaml
PUBLIC_CORE_CLAIM_MODULE_MAP.md
PUBLIC_CORE_SEAM_PLAN.md
PUBLIC_CORE_SCHEMA_SPLIT.md
PUBLIC_CORE_BOUNDARY_PROPOSAL.md
PUBLIC_CORE_LOOPBACK_THREAT_MODEL.md
PUBLIC_CORE_TOKENLESS_DECISION.md
PUBLIC_CORE_TEST_AND_FIXTURE_MAP.md
PUBLIC_CORE_PACKAGING_BOUNDARY.md
PUBLIC_CORE_DOCUMENTATION_MAP.md
PUBLIC_CORE_BOUNDARY_AUDIT.md
PUBLIC_CORE_COMPLETION_AUDIT.md
```

The bounded public-artifact scan found no direct reference to the following
private-content categories:

```text
private mechanism inventory filename
patent directories
private pitch directories
raw evidence directories
runtime launcher artifacts
environment files
```

This does not prove that all sensitive meaning has been removed. It proves only
that the listed direct references were not observed by the bounded scan.

## 3. Concrete dependency evidence

Current public candidates still cross private imports:

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

These are not failures of the planning work. They are evidence that the source
split must use new public seams or rewrites rather than copying current files.

## 4. Requirements not yet proven

The following are not proven because implementation has not started:

```text
public package imports no private modules
public schema can operate independently
public migrations can run independently
public tests use no private fixtures
public Strict Clone operates without private runtime composition
public export cannot disclose private paths or secrets
public backup crypto is safe for public release
public package licensing is approved
public documentation is legally and commercially approved
```

## 5. Owner approvals recorded

The owner approved the following planning boundaries on 2026-11-16:

```text
tokenless loopback disabled by default
explicit authentication for public Core access
non-loopback access requires explicit authentication and security validation
public package, database, schema, export, API, CLI, license, and packaging boundary
```

## 6. Prohibited next actions before approval

Do not yet:

- move source files;
- copy the private ORM into the public package;
- create public migrations from private migrations;
- publish or push the public package;
- change the license;
- enable public provider dispatch;
- implement tokenless loopback access;
- copy private tests or fixtures;
- publish private policy or prompt files;
- create release artifacts.

## 7. Current conclusion

```text
PLANNING_ARTIFACTS: IMPLEMENTED / UNVALIDATED
ENGINEERING_BOUNDARY: DOCUMENTED
DEPENDENCY_AUDIT: OBSERVED FINDINGS RECORDED
SOURCE_SPLIT: NOT STARTED
PUBLIC_RELEASE: NOT APPROVED
GOAL: OWNER_APPROVED_PLANNING_COMPLETE
```

The next work, if requested, is implementation of the approved public/private
seams in an isolated branch or worktree. Public release remains separately
unapproved until implementation, testing, licensing, and release validation are
complete.
