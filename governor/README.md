# THEOS Governor — Technical Specification

This folder contains the complete technical specification for the THEOS Governor, the core runtime governance mechanism that constrains, allocates, and audits AI reasoning.

---

## What the THEOS Governor Is

The THEOS Governor is a **deterministic, stateful control layer** that wraps AI systems to enforce:
- **Bounded reasoning** (depth, energy, tool use)
- **Posture-based escalation** (Normal → Probation → Containment → Isolation)
- **Delayed, auditable adaptation** (wisdom accumulation without observable learning)
- **Capability gating** by deployment mode
- **Enforceable suspension** and lifecycle controls

---

## How It Differs From Alignment/Training

| Aspect | Training-Based Alignment | THEOS Governor |
|--------|-------------------------|----------------|
| **When** | Pre-deployment (RLHF, Constitutional AI) | Runtime (every query) |
| **What** | Shapes model preferences | Constrains reasoning depth & energy |
| **How** | Modifies weights | Wraps model, preserves weights |
| **Auditability** | Opaque (gradient-based) | Transparent (deterministic state machine) |
| **Reversibility** | Requires retraining | Configuration change |

**THEOS is complementary, not competitive.** It governs *how much* intelligence is applied, not *what* the intelligence prefers.

---

## How to Evaluate Compliance

A THEOS-compliant system must:
1. **Enforce all formal invariants** (I1-I8) — see [`/governance/THEOS_Formal_Invariants.md`](../governance/THEOS_Formal_Invariants.md)
2. **Implement the reference mechanism** (v1.2, v1.3, v1.4) — documented in this folder
3. **Pass the worked example** — reproduce the session trace in v1.4
4. **Provide audit logs** — all posture transitions, depth allocations, and wisdom updates must be logged

---

## Documents in This Folder

### Core Specifications (Read in Order)

1. **[v1.2 — Formal Rigor](THEOS_Governor_Reference_Mechanism_v1.2_Formal_Rigor.md)**  
   Mathematical definitions, state variables, and core algorithms

2. **[v1.3 — Safety Envelope Presets](THEOS_Governor_Reference_Mechanism_v1.3_Safety_Envelope_Presets.md)**  
   Deployment mode configurations (Sandbox, Restricted, Operational, High-Assurance)

3. **[v1.4 — Worked Example Session Trace](THEOS_Governor_Reference_Mechanism_v1.4_Worked_Example_Session_Trace.md)**  
   Step-by-step numerical example showing wisdom accumulation and posture escalation

### Reference Implementation

4. **[`reference_impl/`](reference_impl/)**  
   Executable Python code that reproduces the v1.4 worked example  
   See [`reference_impl/README.md`](reference_impl/README.md) for usage

---

## Key Concepts

### Cumulative Wisdom (W_u)
The Governor accumulates **consequence-based wisdom** from past interactions:
- **Not preferences** (what the AI likes)
- **Not training** (modifying weights)
- **Auditable wisdom state** of what caused harm, with temporal decay

### Posture Transitions
```
Normal (NOM) → Probation (PEM) → Containment (CM) → Isolation (ISO)
```
Each posture reduces depth budget, verbosity, and tool access.

### Safety Envelopes
All hyperparameters are **bounded** to prevent:
- Accidental misconfiguration
- Adversarial parameter tuning
- Optimization into danger

---

## For Engineers

**To evaluate THEOS:**
1. Read v1.2 (formal spec)
2. Read v1.3 (deployment presets)
3. Run the reference implementation (`reference_impl/`)
4. Verify the numbers match v1.4

**To integrate THEOS:**
1. Wrap your model's inference endpoint
2. Implement the state machine from v1.2
3. Use presets from v1.3 for your deployment mode
4. Log all state transitions for audit

---

## For Researchers

**Novel contributions:**
- **Cumulative wisdom without observable adaptation** (prevents adversarial learning)
- **Temporal decay with context-specific λ** (prevents stale wisdom from dominating)
- **Safety envelopes with bounded hyperparameters** (prevents misconfiguration)
- **Posture-based escalation** (graceful degradation under threat)

**Comparison to prior work:**  
See [`/research/THEOS_Phase_Zero_Comparative_Positioning_v1.0.md`](../research/THEOS_Phase_Zero_Comparative_Positioning_v1.0.md)

---

## Status

**Specification:** Complete (v1.2, v1.3, v1.4)  
**Reference Implementation:** Available (Python, zero dependencies)  
**Hardening:** In progress (see [`/hardening/`](../hardening/))  
**Deployment:** Awaiting pilot partners

---

**For questions or collaboration inquiries, see [`/outreach/`](../outreach/).**
