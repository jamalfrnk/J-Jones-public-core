# J-Jones Public Core

Public, local-first building blocks for governed knowledge continuity.

J-Jones Public Core is an independent Python package. It is not the private
J-Jones Desktop application, not a hosted AI service, and not a replacement for
the private governance, identity, entitlement, provider, persistence, or
commercial systems.

## Status

This repository is an alpha public implementation slice.

    package:             jjones-public-core
    import namespace:    jjones_core
    license:             Apache-2.0
    minimum Python:     3.12
    GitHub release:      v0.1.0-alpha.2
    package metadata:    0.1.0a1 (candidate branch remains unreleased)
    release date:       2026-11-17
    desktop application: not included
    graphical UI:        not included
    hosted service:      not included

The current release contains generic note parsing, untrusted-content fencing,
provider-neutral contracts, local evidence hashing, rebuildable SQLite FTS5
retrieval, and explicit-authentication primitives.

The authenticated local HTTP boundary in this branch is a release candidate
for the next public release. It is implemented and tested locally, but it is
not represented as part of v0.1.0-alpha.2 until this branch is reviewed,
merged, and released.

## What is implemented

The public Core currently provides:

- Markdown notes with YAML front matter.
- Generic metadata validation.
- Rejection of secret-prohibited content as canonical note content.
- Provider-neutral request and response data classes.
- A deterministic minimum prompt-token bound.
- Nonce-delimited fencing for untrusted retrieved content.
- Fence-marker neutralization and control-character removal.
- SHA-256 evidence manifests.
- Rebuildable local SQLite FTS5 search.
- An explicit API-key-to-session local HTTP boundary in the next-release
  candidate.
- Public tests, package metadata, lockfile, CI, dependency audit, and secret
  scanning.

## What is deliberately not implemented

The public Core does not provide:

- The private J-Jones Desktop application.
- A graphical user interface.
- A Windows or Linux installer.
- Private canonical-knowledge policy.
- Private identity, entitlement, or approval workflows.
- Provider adapters or provider credentials.
- Remote inference.
- Hosted account management.
- Commercial licensing enforcement.
- Private database models or private migrations.
- Canonical mutation or proposal approval.
- Production deployment or production credentials.
- A guarantee of answer quality from any language model.

Those are separate product or private-repository responsibilities.

## Install from source

Requirements:

- Python 3.12 or newer.
- uv, or another Python environment manager.
- SQLite with FTS5 support for local retrieval tests.
- A clean clone of this repository.

PowerShell or a POSIX shell:

    uv sync --locked --extra dev
    uv run --extra dev ruff format --check .
    uv run --extra dev ruff check .
    uv run --extra dev mypy src
    uv run --extra dev bandit -c pyproject.toml -r src
    uv run --extra dev pytest --cov=jjones_core --cov-report=term-missing
    uv run --extra dev pip-audit
    uv build

The package is a library. Running these commands does not launch a desktop
application.

## Local authenticated HTTP boundary

The candidate server is intentionally small and dependency-free.

Default behavior:

- Binds to 127.0.0.1.
- Does not infer identity from loopback.
- Does not allow tokenless loopback requests.
- Requires an API key to create a session.
- Requires a bearer session token for protected requests.
- Keeps only a digest of the configured API key.
- Keeps session-token digests in memory.
- Expires sessions after the configured TTL.
- Does not log request paths, headers, API keys, or session tokens.
- Refuses non-loopback binding unless explicitly opted in.
- Still requires authentication when non-loopback binding is explicitly enabled.

Example:

    from jjones_core.server import ServerConfig, start_server

    server = start_server(
        api_key="owner-provided-key",
        config=ServerConfig(host="127.0.0.1", port=8765),
    )

The API-key exchange is:

    POST /v1/session
    Content-Type: application/json

    {"api_key": "owner-provided-key"}

A successful response returns a short-lived bearer token. A protected request
must send:

    Authorization: Bearer <session-token>

The health endpoint is:

    GET /v1/health

