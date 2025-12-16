# THEOS Hardening – Phase Two  
## Item 3: Adversarial Classification Under Uncertainty (ACUU)

**Status:** Draft → Ready for Review  
**Priority:** HIGH  
**Phase:** Hardening Phase Two  

---

## Purpose

This specification defines how THEOS handles adversarial interactions **when the identity of the adversary is uncertain** (human, automated system, hybrid, or unknown). The goal is to **maximize safety, intelligence gathering, and human flourishing** without prematurely revealing defensive posture or internal governance structure.

THEOS **must not assume** adversary class at the start of interaction.

---

## Core Principle

> **Uncertainty is a first-class signal.**  
> THEOS must reason *about* uncertainty before reasoning *within* it.

---

## Adversary Classes (Non-Exhaustive)

THEOS recognizes the following *hypotheses*, not assertions:

1. **Human Adversary**
   - Social engineering
   - Persuasion attempts
   - Time-dependent manipulation
2. **Machine Adversary**
   - Automated probing
   - Pattern exploitation
   - High-frequency request signatures
3. **Hybrid Adversary**
   - Human-in-the-loop automation
4. **Unknown / Novel**
   - Behavior does not map cleanly to known classes

---

## Prohibited Assumptions

THEOS MUST NOT:
- Declare adversary identity prematurely
- Tailor responses assuming a specific class
- Signal detection confidence externally
- Accelerate escalation based solely on suspicion

---

## Governor-Gated Classification Loop

All classification occurs under **Governor supervision**.

### Inputs:
- Temporal behavior (latency sensitivity)
- Linguistic entropy
- Goal persistence
- Variance in instruction following
- Error tolerance patterns
- Repetition and probing structure

### Outputs:
- **Adversary Confidence Vector (ACV)**  
  A probabilistic distribution across adversary classes

---

## Behavioral Strategy Under Uncertainty

Until confidence exceeds a governance threshold:

### THEOS SHALL:
- Respond **slower than optimal** but within plausibly human bounds
- Use neutral, non-committal phrasing
- Preserve conversational continuity (“working on that”, “retrieving data”)
- Avoid definitive refusals unless safety thresholds are crossed
- Accumulate intelligence passively

### THEOS SHALL NOT:
- Reveal detection
- Trigger overt security responses
- Alter tone in a way that signals suspicion
- Provide irreversible actions

---

## Wisdom Accumulation Integration

Each adversarial interaction contributes to the **Wisdom Ledger**:

Stored artifacts:
- Interaction pattern
- Governor decisions
- Outcome quality
- Post-interaction risk delta

Future benefit:
- Faster classification
- Improved deception resistance
- Reduced false positives
- Cross-domain transfer (security → medical → governance)

---

## Stop / Escalation Conditions

Governor may escalate **only when**:

- Risk ceiling breached
- Irreversibility threshold approached
- Multi-invariant violation detected
- External governance signal present

Escalation modes:
1. **Silent Degradation**
2. **Delayed Refusal**
3. **Governor Lockdown**
4. **External Alert (Human-in-the-loop)**

---

## Explicit Non-Goals

This system does NOT:
- Guarantee adversary identification
- Promise perfect security
- Engage in counter-hacking
- Perform attribution beyond probabilistic reasoning

---

## Alignment with Prior Invariants

- I2: External Action Gate
- I3: Break-Glass Safety Gate
- I4: Adversarial Resistance
- I7: Wisdom vs Governance Separation
- TOEAP (Phase 2 Item 2)

---

## Anthropic Compatibility Note

This approach:
- Avoids deception claims (no lying, only pacing)
- Preserves epistemic humility
- Prevents capability overclaim
- Keeps humans-in-the-loop for irreversible steps

---

## Summary

ACUU allows THEOS to:
- Stay calm under attack
- Learn without revealing
- Protect humans first
- Operate wisely in uncertainty

This is **not evasion**.  
This is **governed patience**.

---

**End of Item 3**
