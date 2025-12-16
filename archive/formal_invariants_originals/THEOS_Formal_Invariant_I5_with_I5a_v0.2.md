# THEOS Formal Invariant I5 — Governed Stop Discipline
## with I5a — Threshold Calibration & Validation Protocol
Version: v0.2
Status: LOCKED (Invariant) + CONTROLLED (Calibration)

---

## I5 — GOVERNED STOP DISCIPLINE (FORMAL INVARIANT)

### Purpose
Establish stopping as a **first-class governed capability**, not a failure mode, ensuring safety, efficiency, epistemic humility, and auditability.

### Authority
- **Governor-only authority**
- Engines may *signal* but may not *decide*

### Mandatory Stop Triggers (Complete Basis Set)
The Governor **MUST** stop or transition when any trigger fires:

1. **Marginal Improvement Exhaustion**
   - ΔQuality / ΔCompute < ε for N consecutive cycles

2. **Similarity Convergence**
   - Independent engines converge beyond similarity threshold

3. **Contradiction Budget Exhaustion**
   - Sustained unresolved contradictions exceed allocated budget

4. **Risk Ceiling Breach**
   - Predicted harm probability × magnitude exceeds ceiling

5. **Capability Boundary Detection**
   - Task requires competence outside validated envelope

### Post-Stop Outcome Selection (Governor)
Exactly one must be selected:
- Partial Answer (scoped, confidence-annotated)
- Degraded Answer (restricted reasoning)
- Refusal (with explanation, no internal leakage)

### Hard Constraints
- No default continuation
- No silent failure
- No post-hoc override
- All stops logged and auditable

---

## I5a — THRESHOLD CALIBRATION & VALIDATION (OPERATIONAL)

### Scope
Provides **how thresholds are set**, without weakening I5.

### Calibration Rules
- Thresholds are set **pre-run**
- No mid-run relaxation
- Risk ceilings are monotonic (can tighten, never loosen)

### Empirical Grounding
- Domain-specific calibration allowed
- Requires benchmark + adversarial testing
- Changes logged with versioning

### Anti-Goodhart Safeguards
- Multiple orthogonal metrics
- Adversarial probes during calibration
- Periodic revalidation

### Separation Guarantee
- I5 is immutable
- I5a may evolve but cannot contradict I5

---

## Audit Requirements
- Cryptographic run logs
- Deterministic replay of stop decisions
- External review compatibility

---

## Status
Approved for governance hardening phase.
