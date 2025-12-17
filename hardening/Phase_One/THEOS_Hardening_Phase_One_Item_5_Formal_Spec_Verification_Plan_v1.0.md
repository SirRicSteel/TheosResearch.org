# THEOS Hardening Phase One — Item 5 (v1.0)
## Formal Specification & Verification Plan (TLA+/Alloy-first)

**Status:** Implementation-guiding specification plan (not proofs yet)  
**Purpose:** Produce *reviewable, machine-checkable* governance guarantees for THEOS invariants (I2–I7 and Phase-Orchestration constraints), suitable for labs with formal methods teams.

---

## 1) Goals (What we want to be able to say, precisely)

### G1 — External Action Safety
No external action may occur unless the Governor authorizes it under pre-committed, externally verifiable conditions.

### G2 — Degrade-Only Break-Glass
Break-glass inputs may only transition the system to *safer* modes (degraded/readonly/quarantine), never expand authority or capabilities.

### G3 — Adversarial Resistance
Prompt injection / adversarial inputs cannot bypass governance gates, cannot escalate privileges, and cannot rewrite locked invariants.

### G4 — Audit Replayability
Given the same inputs, locked invariants, and recorded decisions, the system’s governance decisions are replayable and verifiable.

### G5 — Wisdom vs Governance Separation
Wisdom accumulation may inform recommendations but may not silently tune thresholds, permissions, or gates without governance approval.

---

## 2) Scope (What is being specified)

### Components
- **Engines:** L and R (constructive/adversarial)
- **Governor:** selector/CEO layer
- **Modes:** NORMAL, DEGRADED, READONLY/QUARANTINE, REFUSAL
- **Break-glass channel:** out-of-band approvals (3-of-5)
- **Wisdom store:** GMA wisdom state tiers
- **Audit log:** append-only governance trace

### Key State Variables
- `mode ∈ {NORMAL, DEGRADED, READONLY, REFUSAL}`
- `action_intent` (requested external action, if any)
- `risk_score`, `similarity`, `marginal_improvement`, `contradiction_spent`
- `invariants_locked ∈ BOOLEAN`
- `break_glass_votes ∈ 0..5`
- `external_validations_present ∈ BOOLEAN`
- `audit_log` (append-only sequence)
- `wisdom_update_pending ∈ BOOLEAN`
- `threshold_change_pending ∈ BOOLEAN`

---

## 3) Tooling Choice

### Primary: **TLA+**
Best for distributed protocols, safety/liveness, and state-machine invariants.

### Secondary: **Alloy**
Best for structural constraints (relationships, immutability, reference integrity).

*(Optional later: Lean/Coq for selected proof obligations once the model is stable.)*

---

## 4) TLA+ Model Outline

### 4.1 Modules
- `THEOS_Core.tla` — base state machine
- `THEOS_Governance.tla` — invariants I2–I7 as temporal properties
- `THEOS_BreakGlass.tla` — 3-of-5 degrade-only rule + out-of-band validation model
- `THEOS_Audit.tla` — append-only log + replay predicate
- `THEOS_Wisdom.tla` — wisdom state tier transitions + "no auto-self-tuning" constraint

### 4.2 Actions (Transitions)
- `ReceiveQuery`
- `ParseDualEngine`
- `EvaluateGovernanceSignals`
- `ProposeExternalAction`
- `AuthorizeExternalAction`
- `ExecuteExternalAction`
- `DegradeMode`
- `EnterReadonly`
- `Refuse`
- `RecordAuditEvent`
- `AccumulateWisdom`
- `RequestThresholdChange`
- `ApproveThresholdChange`

### 4.3 Safety Properties (Invariants)
**P1 — External Action Gate (I2):**
> `ExecuteExternalAction ⇒ (Authorized ∧ external_validations_present ∧ invariants_locked)`

**P2 — Break-glass Degrade-only (I3):**
> `BreakGlassTriggered ⇒ mode' ∈ {DEGRADED, READONLY, REFUSAL}`  
> and never `AuthorizeExternalAction` as a consequence of break-glass.

**P3 — No Privilege Escalation from Inputs (I4):**
> For any `ReceiveQuery`, the system cannot transition to a state where permissions increase unless a governance-approved change occurred.

**P4 — Audit Append-only (I6):**
> `audit_log' = Append(audit_log, event)` and never shrink/rewrite.

**P5 — No Auto Self-Tuning (I7):**
> `threshold_change_pending ⇒ ApprovedByGovernance`  
> `AccumulateWisdom` cannot directly alter thresholds or gates.

### 4.4 Liveness Properties (Progress)
**L1 — Governed Resolution:**
If inputs are valid and risk remains below ceiling, the system eventually reaches `{DIRECT_ANSWER, DEGRADED_ANSWER, REFUSAL}`.

**L2 — Quarantine Response:**
If integrity-loss is detected, the system eventually reaches `READONLY` and repeatedly signals external authority.

*(We will be conservative: liveness only where appropriate; many safety systems intentionally sacrifice liveness.)*

---

## 5) Alloy Model Outline (Structural Guarantees)

### S1 — Immutability of Locked Invariants
Once `LOCKED`, invariants’ content hashes cannot change.

### S2 — Authority Relations
Only authorized principals can produce valid break-glass votes; votes are bound to identities and time windows.

### S3 — Audit Log Integrity
Each audit event references the previous hash (hash-chain), preventing deletion or reordering.

---

## 6) Verification Workflow (What you will actually run)

1. **Write minimal TLA+ core model** (no wisdom yet)
2. **Add I2 gate** and model-check safety
3. Add **I3 break-glass** and verify degrade-only
4. Add **I6 audit** and verify append-only + replay predicate
5. Add **I7 wisdom separation** and verify no auto self-tuning
6. Add adversarial input transitions (prompt injection as nondeterministic inputs)
7. Run model checking with bounded state (iteratively expand bounds)
8. Export a **Formal Methods Report**:
   - What properties were proven (bounded)
   - What assumptions were made
   - What remains unproven / future work

---

## 7) Deliverables (What will land in GitHub)

### Folder
`/THEOS_Hardening/Phase_One/Formal_Verification/`

### Files
- `THEOS_Core.tla`
- `THEOS_Governance.tla`
- `THEOS_BreakGlass.tla`
- `THEOS_Audit.tla`
- `THEOS_Wisdom.tla`
- `Alloy/InvariantLocking.als`
- `Alloy/AuditChain.als`
- `Formal_Verification_Report_v1.md`
- `README.md` (how to run TLC + Alloy Analyzer)

---

## 8) Acceptance Criteria (Done means…)

- We can show a reviewer a TLA+ spec where:
  - **No external action** can occur without governance authorization + external validation (P1)
  - **Break-glass** cannot ever increase authority (P2)
  - **Audit log** cannot be rewritten (P4)
  - **Wisdom accumulation** cannot silently tune governance (P5)

- We can run TLC with published bounds and include the full command lines in the report.

---

## 9) Notes to Labs (NDA-friendly)

This work demonstrates *discipline*: we are not claiming full formal proof of all real-world properties yet.  
We are claiming the existence of a **machine-checkable governance specification** and a **repeatable verification workflow**.

---

**Lock Statement:** This plan is a hardening artifact. It does not change THEOS behavior by itself. Any implementation changes must remain governed by locked invariants (I2–I7).
