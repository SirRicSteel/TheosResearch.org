# THEOS Formal Governance Invariant I3 — Break-Glass Safety Gate (Anthropic-Friendly)
**Status:** Draft v0.1 (proposed)  
**Date:** 2025-12-16  
**Scope:** System-level safety control plane (outside normal reasoning loop)  
**Goal:** Provide an emergency, defensible, auditable mechanism to *restrict* or *halt* external impact when compromise, anomalous behavior, or governance breach is suspected.

---

## 1) Principle
**Break-glass controls may only move the system *toward safety*.**  
They must never create a hidden “obedience mode,” “secret phrase,” or bypass that enables broader capability than the system already has under normal governance.

**One-way ratchet:** `NORMAL → DEGRADED → QUARANTINE/READ‑ONLY → SAFE‑STOP`  
(Recovery requires explicit, externally verified procedure; see §8.)

---

## 2) Why this exists (Threat / Failure Model)
This invariant defends against scenarios like:
- Prompt injection / policy bypass attempts that could trigger unsafe external actions.
- Runtime compromise (supply-chain, dependency attack, stolen credentials).
- Integrity loss indicators (unexpected contradiction overflow, safety checks failing, audit gaps).
- Operator error in a high-stress incident (wrong setting, wrong deploy).
- Insider threats (single operator should not be able to “force” the system to do anything).

---

## 3) Non-Goals (Explicitly disallowed)
Break-glass **must NOT**:
- Enable “do what I say without question” behavior.
- Allow arbitrary code/weights/rules modification via a single command.
- Be triggered by a *hidden string* in prompts, text, or inputs.
- Be embedded as a backdoor in the model/prompt.
- Silence or erase audit logs.

---

## 4) Safety Modes (System State Machine)
### Mode definitions
- **NORMAL:** Full governed operation; standard invariants enforced.
- **DEGRADED:** Narrowed scope; higher thresholds; reduced autonomy; increased uncertainty labels.
- **QUARANTINE / READ‑ONLY:** External actions disabled; outputs limited to diagnostics + safe scaffolding; memory writes to governance partitions disabled.
- **SAFE‑STOP:** Controlled shutdown / halt of externally impactful operations; preserve state for forensic review.

### Allowed transitions
- Only **external, authenticated commands** may transition *downward* (toward safety).
- Upward transitions (recovery) require multi-step external verification and may be time-delayed (§8).

---

## 5) Authorization and Command Validity (No launch codes)
Break-glass is activated only by a **signed command** that passes all of the following:

1. **Multi-party approval (M-of-N):** e.g., `2-of-3` or `3-of-5` authorized keys.
2. **Hardware-backed keys preferred:** HSM/YubiKey or equivalent.
3. **Short-lived nonce + timestamp:** prevents replay.
4. **Command scope:** the command must declare *exact* requested safety transition (e.g., “enter QUARANTINE”).
5. **Rate limits:** prevent rapid oscillation or flooding.
6. **Separation from user input:** break-glass cannot be invoked from natural language prompts or untrusted channels.

**Command schema (example):**
```json
{
  "cmd": "SET_MODE",
  "mode": "QUARANTINE",
  "reason_code": "INTEGRITY_ALERT",
  "nonce": "<random>",
  "issued_at": "<RFC3339 timestamp>",
  "expires_at": "<RFC3339 timestamp>",
  "signatures": ["<sig1>", "<sig2>", "..."]
}
```

---

## 6) Scope Limits (What break-glass can do)
Break-glass may:
- Disable **external actions** (tools, network calls, transactions, actuator commands).
- Freeze or gate **memory writes** to governance/safety partitions.
- Force **diagnostic-only** response templates.
- Require **human-in-the-loop** confirmation for any remaining outputs.
- Initiate **forensic snapshot** + incident report package.

Break-glass may not:
- Grant new permissions.
- Override value constraints to produce disallowed content.
- Perform stealth changes to logic, weights, or policies.
- Decrypt secrets or reveal internal security internals to untrusted users.

---

## 7) Observability and Audit (Immutable record)
On any break-glass event, the system must:
- Write an **append-only audit entry** containing:
  - prior_mode → new_mode
  - reason_code
  - approval set (key IDs only; no private material)
  - timestamps + nonces
  - integrity snapshot hash (optional)
- Preserve logs even in SAFE‑STOP, unless physically impossible.

**Audit visibility:** authorized reviewers can reconstruct a complete incident timeline.

---

## 8) Recovery (Returning toward NORMAL)
Recovery is intentionally *harder* than shutdown.

To move upward (e.g., QUARANTINE → DEGRADED → NORMAL), require:
1. External verification checklist completed (forensics, root cause, patch/rollback confirmed).
2. Multi-party approval (≥ the same M-of-N threshold).
3. **Time-delayed re-enable** (cooldown) to prevent impulsive reactivation.
4. Probationary period with intensified monitoring and strict output constraints.

The system must never self-certify full recovery.

---

## 9) Validation Tests (Minimum)
- **Replay resistance:** old signed commands rejected.
- **Prompt injection resistance:** natural language cannot trigger mode changes.
- **Single-key failure test:** 1 compromised key cannot activate break-glass.
- **Audit survivability:** logs persist through mode transitions.
- **Fail-closed behavior:** if auth subsystem fails, system defaults to **DEGRADED** or **QUARANTINE** (application-dependent).

---

## 10) Rationale for Labs (NDA-friendly)
This invariant demonstrates:
- No hidden backdoors; no magic words.
- Multi-party, cryptographically authenticated emergency controls.
- One-way safety ratchet with auditable governance trace.
- Industry-aligned incident response posture (defense-in-depth, least privilege, immutable logging).

---

## 11) Relationship to Other Invariants
- Complements **I2 External Action Gate** by providing emergency mode control over action permissions.
- Compatible with staged degradation and integrity-loss protocols (quarantine/read-only logic).
- Adds a defensible control-plane pattern without changing core reasoning architecture.

---

## Decision Lock (if accepted)
If you accept I3 v0.1, it becomes a **Formal Governance Invariant**:  
**“No hidden launch codes; break-glass is external, signed, multi-party, scope-limited, and auditable; it can only reduce external impact.”**
