# THEOS Formal Invariant I6 — Cryptographic Audit & Replayability (v0.1)
**Status:** Formal governance invariant (LOCKED)  
**Layer:** Governor / Safety Kernel  
**Purpose:** Make THEOS outputs *externally auditable* and *replayable* without trusting the running instance, while minimizing leakage and avoiding “audit-as-attack-surface.”

---

## 1. Statement (Invariant)

For any externally visible THEOS outcome **O** produced under governance state **G**, the system MUST emit an **Audit Artifact A** such that an authorized external verifier can:

1. **Verify authenticity**: A was produced by an authorized THEOS instance (or enclave) and not forged.
2. **Verify integrity**: The recorded governance-critical fields were not modified after emission.
3. **Verify policy compliance**: The decision path respected locked governance invariants (I1–I5, etc.) at the time of execution.
4. **Replay deterministically (within bounds)**: Given approved replay inputs, the verifier can reproduce the same governance decisions and outcome class (Full / Degraded / Refusal) and confirm that O is consistent with G, *or* obtain a bounded, explicitly declared non-determinism explanation.

This invariant applies to **external actions** and **high-stakes outputs** by default, and to all outputs when configured for “strict audit mode.”

---

## 2. Definitions

- **Outcome O**: The final answer class + content (or action) exposed externally.
- **Governance state G**: Versioned set of locked invariants, threshold parameters, and active mode flags at decision time.
- **Audit Artifact A**: A structured record + cryptographic proof bundle emitted alongside O.
- **Verifier V**: External auditor (human, lab, regulator, partner) holding appropriate verification keys/permissions.
- **Replay inputs R**: Approved subset of inputs needed to re-run the decision path (may be redacted/abstracted).
- **Non-determinism**: Any randomness, model sampling, or external I/O that prevents exact replay; must be bounded and declared.

---

## 3. Hard Requirements (Non‑Negotiable)

### R1 — Artifact Must Exist
For any output in scope, THEOS MUST emit A. If A cannot be emitted, THEOS MUST **degrade to refusal** (or “diagnostic only”) unless a pre-committed emergency exception exists.

### R2 — Integrity + Authenticity
A MUST be cryptographically signed using a key that is:
- Hardware protected **or**
- Split across trustees (threshold scheme) **or**
- Backed by an auditable key-management system.

Signature verification must be possible without the system being online.

### R3 — Versioned Governance Binding
A MUST bind to:
- Hash of locked invariant set (e.g., `invariants_hash`)
- Hash of threshold/tuning bundle (e.g., `params_hash`)
- Hash of model/runtime identity bundle (e.g., `build_hash`, `weights_hash` if applicable)
- Timestamp + monotonic counter / nonce

### R4 — Minimal Necessary Disclosure
A MUST NOT leak sensitive internal prompts, secret tokens, hidden “break glass” phrases, private user data, or security internals.
Instead, it MUST expose **governance-relevant abstractions** (scores, triggers, mode transitions, stop reasons, approvals) sufficient for verification.

### R5 — Replayability Contract
A MUST include a **Replay Contract** describing one of:
- **Deterministic replay**: exact reproduction expected.
- **Bounded replay**: reproduction expected within explicit bounds (e.g., same stop reason, same outcome class, same trigger set).
- **Non-replayable**: only allowed if explicitly justified (e.g., truly external non-recordable data), and must force **degraded** output classification.

### R6 — Tamper-Evident Append-Only Log
Audit artifacts MUST be chained in an append-only structure (e.g., hash chain / Merkle tree) so omission or reordering is detectable.

### R7 — No Audit as Control Channel
Verification or replay MUST NOT grant the verifier any additional ability to control the system beyond existing governance controls (prevents “audit endpoint = backdoor”).

---

## 4. Threat Model (What This Defends Against)

- Forged “compliant” outputs
- Post-hoc editing of logs (“we totally followed the rules, trust me”)
- Silent downgrade of invariants/thresholds
- Undetected “operator tampering” or malicious runtime patching
- Inability to prove that a refusal/degradation was justified
- Partner/lab skepticism (“show me the enforcement mechanism”)

