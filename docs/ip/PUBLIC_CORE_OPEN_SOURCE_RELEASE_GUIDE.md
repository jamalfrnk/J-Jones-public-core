# J-Jones Public Core: Open-Source Repository and Release Guide

This guide is the operational checklist for turning the approved public-Core
boundary into a separate GitHub repository. The public repository must be
created from an empty repository and populated only with independently
reviewed public implementation files.

The current ZIP is a planning handoff. It does not prove that public source
has been extracted, that the proposed interfaces are implemented, or that a
release is legally or technically ready.

## 1. Use the release states precisely

1. **Planning approved** — the owner approved the documented boundary and
   implementation direction.
2. **Source extraction in progress** — public source is being rebuilt or
   extracted in an isolated public worktree.
3. **Public candidate** — a repository exists, but release gates are open.
4. **Release candidate** — a specific commit passed the source, test,
   security, dependency, license, documentation, and provenance gates.
5. **Published release** — the owner intentionally published a tagged GitHub
   release after the release-candidate review.

The present handoff is state 1. Do not describe it as state 4 or 5.

## 2. Patent and intellectual-property stop gate

Before making the repository public, obtain a written owner/counsel decision
covering:

- whether any public source or documentation would disclose a patent-sensitive
  mechanism, implementation detail, sequence, data structure, policy,
  governance rule, or knowledge-base method that should remain private;
- whether the public interfaces are generic enough to avoid publishing the
  protected implementation while remaining useful;
- whether public documentation must omit details beyond generic contracts and
  observable behavior;
- whether the J-Jones name, logo, product name, and repository title may be
  used publicly and in which jurisdictions;
- whether third-party code, documentation, datasets, model output, fonts,
  images, or examples have rights compatible with public redistribution; and
- whether the release includes cryptography, export-controlled functionality,
  regulated data examples, or other special review topics.

Do not backdate a filing, commit, tag, or release. Preserve actual engineering
history and record the real public-disclosure date.

## 3. Create the repository from an empty starting point

Do not make the private repository public. A new empty repository prevents
private history, deleted files, ignored files, object recovery, and accidental
configuration from entering the public repository.

Recommended identity:

    Name:        J-Jones
    Title:       J-Jones Public Core
    Visibility:  Public only after the IP and privacy stop gates pass
    Description: Public, local-first building blocks for governed knowledge
                 continuity: deterministic notes, evidence integrity,
                 rebuildable indexes, provider-neutral interfaces, and screened
                 exports.

If J-Jones is unavailable, use an owner-approved name such as
J-Jones-public-core. Do not use a second name to avoid an unresolved trademark
or ownership question.

On GitHub:

1. Open New repository.
2. Select the correct owner account or organization.
3. Enter the approved name and description.
4. Choose Public only after the IP and privacy stop gates pass.
5. For a local import, do not initialize with a README, gitignore, or license
   if those files will be added locally; this keeps the first commit reviewable.
6. Keep the repository owner, administrators, branch settings, and billing
   account under owner control.

## 4. Build the public repository in a clean directory

Create a new directory outside the private checkout. For example, in
PowerShell:

    New-Item -ItemType Directory -Path C:\Users\malcf\Code\J-Jones-public-core -Force
    Set-Location C:\Users\malcf\Code\J-Jones-public-core
    git init -b main

Copy only files explicitly classified for the public Core. Prefer rebuilding a
small public package from generic interfaces over copying private modules and
deleting what looks sensitive. The public package needs its own:

- package metadata, version, dependencies, and lock policy;
- database/schema and migration chain;
- tests and synthetic fixtures;
- CI workflows;
- documentation and security policy;
- contribution process; and
- release and provenance process.

Do not copy private runtime databases, evidence, logs, credentials, ignored
files, build caches, virtual environments, installer artifacts, private
workflows, or private migration history.

## 5. Required first-commit contents

After implementation begins, the candidate public tree should contain these
reviewed files or directories:

    README.md
    LICENSE
    CONTRIBUTING.md
    CODE_OF_CONDUCT.md
    SECURITY.md
    CITATION.cff
    CHANGELOG.md
    docs/
    src/
    tests/
    schemas/
    migrations/
    pyproject.toml
    uv.lock
    .gitignore
    .github/ISSUE_TEMPLATE/
    .github/workflows/
    .github/pull_request_template.md

