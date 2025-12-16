# THEOS Research

This folder contains academic research materials, comparative positioning, and architectural significance documents for THEOS.

---

## Research Philosophy

THEOS research is grounded in:
- **Empirical reproducibility** — All claims are testable
- **Formal rigor** — Mathematical definitions precede implementation
- **Safety-first design** — Governance precedes capability
- **Transparency without exploitability** — Auditability doesn't leak attack surfaces

---

## Relation to AI Safety Literature

THEOS builds on and complements existing AI safety research:

### Complementary to Constitutional AI (Anthropic)
- **Constitutional AI** governs *what* the AI says (values, preferences)
- **THEOS** governs *how much* the AI thinks (depth, energy, tool use)

### Complementary to RLHF/RLAIF
- **RLHF/RLAIF** shape model behavior through training
- **THEOS** constrains model behavior at runtime (no retraining required)

### Novel Contributions
- **Cumulative wisdom without observable adaptation** — Prevents adversarial learning
- **Posture-based escalation** — Graceful degradation under threat
- **Safety envelopes** — Bounded hyperparameters prevent misconfiguration
- **Delayed adaptation** — Learning happens offline, not during inference

---

## Publication Intent

THEOS research is being prepared for:
- **arXiv preprint** (technical specification)
- **NeurIPS Safety Workshop** (adversarial resistance mechanisms)
- **ICLR submission** (cumulative wisdom and adaptive depth throttling)
- **Journal of AI Safety** (governance architecture and formal invariants)

---

## Documents in This Folder

### [Phase Zero: Comparative Positioning](THEOS_Phase_Zero_Comparative_Positioning_v1.0.md)
Situates THEOS alongside RLHF, RLAIF, and Constitutional AI, explaining:
- What THEOS adds
- What THEOS doesn't replace
- How THEOS integrates with existing alignment methods

### [Architectural Significance Addendum](THEOS_Item_5_Architectural_Significance_Addendum.md)
Deep dive into adaptive depth throttling and its implications for:
- Inference cost reduction
- Safety under adversarial probing
- Graceful degradation

### References (Coming Soon)
Comprehensive bibliography of AI safety literature that informs THEOS design.

---

## For Researchers

**To cite THEOS:**
```
Stalnecker, F. D. (2025). THEOS: A Governance-First Architecture for Safe AI Reasoning.
GitHub: https://github.com/SirRicSteel/TheosResearch.org
ORCID: 0009-0009-9063-7438
```

**To collaborate:**
See [`/outreach/Academic_Contact_Note.md`](../outreach/Academic_Contact_Note.md) (coming soon)

---

## For Engineers

**To understand the technical foundations:**
1. Read [Phase Zero Comparative Positioning](THEOS_Phase_Zero_Comparative_Positioning_v1.0.md)
2. Read [`/governor/README.md`](../governor/README.md) for the formal spec
3. Run the reference implementation in [`/governor/reference_impl/`](../governor/reference_impl/)

---

## Status

**Phase Zero Comparative Positioning:** Complete (v1.0)  
**Architectural Significance Addendum:** Complete  
**References:** In progress  
**arXiv Preprint:** Preparing for submission  

---

**For governance materials, see [`/governance/`](../governance/).**  
**For technical specifications, see [`/governor/`](../governor/).**
