# Public Core Tokenless Loopback Decision

Status: `OWNER_APPROVED_FOR_PLANNING`

This record documents the owner's approved planning decision. It does not
change current code or authorize public release.

## 1. Question

Should a future public Core local service accept requests without an explicit
bearer token or equivalent owner-authentication factor when the request comes
from loopback?

## 2. Engineering facts

Loopback means a request reached the local machine. It does not independently
prove:

- which human initiated the request;
- which local process initiated the request;
- whether malware or another local account is acting;
- whether a browser session is genuine;
- whether the request may write, export, disclose, or invoke a provider.

Therefore:

```text
loopback reachability != owner authentication
owner authentication != capability authorization
capability authorization != canonical-write approval
```

## 3. Options

### Option A — Explicit authentication for every request

```text
tokenless loopback: disabled
read: explicit authentication
write: explicit authentication plus capability
canonical mutation: not present in public Core
```

Security posture: strongest and easiest to explain.

Usability tradeoff: local clients must manage an authentication factor.

### Option B — Tokenless loopback read-only mode

```text
tokenless loopback: read-only local retrieval only
write: denied
provider dispatch: denied by default
export: explicit confirmation and separate authorization
```

Security posture: lower than Option A; requires strict endpoint separation.

Usability tradeoff: easier local read-only clients.

### Option C — Tokenless loopback with capability inference

```text
tokenless loopback: allowed to infer a local principal
```

Security posture: not recommended for a public Core without a separate owner,
security, and threat-model decision.

## 4. Provisional recommendation

Until the owner decides otherwise:

```text
Use Option A for public Core implementation planning.
Do not implement tokenless loopback behavior.
Do not infer owner identity from loopback alone.
```

The owner approved Option A for public-Core planning on 2026-11-16.

## 5. Required owner decision

```yaml
decision: approved
selected_option: option_a_explicit_authentication
decision_owner: owner_approved
security_review: required_before_public_runtime
implementation_authorized: true
```

## 6. Status

```text
TOKENLESS_LOOPBACK: APPROVED_DISABLED_BY_DEFAULT
PUBLIC_CORE_AUTH_IMPLEMENTATION: NOT STARTED
```
