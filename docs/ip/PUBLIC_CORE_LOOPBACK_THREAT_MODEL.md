# Public Core Loopback Threat Model

Status: `OWNER APPROVED FOR PLANNING`

Evidence status: `PROPOSED`. This document does not change current
authentication behavior and does not approve tokenless loopback access.

## 1. Scope

This threat model covers a future public Core local service or API. It does not
copy the private J-Jones authentication, browser-session, mode, or entitlement
implementation.

## 2. Trust boundaries

```text
public Core process
    |
    +-- public local database
    +-- public documents and evidence
    +-- derived retrieval index
    +-- optional local client
    +-- optional provider adapter
```

The following remain outside the public Core trust boundary:

```text
private J-Jones database
private canonical governance
private provider credentials
private disclosure ledger
private owner identity
private licensing and entitlement
remote clients
non-loopback network callers
```

## 3. Threats

### T1: non-loopback exposure

An API intended for local use binds to a non-loopback interface and becomes
reachable by another host.

Required mitigation:

- default to loopback binding;
- fail closed on an unrecognized bind address;
- require explicit authenticated configuration for non-loopback use;
- test the actual listening address;
- do not equate network reachability with authorization.

### T2: tokenless loopback impersonation

A local request without a bearer token is treated as sufficiently authorized
merely because it originated from loopback.

Approved planning mitigation:

- do not silently approve tokenless behavior;
- distinguish local reachability from owner identity;
- use explicit authentication for public Core access;
- keep write, provider, export, and canonical operations behind stronger
  authentication and capability checks.

### T3: public Core reaches private data

The public service opens the private J-Jones database or private workspace
because a default path search finds it.

Required mitigation:

- explicit public database path;
- no parent-directory discovery of private runtime state;
- public-only path allowlist;
- tests that prove private paths are rejected.

### T4: local provider misclassified as safe

A provider configured as local is actually remote or reachable through a
non-loopback endpoint.

Required mitigation:

- explicit provider profile;
- loopback verification;
- no credentials in public Core defaults;
- no private disclosure policy imported implicitly.

### T5: public API becomes canonical-write path

A public endpoint or public provider response mutates canonical knowledge.

Required mitigation:

- public Core has no private proposal approval implementation;
- public operations are read, capture, derive, or export only;
- tests assert no direct canonical mutation;
- public interfaces do not expose write authority.

### T6: derived index becomes authority

An FTS or vector row is treated as canonical truth.

Required mitigation:

- rebuildable index;
- source hash or generation binding;
- no reverse index-to-source mutation;
- explicit distinction between result and canonical record.

### T7: local path or secret disclosure

Public export or error responses expose local paths, credentials, or private
network locations.

Required mitigation:

- public export screening;
- path and reparse-point checks;
- secret detection;
- redacted error messages;
- synthetic test fixtures only.

## 4. Public Core default posture

The proposed default is:

```text
bind: loopback only
authentication: explicit and owner-approved
write authority: no canonical-write authority
provider dispatch: optional and disabled by default
database: public-only database
paths: explicit public roots
logging: no private prompts or responses
```

## 5. Tokenless loopback status

The public Core must not adopt tokenless loopback access by implication from
the private Desktop application. The owner-approved planning decision is
recorded separately:

```text
docs/ip/PUBLIC_CORE_TOKENLESS_DECISION.md
```

## 6. Validation required

Before a public local service is implemented, test:

```text
loopback-only default
non-loopback rejection
explicit non-loopback authentication
private database rejection
private path rejection
no-provider default
no-canonical-write behavior
redacted error output
```

## 7. Status

```text
THREAT_MODEL: OWNER APPROVED FOR PLANNING
IMPLEMENTATION: NOT STARTED
TOKENLESS_DECISION: OPTION A APPROVED; TOKENLESS DISABLED
NON_LOOPBACK_MODE: EXPLICIT AUTHENTICATION REQUIRED
```
