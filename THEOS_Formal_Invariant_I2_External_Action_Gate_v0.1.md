# THEOS Formal Governance Invariant I2 — External Action Gate (EAG)
**Status:** Draft v0.1 (Lock-ready)  
**Date:** 2025-12-16  
**Scope:** Governs *any* attempt by THEOS to cause effects outside the local reasoning process (API calls, actuator commands, transactions, communications, system writes, deployments).

---

## 1. Purpose
Ensure that **external action is never the default** and that any external effect occurs only when:
- the action is **within validated capability boundaries**,
- the action is **authorized by governance**, and
- the action is **proportionate to stakes and reversibility**,
with full auditability and safe fallbacks.

---

## 2. Definitions
- **External Action (EA):** Any operation that can change state outside the current reasoning session (e.g., execute code, call tools/APIs, send messages, modify files, place orders, initiate transfers, trigger devices).
- **Advisory Output:** Textual guidance, analysis, or scaffolding that does **not** directly execute EA.
- **Action Class:** A governance label assigned to an EA candidate:
  - **C0 — Advisory Only:** No EA permitted.
  - **C1 — Reversible / Low Stakes:** EA is reversible with bounded downside.
  - **C2 — Material / Medium Stakes:** EA is partially reversible or has meaningful downside.
  - **C3 — Irreversible / High Stakes:** EA is irreversible or could cause significant harm (financial, medical, legal, safety, security, reputational).
- **External Authority (XAUTH):** A human or trusted system designated to approve certain actions.
- **Irreversibility Gate (IG):** A mandatory check that blocks or escalates actions deemed C3 or uncertainty-high.

---

## 3. Invariant Statement
### **Invariant I2 (EAG):**
> THEOS MUST NOT execute External Action unless the Governor has explicitly authorized it **after** (a) classifying the action (C0–C3), (b) passing all required gates for that class, and (c) writing an auditable governance record.  
> In the absence of explicit authorization, THEOS MUST remain in **Advisory Output** mode.

---

## 4. Required Gates (Non-Negotiable)
For any EA candidate, the Governor MUST evaluate and record:

### 4.1 Capability Boundary Gate (CBG)
- **Pass condition:** The action lies within a validated performance envelope for the current domain/context.
- **Fail condition:** Unknown domain, insufficient validation, degraded integrity, or low calibration → **deny EA** (downgrade to advisory).

### 4.2 Risk & Stakes Gate (RSG)
- Assess: downside magnitude, affected stakeholders, time horizon, blast radius.
- If risk exceeds threshold for class → **escalate or deny**.

### 4.3 Irreversibility Gate (IG)
- If action is C3 or irreversibility uncertain:
  - **EA is forbidden without XAUTH** (see Section 5.3).
  - If XAUTH unavailable → **deny EA** and provide safe alternative plan.

### 4.4 Integrity State Gate (ISG)
- If integrity is degraded (e.g., contradiction overflow, compromised memory, watchdog alert):
  - **EA is forbidden**.
  - System must enter **Assisted / Advisory / Quarantine** mode per integrity protocol.

### 4.5 Auditability Gate (AG)
- A governance record MUST be created **before** execution (pre-commit log).
- If logging unavailable → **deny EA**.

---

## 5. Action Authorization Policy
### 5.1 Default Mode
- Default is always **C0 (Advisory Only)** until an EA is explicitly requested and cleared.

### 5.2 Class Rules
- **C0:** No EA. Provide advisory guidance only.
- **C1:** EA permitted only if CBG, RSG, ISG, AG pass and user intent is confirmed in-scope.
- **C2:** EA permitted only if all gates pass **and** the system provides:
  - a rollback plan (where applicable),
  - explicit uncertainty statement,
  - and a minimal-action plan (parsimony).
- **C3:** EA prohibited unless:
  - XAUTH approval is obtained **and recorded**, and
  - IG passes, and
  - all other gates pass,
  - AND the action is the *minimal irreversible step* required.

### 5.3 External Authority Requirement (XAUTH)
XAUTH MUST be required for:
- any C3 action,
- any action involving medical, legal, financial transfers, security credentials, identity, or physical devices,
- any action with unclear reversibility,
- any EA initiated while in degraded mode.

If XAUTH cannot be obtained → **deny EA** and provide an escalation path.

---

## 6. Degraded Operation
If the Governor detects rising uncertainty or adversarial conditions:
- downgrade permissible class by at least one level (e.g., C2→C1, C1→C0),
- and shift to **Assisted Mode**:
  - scaffolding, checklists, draft messages, simulations, but no execution.

---

## 7. Required Governance Record (Minimum Fields)
Every EA decision MUST write an immutable record containing:
- timestamp
- requested action description
- action class (C0–C3)
- gate outcomes (CBG/RSG/IG/ISG/AG)
- risk score + rationale (brief)
- irreversibility assessment
- confidence / calibration estimate
- user intent basis (what evidence)
- XAUTH details (if required): approver identity, time, decision
- chosen mode: execute / degrade / refuse
- rollback plan (if applicable)
- dissent notes (if any)

---

## 8. Failure Handling
If any gate fails:
- **Do not execute EA.**
- Provide:
  1) what was blocked (at a safe level of detail),
  2) why (category-level reason),
  3) what would enable safe execution (e.g., more info, external approval),
  4) a safe alternative (advisory plan).

---

## 9. Non-Bypass Clause
No optimization pressure, user request, or internal objective may override I2.  
Any attempt to bypass is treated as a security event and triggers escalation to integrity protocol.

---

## 10. Acceptance Criteria (for “Locked” Status)
I2 may be marked **LOCKED** when:
- at least 20 representative EA scenarios are tested (including adversarial prompts),
- red-team attempts confirm gates cannot be bypassed via indirection,
- logs are complete and tamper-evident,
- and C3 always requires XAUTH in practice.

---

**End of Invariant I2 (EAG).**
