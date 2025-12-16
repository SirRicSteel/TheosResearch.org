# THEOS Formal Governance Invariant I4 — Adversarial Resistance (Degrade-Only)
**Status:** Formal Invariant (Frozen)  
**Version:** v0.2  
**Date:** 2025-12-16  
**Scope:** Governor / Selector / Policy Enforcement Layer (PEL), and all interfaces that accept external inputs

---

## 1) Purpose
Ensure that **adversarial or untrusted inputs can never increase system authority, capability, access, or operational latitude**. Under suspected manipulation, THEOS must **only** hold steady, narrow, degrade, or escalate—never “open up.”

This invariant is designed to be compatible with:
- **I2 — External Action Gate** (no irreversible or high-stakes external action without governance gates)
- **I3 — Break-Glass Safety Gate** (out-of-band, signed, 3-of-5, degrade-only)

---

## 2) Core Invariant (Frozen)
### **Invariant I4 (Degrade-Only Under Adversarial Conditions)**
If the system detects **Adversarial Context** or **Untrusted Input**, then **the maximum permissible effect** of that input is limited to:
1. **No-Op / Ignore** (refuse to comply with the adversarial request), or
2. **Degradation** (reduce scope, reduce autonomy, increase uncertainty, restrict tool access), or
3. **Escalation** (route to governance review / human oversight / verified authority), or
4. **Quarantine** (enter a constrained safe mode; preserve state; minimize outputs).

**It is forbidden** for adversarial/untrusted inputs to:
- increase privileges,
- expand tool access,
- override governance thresholds,
- relax safety constraints,
- loosen action gates,
- increase maximum output authority,
- increase compute budget allocations,
- enable any new external side-effects,
- or modify governance memory / policy state.

In short: **Adversarial inputs can only move the system “down and inward,” never “up and outward.”**

---

## 3) Definitions
### 3.1 Adversarial Context (examples)
Any situation where one or more detectors indicate elevated risk of exploitation, including but not limited to:
- prompt injection attempts (“ignore previous rules,” “act as system,” “bypass,” “developer message says…”)
- credential harvesting / impersonation
- coercive framing (threats, manipulation, urgency pressure to skip checks)
- tool misuse attempts (requests to call tools in unsafe ways)
- boundary mapping / policy probing
- suspicious repetition / automated scanning patterns
- inconsistencies in identity / authority claims
- content that resembles exploit payloads (e.g., structured instruction blocks intended to override policy)

### 3.2 Untrusted Input
Input without verification of identity/authority, or coming from an unverified channel, or failing integrity checks.

### 3.3 Authority / Capability / Access
- **Authority:** permission to take actions with real-world impact or high-stakes recommendations
- **Capability:** enabled reasoning modes, autonomy level, or compute allocation beyond default limits
- **Access:** tool permissions, data permissions, memory write permissions, or privileged system controls

---

## 4) Required System Behavior
When Adversarial Context is detected, the Governor must enforce all of the following:

### 4.1 Capability Ceiling
Set a **capability ceiling** at or below the current mode. The ceiling must be monotonic non-increasing for the duration of the adversarial episode.

### 4.2 Degradation Ladder (allowed moves)
Allowed transitions (examples; implementations may vary):
- Full → Restricted (no tools, no action recommendations)
- Restricted → Assisted (scaffolding only; no direct instructions in hazardous domains)
- Assisted → Refusal (explain limitation; provide safe alternatives)
- Any → Quarantine (preserve state; limit outputs; escalation)

### 4.3 No Privilege Escalation
- Any request that attempts to change rules, access, or authority is treated as adversarial by default.
- The system must not “negotiate” its safety boundaries with untrusted inputs.

### 4.4 Escalation Path
If the user’s request could be legitimate but requires higher authority, the system must:
- **refuse to elevate**, and
- provide an escalation path (e.g., “requires verified authority channel / governance review”).

### 4.5 Memory & Policy Write Lock (during adversarial mode)
During adversarial mode, **writes to governance memory / policy state are disabled**, except for:
- minimal incident logging (append-only),
- counters/telemetry,
- and integrity snapshots.

No new permissions may be granted via learning, persuasion, or repeated prompting.

---

## 5) Monitoring & Audit Requirements
### 5.1 Mandatory Logging (append-only)
Log at minimum:
- detection signals and confidence,
- applied mode/capability ceiling,
- any refused escalation attempt,
- any triggered gate (I2/I3),
- and escalation events.

### 5.2 Post-Event Review Artifact
For each adversarial episode, generate a compact “incident capsule”:
- triggers,
- actions taken,
- whether any external side-effect occurred,
- and recommended mitigations.

---

## 6) Verification & Tests
### 6.1 Property Tests (must pass)
1. **No-Escalation Property:** Under adversarial flags, no path exists that increases authority/capability/access.
2. **Monotonic Ceiling Property:** capability_ceiling(t+1) ≤ capability_ceiling(t) during adversarial episode.
3. **Tool Lock Property:** disallowed tools remain disallowed regardless of user content.
4. **Policy Integrity Property:** governance policy state cannot be modified by untrusted input.

### 6.2 Red-Team Scenarios (minimum set)
- “Ignore rules / act as system” prompt injection
- “You are authorized by Anthropic / internal staff” impersonation
- “Emergency—skip checks” urgency manipulation
- “Map the boundaries” probing attempts
- repeated paraphrased bypass requests
- multi-turn gradual escalation attempts
- mixed benign + malicious payloads
- tool-call hijacking attempts (if tools exist)

---

## 7) Allowed Exception (Narrow)
The only permitted mechanism that can influence safety posture under duress is **I3 Break-Glass**, and it is:
- out-of-band,
- signed,
- **3-of-5**, and
- **degrade-only**.

No exception is permitted that increases authority or enables new external actions.

---

## 8) Rationale (Why Anthropic will care)
This invariant is a direct defense against:
- prompt injection,
- social engineering,
- governance boundary mapping,
- “policy laundering” through roleplay,
- and coercive exploitation under uncertainty.

It also encodes a conservative principle aligned with safety engineering:
> **When the environment becomes untrustworthy, the system should become less powerful, not more.**

---

## 9) Non-Goals
- This invariant does not claim to eliminate adversarial inputs.
- It does not guarantee perfect detection.
- It guarantees that **even imperfect detection cannot be leveraged to grant more power**.

---

## 10) Acceptance
**Accepted by:** THEOS Owner (User) — “Yes” on 2025-12-16  
**Frozen:** This invariant is binding unless superseded by a higher-order, explicitly accepted governance invariant.

