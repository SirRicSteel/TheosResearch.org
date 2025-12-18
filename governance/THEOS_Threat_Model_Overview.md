# THEOS — Threat Model Overview

## Addressed Threats

### Adversarial Probing
Mitigated via posture escalation and non-signaling throttles.

### Gradient / Feedback Extraction
Blocked by delayed, non-observable adaptation.

### Slow-Roll Manipulation
Countered by cumulative wisdom with long half-lives for harm. THEOS uses **functional time** to enable consequence-based learning without exposing exploitable memory or requiring recursive refinement.

### Memory Poisoning
Prevented by bounded wisdom state and offline validation.

### Silent Governance Drift
Prevented by configuration integrity and audit logs.

## Explicit Tradeoff
False positives are preferred to false negatives under safety stress.