Without a bearer token, the server returns HTTP 401 with a structured
authentication error and visible fallback actions. A request from
127.0.0.1 is not accepted as proof of ownership.

The public Core does not decide how an external service issues or rotates an
API key. A desktop shell or private account service must own that lifecycle.

## End-user workflow: what exists now

An end user who downloads v0.1.0-alpha.2 receives a Python public-Core package,
not a finished J-Jones Desktop app.

The current verified workflow is:

1. The user obtains the source or release artifact.
2. The user verifies the release checksum.
3. The user installs Python 3.12 and the package environment.
4. The user runs the public tests or imports the library.
5. The user may use the public note, prompt-fencing, evidence, retrieval, and
   authentication primitives from their own application.
6. No graphical sign-in screen, tray application, desktop launcher, or provider
   account flow is included in this repository.

The next-release server candidate adds a local authenticated HTTP boundary, but
it still does not create the desktop shell or the account/key-provisioning
service.

## End-user workflow: intended desktop integration

The following is the intended product workflow for a future J-Jones Desktop
application. It is an integration contract and UX design, not a claim that the
public Core already ships the desktop experience.

### 1. Download and verify

The user downloads an owner-published J-Jones Desktop installer or public-Core
release from an approved source.

The first screen should show:

- Product name and version.
- Release channel: stable, beta, or alpha.
- Source and release URL.
- Checksum or signature verification result.
- Local data directory.
- Whether the application is using the public Core, private Desktop Core,
  or a configured provider integration.

A failed checksum or signature must stop launch and provide a clear recovery
link. It must not silently continue.

### 2. First launch

The application creates or selects a local workspace. It should explain:

- Which data remains local.
- Which data is rebuildable.
- Whether any provider connection is configured.
- Whether external inference is disabled.
- Which actions require authentication.
- Which actions require a human approval step.

The default local service should bind to loopback only. Loopback is a network
location, not an identity assertion.

### 3. One-time API-key authentication

The user enters the unique API key through a protected first-run screen.

The screen should show:

- API-key field with paste protection and no echo in logs.
- A clear statement that the key is used to establish a session.
- The destination or account that issued the key.
- The retention behavior: raw key not written to public-Core logs or prompts.
- Session expiration and re-authentication behavior.
- A visible Cancel path that leaves local functionality available when
  applicable.

The public-Core candidate exchanges the API key for an in-memory bearer session.
The raw API key is not retained by the public server after its digest is
created. A desktop application may persist a user credential only through an
owner-approved operating-system credential store; that persistence mechanism is
not included in this public package.

The user should not be told that authentication succeeded merely because the
request came from localhost.

### 4. Normal authenticated session

After authentication, the desktop UI should show:

- Authenticated session state.
- Session expiration time or re-authentication reminder.
- Local index health.
- Canonical-data status.
- Provider status, if a provider is configured.
- Current operating mode.
- Whether external disclosure is disabled, allowed, or awaiting confirmation.
- Whether a response is source-backed, derived, inferred, proposed, or unresolved.

The public Core itself only proves the explicit transport boundary and local
utilities. The desktop shell must supply the product-level status model.

### 5. Retrieval and response presentation

A user question should move through these semantic stages:

1. The UI identifies the request purpose.
2. The application classifies the requested and retrieved data.
3. The local index retrieves bounded candidate records.
4. Evidence identifiers and hashes remain attached to retrieved material.
5. Retrieved content is fenced as untrusted data.
6. A provider is used only if the active product policy permits it.
7. The provider response is labeled as model output.
8. The UI distinguishes source evidence from summaries, inferences, and proposals.
9. The user can inspect the supporting evidence.
10. A model response cannot silently become canonical knowledge.

A good UI should never display a generated answer with the same visual treatment
as an approved canonical note.

### 6. Canonical knowledge changes

The public Core does not implement canonical mutation.

A future Desktop workflow should show a model-generated change as:

    DRAFT PROPOSAL
    source: model output
    support: evidence IDs
    confidence: stated or unresolved
    canonical effect: none until human review

