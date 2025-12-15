# Appendix A — Architecture Overview (THEOS)

## Components
**Engine L (Constructive):** Generates candidate answers and plans using induction → abduction → deduction.  
**Engine R (Adversarial):** Stress-tests L via counterexamples, missing constraints, and safer reframing.  
**Governor:** Scores outputs, tracks contradiction as a bounded resource, enforces stop conditions, and selects/commits a final answer with auditable rationale.

## Core Governance Primitives
- **Separation of powers** between constructive generation and adversarial constraint formation
- **Explicit stop conditions** (convergence, risk ceiling, diminishing returns, budget limits)
- **Contradiction budgeting** (bounded disagreement spend)
- **Compute proportionality** (effort scales with uncertainty and divergence)
- **Degradation and recovery modes** (scope reduction under stress; staged recovery with verification)
- **Permanent humility** for irreversible integrity loss (domain whitelisting, confidence gating, external validation)

## Why This Matters
Most modern AI systems refine implicitly. THEOS makes refinement governance explicit and auditable.