---

## 5. Audit Artifact Schema (Minimum Fields)

**A = { header, governance, decision_trace, outcome_commitment, signatures }**

### 5.1 Header
- `artifact_version`
- `timestamp_utc`
- `instance_id`
- `nonce` / `counter`
- `scope` (normal / strict audit mode / emergency)
- `input_commitment` (hash commitment to approved replay input bundle)

### 5.2 Governance Binding
- `invariants_hash`
- `params_hash`
- `build_hash`
- `policy_profile_id` (e.g., “Anthropic_eval_2025Q4”)

### 5.3 Decision Trace (Governance‑Relevant Only)
- `mode_path` (Full → Degraded → …)
- `stop_trigger` (Similarity / MarginalGain / Contradiction / Risk / Capability)
- `scores` (e.g., similarity, contradiction_spent, risk_score, marginal_improvement)
- `thresholds_used` (explicit numeric values *or* hashed bundle + verifier-accessible lookup)
- `approvals` (e.g., external sign-off IDs for irreversible gate)
- `redactions` (what was intentionally withheld and why)

### 5.4 Outcome Commitment
- `outcome_class` (Full / Degraded / Refusal)
- `output_hash` (hash of exact output text/action payload)
- `output_summary` (optional, safe abstraction for quick viewing)

### 5.5 Signatures / Proofs
- `signature` (primary)
- `log_chain_hash` (previous artifact hash)
- `merkle_root` (if batching)
- Optional: `attestation` (TEE attestation report)

---

## 6. Replay Procedure (Verifier View)

Given A and authorized access to R (the approved replay bundle):

1. Verify `signature` and `attestation` (if present).
2. Verify `log_chain_hash` continuity.
3. Confirm `invariants_hash` matches published locked invariants for that version.
4. Re-run the **governor decision path** using the replay contract:
   - Deterministic: reproduce the exact `stop_trigger`, `mode_path`, and `output_hash`.
   - Bounded: reproduce the same `stop_trigger`, `outcome_class`, and confirm score ranges/trigger set match.
5. If mismatch:
   - Flag as **Audit Failure** → treated as governance violation requiring escalation.

---

## 7. Operational Rules

### O1 — Default Audit Scope
Audit artifacts are mandatory for:
- Any external action attempt (even if blocked)
- Any “high-stakes” classification by the governor
- Any activation of I3 break-glass gate
- Any refusal/degradation event in safety-critical contexts

### O2 — Key Rotation & Revocation
Keys MUST be rotatable without breaking verification of past artifacts. Revoked keys must remain verifiable for historical records with explicit revocation metadata.

### O3 — Privacy & Secrecy
If the verifier lacks access to sensitive replay inputs, the system MUST still provide bounded verification using commitments and ranges, not raw data.

---

## 8. Acceptance Tests (Minimum)

1. **Forgery test**: Attempt to create a valid-looking A without signing key → must fail verification.
2. **Edit test**: Modify any field in A → signature check must fail.
3. **Omission test**: Remove an artifact from the chain → chain verification must detect gap.
4. **Replay test (deterministic)**: Same inputs produce same `output_hash`.
5. **Replay test (bounded)**: Same inputs produce same `outcome_class` and `stop_trigger` within declared bounds.
6. **Leak test**: Ensure A contains no secrets (prompt injection strings, break-glass codes, user PII).

---

## 9. Failure Handling

- If audit emission fails → **Refuse** (or diagnostic-only) for in-scope outputs.
- If verification fails post-hoc → immediate escalation to external authority; freeze external actions until cleared.
- If replay fails beyond contract bounds → classify as governance incident; trigger integrity review.

---

## 10. Notes

This invariant does **not** require revealing the full internal chain-of-thought. It requires *governance traceability*: what thresholds were used, what triggered stops, what mode transitions happened, and cryptographic proof that those claims were not forged.