The user must be able to:

- Accept.
- Reject.
- Edit.
- Defer.
- Inspect evidence.
- See what changed.
- See whether the change was model-derived or canonical.
- Undo or recover according to the private product's governed persistence rules.

Model output alone must never be presented as authority.

## Visible fallback behavior

Fallbacks must be visible, specific, and actionable. The UI should not show
a generic “something went wrong” message when the user can take a safe next
step.

### Missing API key

Show:

    Authentication required.
    Loopback access does not prove ownership.

    Available next steps:
    - Enter the configured API key.
    - Open the desktop sign-in flow.
    - Use the owner-controlled recovery flow.
    - Continue with local-only features, if available.

### Invalid API key

Show:

    The key was not accepted.

    Available next steps:
    - Check the key and try again.
    - Confirm the key's account or environment.
    - Use recovery or re-provisioning.
    - Continue with local-only features, if available.

Do not reveal whether a partial key matched, whether an account exists, or which
part of the credential failed.

### Expired session

Show:

    Your local session expired.

    Available next steps:
    - Re-authenticate with the API key.
    - Use the desktop sign-in flow.
    - Continue with local-only features, if available.

### Provider unavailable

Show:

    External reasoning is unavailable.

    Available next steps:
    - Retry.
    - Use a configured local provider, if available.
    - Ask from local indexed knowledge only.
    - Save the question as a draft.

The UI must not silently substitute a provider that has a weaker privacy policy,
different retention behavior, or broader disclosure scope.

### Local index unavailable

Show:

    Local retrieval is unavailable or rebuilding.

    Available next steps:
    - Rebuild the derived index.
    - Inspect the local workspace.
    - Continue with direct local file review.
    - Retry after the rebuild completes.

An index outage must not be represented as loss of canonical knowledge.

## UI/UX principles

The intended J-Jones Desktop experience should make authority and provenance
visible without requiring the user to understand implementation jargon.

Important visual distinctions:

- Canonical note: authoritative local record.
- Evidence: source material and hash/provenance metadata.
- Derived result: rebuildable index or summary.
- Model output: generated response, not canonical truth.
- Proposal: pending human decision.
- Unresolved: information that needs confirmation.
- Restricted: content withheld or redacted by policy.
- External: information that may leave the device.

Useful interaction patterns:

- A persistent authentication/session indicator.
- A local-only versus external-inference indicator.
- A visible provider and model label.
- Evidence chips that open source records.
- A “why am I seeing this?” provenance panel.
- A “what will leave this device?” disclosure preview.
- A clear approval boundary before consequential changes.
- Recovery actions next to every recoverable error.
- No hidden provider fallback.
- No hidden conversion of model output into canonical memory.

## Semantic effectiveness: what it means and how to measure it

The public Core can prove structural and safety properties. It cannot prove that
a language model gives correct answers to every user question.

### What the public Core can validate

- Note metadata is parsed deterministically.
- Malformed front matter fails closed.
- Secret-prohibited content is rejected from canonical note validation.
- Fenced content is treated as untrusted data.
- Fence markers are neutralized.
- Evidence hashes detect changed bytes.
- Derived indexes can be rebuilt.
- Search results come from local indexed records.
- Missing authentication is rejected.
- Loopback does not imply authentication.
- Non-loopback binding is disabled by default.
- Public CI, dependency, and secret checks run.

### What requires a separate evaluation program

- Retrieval precision and recall.
- Evidence citation accuracy.
- Answer faithfulness to evidence.
- Resistance to prompt injection in realistic documents.
- Human usefulness and task completion.
- Provider response quality.
- Latency and resource use.
- Accessibility and UI comprehension.
- Recovery success after provider, index, or authentication failure.
- Cross-platform packaging and upgrade behavior.
- Canonical mutation safety in the private Desktop Core.

Recommended evaluation measures include:

    retrieval precision@k
    retrieval recall@k
    evidence citation precision
    unsupported-claim rate
    prompt-injection success rate
    false-approval rate
    human correction rate
    authentication recovery completion rate
    local-only disclosure violations
    time to understand the fallback action