LICENSE is added only after the license decision. CITATION.cff is optional.
The README must state actual implementation status, supported platforms,
installation method, data boundaries, non-goals, security limitations,
license, contribution route, and vulnerability-reporting route. Write it from
the public contract; do not copy a private product README and delete a few
paragraphs.

## 6. License and copyright clearinghouse

Do not select a license by habit. The license interacts with patent,
trademark, contribution, commercial, and derivative-work strategy.

The owner and counsel should decide:

- source-code license;
- documentation license, if different;
- example/data license, if examples are included;
- treatment of generated files and build artifacts;
- contributor copyright and inbound-rights policy;
- Developer Certificate of Origin versus contributor license agreement;
- trademark and logo usage rules; and
- whether a patent notice or defensive-publication notice is appropriate.

If an OSI-approved license is selected, record its exact SPDX identifier and
include the complete license text. Do not call a custom license open source or
OSI-approved. Apache-2.0, MIT, BSD-3-Clause, and MPL-2.0 are examples of
OSI-listed licenses, but this guide does not select one for J-Jones. Counsel
should review patent grants, attribution and notice requirements, reciprocity,
and commercial-use implications.

After the decision:

1. Add the complete license text at the repository root.
2. Add the correct SPDX identifier to source and documentation where
   appropriate.
3. Record copyright ownership and year accurately.
4. Add third-party notices and a dependency-license inventory.
5. Verify every bundled asset and example has compatible rights.
6. Run a license scanner and review every finding manually.

SPDX identifiers are machine-readable labels; they do not replace the actual
license text or a rights review.

## 7. GitHub community and governance files

Create and review:

- README.md — what the project is and is not.
- CONTRIBUTING.md — setup, tests, style, issues, and review rules.
- CODE_OF_CONDUCT.md — an owner-approved standard.
- SECURITY.md — supported versions, private reporting route, response
  expectations, and what reporters must not disclose publicly.
- CITATION.cff — project citation metadata, if useful.
- CHANGELOG.md — user-visible changes with accurate dates.
- pull-request template — scope, tests, security/privacy impact, and evidence.
- issue forms/templates — bug reports that prohibit secrets and private data.
- SUPPORT.md — support channels and boundaries.
- GOVERNANCE.md — only if the project has multiple maintainers or a formal
  decision process.

GitHub's public-repository community profile checks for common health files
such as README, license, code of conduct, and contribution guidance. A green
checklist is not a legal or security approval.

## 8. Security and supply-chain setup

Before the first public release:

1. Enable dependency graph and Dependabot alerts/updates where appropriate.
2. Enable secret scanning and push protection if available.
3. Enable code scanning, such as CodeQL, for the public languages.
4. Add dependency review to pull requests and define an owner-approved failure
   policy for vulnerable packages and disallowed licenses.
5. Pin third-party GitHub Actions to reviewed commit SHAs where practical.
6. Set workflow token permissions to the minimum required, normally read-only.
7. Require pull-request review and status checks on the default branch.
8. Add format, lint, type, unit, integration, migration, privacy-boundary,
   dependency, license, and secret-scanning checks to CI.
9. Run OpenSSF Scorecard; fix high-risk findings or document an owner-approved
   exception.
10. Generate an SBOM for the release and retain it with release evidence.
11. Produce checksums for every release asset.
12. Sign release artifacts if the release process supports it, and document
    signature verification.

A security scan is evidence about a scanned commit and tool configuration; it
is not a permanent claim that the repository is secure.

## 9. Public-data and privacy gate

The repository must contain only synthetic or intentionally public content.
Verify that it contains no user notes, professional knowledge, canonical
private content, raw evidence, provider responses, logs, telemetry, secrets,
private hostnames, local paths, tenant identifiers, internal URLs, commercial
settings, private prompts, policy rules, identity rules, entitlement rules,
approval thresholds, private databases, migration history, indexes, embeddings,
caches, or unreviewed media and datasets.

Use disposable synthetic fixtures. Run secret scanning on the complete Git
history and on the release ZIP, not only on the current working tree.

## 10. Public implementation and test gate

The public Core must make these boundaries visible in code and tests:

