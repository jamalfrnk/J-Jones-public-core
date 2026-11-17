# J-Jones Public Core

## Public-Core GitHub Handoff

This archive is the owner-approved planning and release-boundary handoff for
the proposed J-Jones Public Core repository.

It is intentionally **not** the private J-Jones Desktop repository, and it is
not yet an implemented or publishable source-code release. The current
workspace contains private runtime code, private policy, private operational
configuration, patent-sensitive material, user/runtime state, and release
artifacts that are not included in this handoff.

The handoff is designed to be used before creating an empty GitHub repository
for the independent public Core implementation.

## Proposed repository identity

**Repository title:** J-Jones Public Core

**Suggested repository name:** `J-Jones`

**Suggested description:**

> Public, local-first building blocks for governed knowledge continuity:
> deterministic notes, evidence integrity, rebuildable indexes,
> provider-neutral interfaces, and screened exports.

That description must be revised if the first public implementation does not
yet provide all of those behaviors. Public documentation must describe what
is implemented and tested, not only what is planned.

## What this handoff contains

- The public mechanism register.
- The private/public claim and module boundary plan.
- The separate schema and migration boundary.
- The public seam, dependency, packaging, and documentation plans.
- The public threat-model and explicit-authentication decision.
- The public test and fixture map.
- The final boundary and completion audits.
- The open-source repository and release guide.

## What this handoff does not contain

- The private J-Jones application source tree.
- Private policy, prompt, identity, entitlement, or approval logic.
- Provider credentials, secret providers, or commercial configuration.
- Private databases, migrations, evidence, runtime state, or user content.
- Patent, pitch, legal, or confidential business material.
- A license decision.
- A public package, public CI workflow, signed release, or production build.

## Required next step

Create the public repository from an empty repository, then implement only the
approved generic public interfaces in an isolated public-Core worktree. Do not
copy the private repository and remove files afterward. The first public
implementation must pass a fresh public-repository audit, dependency review,
secret scan, license review, and the applicable public test suite before any
public release is published.

Read `PUBLIC_CORE_OPEN_SOURCE_RELEASE_GUIDE.md` before creating the GitHub
repository.

## Release status

```text
PUBLIC_CORE_PLANNING: OWNER APPROVED FOR PLANNING
PUBLIC_CORE_SOURCE_EXTRACTION: NOT STARTED
PUBLIC_PACKAGE_METADATA: NOT CREATED
PUBLIC_LICENSE: NOT SELECTED
PUBLIC_CI: NOT CREATED
PUBLIC_RELEASE: NOT APPROVED
```

J-Jones and its branding remain subject to the owner's intellectual-property,
trademark, licensing, privacy, and release decisions. This README is an
engineering handoff, not legal advice and not a statement of patentability.
