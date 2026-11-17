# J-Jones Public Core

Public, local-first building blocks for governed knowledge continuity.

This repository is the independent public-Core alpha. It contains generic
interfaces and local utilities for note metadata, untrusted-content fencing,
provider-neutral request contracts, evidence integrity, and rebuildable local
retrieval. It does not contain the private J-Jones Desktop application or its
private policy, identity, entitlement, provider, persistence, deployment, or
commercial systems.

## Status

- Version: 0.1.0-alpha.1
- Release date: 2026-11-17
- License: Apache-2.0
- Scope: public generic interfaces and local utilities
- Canonical knowledge: not owned or mutated by this package
- External inference: not performed by this package

## Install

    uv sync --locked
    uv run pytest
    uv run python -c "import jjones_core; print(jjones_core.__version__)"

## Boundaries

The package treats model output as noncanonical, keeps derived indexes
rebuildable, fences retrieved content as untrusted data, and requires explicit
authentication before a caller crosses a provider transport boundary.

The public package does not provide private governance, commercial licensing,
provider credentials, private approval workflows, or hosted runtime behavior.

## Release and contribution

Read CONTRIBUTING.md, SECURITY.md, and the public boundary documents under
docs/ip before contributing. Do not submit secrets, private user content, or
patent-confidential implementation details.

This alpha is a public implementation slice. Features not represented by the
code and tests are not claimed to be implemented.