- model output does not silently change canonical knowledge;
- provider responses are noncanonical outputs;
- indexes and caches are rebuildable and are not canonical truth;
- untrusted content is data, not privileged instruction;
- public exports are screened and do not grant private authority;
- explicit authentication is required for public runtime access;
- external inference is not implied by a local-only claim;
- malformed or ambiguous input fails closed;
- public storage and migrations do not import private ORM or policy modules;
- public tests do not require private credentials or private services.

Run the public test suite from a clean clone with no access to the private
checkout. A test that passes only because private modules are importable is
not a public-Core test.

## 11. Versioning and the public release date

Use a release-candidate process:

1. Select a version such as 0.1.0-alpha.1 for an early public preview.
2. Freeze the candidate commit.
3. Run complete public checks on that exact commit.
4. Review the complete diff and Git history for private material.
5. Generate the SBOM, checksums, and release notes.
6. Create an attributable tag such as v0.1.0-alpha.1.
7. Draft the GitHub release from that tag.
8. Attach source archives, package artifacts, SBOM, checksums, and
   verification instructions.
9. Review release notes for private or patent-sensitive disclosure.
10. Obtain final owner publication approval.
11. Publish the release.

The public release date is the actual date and time the GitHub release becomes
public. Repository creation date, commit date, tag date, and release date are
distinct records. Record them separately. Never backdate or preannounce a
date as completed.

GitHub provides source ZIP and tarball links for a tag, but project-specific
release assets still need checksums, an SBOM, and verification instructions
when those artifacts are part of the release contract.

## 12. Uploading the prepared public tree

After source extraction and review, from the clean public directory:

    git status --short
    git add --all
    git diff --cached --check
    git commit -m "Initial J-Jones Public Core release candidate"
    git remote add origin https://github.com/OWNER/REPOSITORY.git
    git push -u origin main

Replace OWNER and REPOSITORY only after confirming the repository owner and
name. Never paste a token into a command, URL, README, issue, or release note.
Use GitHub's credential manager or browser login.

Immediately after pushing:

    git ls-files
    git log --oneline --decorate -n 5
    git tag --list

Compare the remote file list with the approved public manifest. Stop if an
unexpected file, private path, secret, binary, or dependency appears.

## 13. Release evidence packet

Retain an owner-controlled packet containing:

    release version
    commit SHA
    tag name and tag SHA
    GitHub release URL
    actual publication timestamp
    source archive SHA-256
    package artifact SHA-256 values
    SBOM and its SHA-256
    test and security check results
    license and third-party notice review
    IP/privacy approval record
    known limitations
    rollback or withdrawal contact

The packet should contain metadata and hashes, not private user data, full
private prompts, provider responses, credentials, or confidential legal
material.

## 14. Final go/no-go checklist

Do not publish until every applicable item is PASS or has an explicit
owner-approved exception:

    [ ] IP/patent disclosure gate passed
    [ ] trademark and branding gate passed
    [ ] public source manifest approved
    [ ] private-history and private-artifact audit passed
    [ ] public license selected and reviewed
    [ ] third-party notices complete
    [ ] README and public documentation accurate
    [ ] security policy and reporting route active
    [ ] dependency graph and vulnerability alerts enabled
    [ ] secret scanning and push protection enabled
    [ ] code scanning configured
    [ ] dependency review configured
    [ ] branch protection and review rules active
    [ ] public tests pass from a clean clone
    [ ] package/build smoke test passes
    [ ] public privacy and provider-boundary tests pass
    [ ] SBOM generated
    [ ] release checksums generated
    [ ] release signature/provenance documented
    [ ] release notes reviewed for private disclosure
    [ ] actual public release date recorded after publication
    [ ] owner gave final publication approval

## 15. Current handoff status

    PLANNING_BOUNDARY: OWNER APPROVED FOR PLANNING
    PUBLIC_SOURCE_EXTRACTION: NOT STARTED
    PUBLIC_REPOSITORY: NOT CREATED
    LICENSE: NOT SELECTED
    PUBLIC_CI: NOT CREATED
    RELEASE_CANDIDATE: NOT CREATED
    PUBLIC_RELEASE_DATE: NOT SET
    PUBLIC_RELEASE: NOT APPROVED

This status prevents a planning ZIP from being mistaken for an implemented
public release.
