# Appendix D — Governance Memory, GMAs, and Cumulative Assets (Draft)

## Purpose
THEOS treats governance artifacts as cumulative assets that can compound over time. These include:
- contradiction signals and budgets
- governor decisions and rationales
- failure mode records and mitigations
- degradation/recovery traces
- “GMAs” (governance memory artifacts): compact, reusable governance heuristics derived from prior runs

## GMAs as Cumulative Assets
A GMA is a compact governance-relevant unit derived from experience (e.g., a stop-pattern, refusal taxonomy trigger, or “degrade-to-safe-mode” rule). GMAs should:
- be **portable** across tasks and domains (where appropriate)
- be **auditable** (source trace and rationale)
- have **bounded influence** (cannot override hard safety/risk ceilings)
- support **time-consequence tracking** by allowing the system to reference what it previously learned as “momentary past”

## Implementation Notes (Model-Agnostic)
- Maintain a small ledger of GMAs keyed by scenario class and risk profile.
- Apply GMAs via the governor as constraints/tie-breakers, not as a replacement for reasoning.
- Ensure GMAs have expiry / revalidation hooks to avoid stale governance.

## Why This Matters
This is how “wisdom” becomes maintainable rather than episodic: governance learns from its own governed history.
