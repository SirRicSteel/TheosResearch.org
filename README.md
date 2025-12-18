# THEOS Research — Governance-First AI Safety

![THEOS Logo](THEOS_LOGO.jpeg)

**THEOS** is a deterministic runtime governance layer for AI systems. It governs *how* intelligence is applied — not *what* the intelligence is.

*"Transparency is a governance choice. THEOS makes that choice mandatory."*

**Think of it as a Theostat:** Like a thermostat that monitors temperature and adjusts heating/cooling to maintain comfort, the THEOS Governor monitors risk signals and adjusts constraints to keep AI systems operating within safe boundaries.

---

## New to THEOS?

### **For Anthropic Reviewers:**
**Start here:** [ANTHROPIC_QUICK_START.md](ANTHROPIC_QUICK_START.md) — Tailored 60-minute review path with evidence, implementation, and compliance docs.

### **For Everyone Else:**
**Start here:** [BENCHMARKS.md](BENCHMARKS.md) — Quantitative performance analysis including safety improvements, compute costs, and latency impacts.

**Core concept:** [THEOS Functional Time](governance/THEOS_Functional_Time.md) — How temporal governance enables AI accountability without recursive refinement.

**Quick orientation:** [THEOS Quick Reference](governance/00_THEOS_Quick_Reference.md) — One-page overview for busy executives.

---

## What THEOS Does

The **Theostat** (THEOS Governor) constrains, allocates, and audits reasoning produced by other AI systems, providing:
- **Bounded reasoning** (depth, energy, tool use)
- **Posture-based escalation** (Normal → Probation → Containment → Isolation)
- **Delayed, auditable adaptation** (wisdom accumulation without observable learning)
- **Capability gating** by deployment mode
- **Enforceable suspension** and lifecycle controls

**THEOS does not replace Constitutional AI; it governs its application in real-time.** It is a **"Theostat"** that helps the model run safely in high-stakes environments.

---

## Repository Navigation

This repository is organized into four key directories:

1.  **[/pitch](pitch/)** - Core pitch materials for Anthropic.
2.  **[/evidence](evidence/)** - Empirical evidence validating THEOS.
3.  **[/code](code/)** - Core code and integration guides.
4.  **[/compliance](compliance/)** - Regulatory compliance documentation.

---

## Key Innovations

1. **Functional Time (Temporal Governance)**  
   THEOS introduces functional time as a governance primitive—enabling AI systems to be shaped by past consequences without requiring recursive refinement or exploitable memory.

2. **Cumulative Wisdom Without Observable Adaptation**  
   THEOS accumulates consequence-based wisdom from past interactions without allowing adversaries to observe or exploit the learning process.

3. **Posture-Based Escalation**  
   Under threat, THEOS gracefully degrades capabilities (depth, verbosity, tool access) rather than failing catastrophically.

4. **Safety Envelopes**  
   All hyperparameters are bounded to prevent accidental misconfiguration or adversarial parameter tuning.

5. **Delayed Adaptation**  
   Wisdom updates happen offline, not during inference, preventing real-time manipulation.

---

## Status

**Specification:** Complete (v1.2, v1.3, v1.4)  
**Reference Implementation:** Available (Python, zero dependencies)  
**Hardening:** Complete (Phases 1-5)  
**Deployment:** Seeking pilot partners  

---

## Quick Links

- **[/pitch/THEOS_CROSS_PLATFORM_PERFORMANCE_SUMMARY.md](pitch/THEOS_CROSS_PLATFORM_PERFORMANCE_SUMMARY.md)** (Start here)
- **[/code/theos_governor.py](code/theos_governor.py)** (For engineers)
- **[/evidence/BENCHMARKS.md](evidence/BENCHMARKS.md)** (Performance analysis)
- **[/compliance/REGULATORY_COMPLIANCE_MAPPING.md](compliance/REGULATORY_COMPLIANCE_MAPPING.md)** (Regulatory alignment)

---

## About the Creator

**Frederick Davis Stalnecker** is a U.S. musician, songwriter, inventor, and AI safety researcher. His work spans multiple disciplines, from headlining international music tours to pioneering governance-first AI architectures.

- **ORCID:** [0009-0009-9063-7438](https://orcid.org/0009-0009-9063-7438)

---

## Contact & N.D.A.

For research collaboration, licensing inquiries, or pilot deployments:

**Frederick Davis Stalnecker**  
**Email:** frederick.stalnecker@theosresearch.org  
**Phone:** +1 (615) 642-6643  
**GitHub:** [Frederick-Stalnecker/THEOS](https://github.com/Frederick-Stalnecker/THEOS)

**N.D.A. available upon request.** Public materials require no N.D.A.

---

## License

Unless otherwise noted, THEOS documentation and specifications are:
- **Copyright © 2025 Frederick Davis Stalnecker**
- Available for academic/research use (see [`/legal/`](legal/) for licensing options)

---

## Contributing

We welcome contributions! See [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) for guidelines.

For security vulnerabilities, see [`.github/SECURITY.md`](.github/SECURITY.md).

---

**THEOS: Governance-first AI safety. Deployable today.**