A green unit-test run does not prove semantic answer quality. Semantic
effectiveness must be measured with a labeled, synthetic, privacy-safe
evaluation set and human review.

## Supported operating systems

### Validated

- Windows development environment with Python 3.12.
- Ubuntu GitHub Actions environment with Python 3.12.

### Intended for public-Core source use

Any operating system that provides:

- Python 3.12 or newer.
- SQLite with FTS5 support.
- A supported Python package environment.
- A filesystem that can hold the local workspace.

This is a design target, not proof that every distribution works.

### Not yet validated or supported as a packaged app

- macOS.
- Windows ARM.
- Linux distribution-specific installers.
- iOS.
- Android.
- ChromeOS.
- Web browsers as a standalone client.
- A signed Windows installer.
- A signed Linux package.
- A full graphical desktop application on any operating system.

The public repository is not currently a downloadable J-Jones Desktop app. A
future desktop release needs separate platform validation for installation,
restart, upgrade, uninstall, recovery, signing, local credential storage,
accessibility, and provider behavior.

## How to know the public repository works

Use several independent forms of evidence.

### Repository checks

    uv sync --locked --extra dev
    uv run --extra dev ruff format --check .
    uv run --extra dev ruff check .
    uv run --extra dev mypy src
    uv run --extra dev bandit -c pyproject.toml -r src
    uv run --extra dev pytest --cov=jjones_core --cov-report=term-missing
    uv build
    uv run --extra dev pip-audit
    uv run --extra dev detect-secrets scan --all-files --exclude-files '(?i)(^|[\\/])(\\.venv|\\.pytest_cache|\\.ruff_cache|\\.mypy_cache|dist)([\\/]|$)'

### Runtime boundary checks

The server test suite must prove:

- No-auth health request returns HTTP 401.
- Loopback does not grant access.
- Invalid API keys return HTTP 401.
- A valid API key creates a session.
- A bearer session can access the protected health endpoint.
- The health response reports tokenless loopback as false.
- Non-loopback binding fails unless explicitly enabled.
- Authentication failures expose safe fallback actions.
- Raw keys are not included in response bodies or logs. A session token is
  returned only by a successful session exchange and is never logged.

### Hosted evidence

The public GitHub repository must show:

- A successful Public Core CI workflow.
- A clean dependency audit.
- A clean secret scan.
- A published source tag.
- Checksums and SBOM for release artifacts.
- An Apache-2.0 license.
- Accurate release notes.
- No private files or private history.

### Limits of the evidence

These checks do not prove:

- A complete J-Jones Desktop app exists.
- A GUI behaves correctly.
- Provider contracts or retention behavior are correct.
- Semantic answer quality is high.
- The application is production-ready.
- Every OS is supported.
- The private J-Jones runtime is reproduced by the public Core.

## Privacy and public/private boundary

Public repository code should remain generic and replaceable.

Keep private:

- Governance policies.
- Approval thresholds.
- Identity and entitlement rules.
- Provider credentials.
- Commercial integrations.
- Private prompts and policy YAML.
- Private databases and migrations.
- User content and professional knowledge.
- Runtime logs and evidence.
- Installer signing and deployment configuration.

Public interfaces may define contracts, but they must not grant private
authority.

## Contributing and security

Read:

- CONTRIBUTING.md
- SECURITY.md
- docs/PUBLIC_CORE_IMPLEMENTATION_STATUS.md
- docs/ip/PUBLIC_CORE_LOOPBACK_THREAT_MODEL.md
- docs/ip/PUBLIC_CORE_TOKENLESS_DECISION.md
- docs/ip/PUBLIC_CORE_TEST_AND_FIXTURE_MAP.md

Never place secrets, user content, provider responses, or confidential
patent/business information in issues, pull requests, fixtures, prompts, or
release artifacts.

This README describes the public Core accurately as an alpha implementation.
It does not claim patentability, production readiness, universal platform
support, or semantic correctness.
