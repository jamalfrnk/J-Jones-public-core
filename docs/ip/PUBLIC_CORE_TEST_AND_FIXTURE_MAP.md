# Public Core Test and Fixture Map

Status: `OWNER APPROVED FOR PLANNING`

Evidence status: `OBSERVED` for current test areas and `PROPOSED` for the
public test split. No tests or fixtures have been moved.

## 1. Rule

The public test suite must prove public behavior without importing or revealing
private policy, canonical governance, provider disclosure, identity, or
commercial implementation.

## 2. Public test candidates

| Public behavior | Candidate test area | Required public assertion |
|---|---|---|
| Note parsing | `tests/unit` or new public unit tests | Generic metadata parses, renders, and validates without private authority rules. |
| Hashing | new public unit tests | Byte and file hashes are deterministic. |
| Manifest verification | new public contract tests | Valid manifests pass; mismatches are reported. |
| Journal behavior | new public property/integration tests | Interrupted writes are visible and bounded. |
| FTS retrieval | new public contract and integration tests | Search is deterministic and rebuildable. |
| Strict Clone | new public integration tests | No external provider is called and no canonical write occurs. |
| Public export screening | `tests/property/test_okf_roundtrip.py` plus new public tests | Secrets, local paths, and private network references are rejected. |
| Public metadata round trip | `tests/property/test_metadata_roundtrip.py` | Public metadata remains stable and bounded. |
| Safe file access | new public security tests | Links, reparse points, path traversal, and changing files are rejected. |
| Provider port | new public contract tests | Provider implementations satisfy the neutral protocol only. |
| Public backup crypto | new public security tests | Tampering and invalid headers fail closed. |

## 3. Tests requiring private treatment

Do not copy these unchanged into a public repository:

```text
proposal approval tests
canonical mutation tests
claim authority tests
epistemic ceiling tests
disclosure ledger tests
provider egress tests
authentication fallback tests
browser-session tests
mode authority tests
passkey and elevation tests
private migration tests
private ORM tests
private prompt and extraction tests
private MCP and ACP tests
Claude Code session tests
private release, signing, and deployment tests
```

## 4. Fixture rules

Public fixtures must use:

```text
synthetic notes
synthetic evidence
synthetic public paths
synthetic provider responses
synthetic identities
synthetic hashes
```

Public fixtures must not contain:

```text
private canonical notes
real evidence
real provider prompts or responses
credentials
tokens
private filesystem paths
private database snapshots
patent material
```

## 5. Public database fixture

The public tests require a public-only database fixture that:

- imports the public ORM metadata only;
- runs public migrations only;
- creates no private governance tables;
- uses a temporary database path;
- enables foreign keys;
- does not load private settings or credentials.

## 6. Import-boundary tests

Add a public-package test that fails if public modules import private modules,
including:

```text
jjones.policies
jjones.proposals
jjones.runtime.mode_activation
jjones.pipeline.context_compilation
jjones.pipeline.disclosure
jjones.security.principal
jjones.security.elevation
jjones.providers.factory
jjones.persistence.orm
jjones.cli.context
jjones.licensing
jjones.mcp
jjones.acp
```

## 7. Required public test stages

```text
contract tests
unit tests
property tests
database integrity tests
security/path tests
local-only behavior tests
public export/import tests
dependency-boundary tests
packaging smoke tests
```

## 8. Status

```text
PUBLIC_TEST_MAP: IMPLEMENTED / UNVALIDATED
PUBLIC_TEST_SUITE: NOT CREATED
PRIVATE_TEST_SPLIT: NOT STARTED
FIXTURE_REDACTION_AUDIT: NOT STARTED
```
