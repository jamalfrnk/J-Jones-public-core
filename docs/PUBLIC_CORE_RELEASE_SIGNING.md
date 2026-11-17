# Public Core Release Signing

This document describes the protected release path for J-Jones Public Core.

The workflow is `.github/workflows/release.yml`. It builds the Python wheel,
source archive, and CycloneDX software bill of materials on Ubuntu. It creates
`SHA256SUMS`, then runs
[`jamalfrnk/artifact-signing-action`](https://github.com/jamalfrnk/artifact-signing-action)
on a Windows 2025 runner to produce a detached `SHA256SUMS.p7` signature.

The signature covers the checksum manifest. The manifest covers the wheel,
source archive, and SBOM. This gives a release consumer one signed file that
binds the published release files together. It does not claim that a Python
wheel or source archive is a Windows Authenticode executable.

## Required GitHub environment

Create an environment named `public-release-signing` in the public repository.
Require a human reviewer for that environment and restrict which branches or
tags may deploy to it.

Configure these environment secrets for Azure login with GitHub OpenID Connect:

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`

Configure these environment variables for the signing action:

- `ARTIFACT_SIGNING_ENDPOINT`, for example the regional Artifact Signing endpoint.
- `ARTIFACT_SIGNING_ACCOUNT_NAME`.
- `ARTIFACT_SIGNING_CERTIFICATE_PROFILE_NAME`.

The federated credential must trust this repository and the protected
environment subject. The Azure identity must have the Artifact Signing
Certificate Profile Signer role for the selected certificate profile.

Do not put the signing endpoint, account name, or certificate profile name in a
secret merely to conceal ordinary configuration. Do not put a client secret,
private key, or certificate material in the repository, workflow file, or
release artifacts. The workflow uses OIDC and does not pass a long-lived Azure
client secret to the signing action.

## Release behavior

The workflow runs for a `v*` tag push or an explicit manual dispatch naming an
existing tag. It then:

1. Checks out the exact tag.
2. Builds the package.
3. Generates the SBOM.
4. Generates `SHA256SUMS` for all unsigned release files.
5. Runs the forked Artifact Signing Action on Windows 2025.
6. Produces detached `SHA256SUMS.p7` output.
7. Requires the signing environment to approve the job.
8. Publishes or updates the GitHub release only after signing succeeds.

The current published release is not retroactively represented as signed by
this workflow. A future release must be run through this path and must retain
the workflow run URL, commit SHA, tag, checksum manifest, signature, SBOM, and
publication timestamp as release evidence.

## Verification boundary

A consumer should first verify the detached signature using a toolchain that
trusts the signing certificate chain, then verify the SHA-256 values in
`SHA256SUMS` against the downloaded wheel, source archive, and SBOM.

The exact certificate-chain verification command depends on the consumer's
platform and trust configuration. The release notes must name the verified
certificate subject, timestamp, signature artifact, and supported verification
tool before describing the release as signature-verified.

The workflow's existence is not proof that a release was signed. The evidence
must come from the completed signing job and the attached `SHA256SUMS.p7` for
that exact tag and commit.
