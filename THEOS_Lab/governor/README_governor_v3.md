# THEOS Dual-Clock Governor (LOCKED v3)

This release locks in two upgrades:

1) **Roller Pressure (Adaptive Contradiction Intensity)**
- The governor maintains a bounded `pressure` value (think: roller distance/pressure).
- Higher pressure increases adversarial intensity and consumes contradiction budget faster.
- Lower pressure relaxes and allows early freeze when engines converge.

2) **Contradiction Signal + Optional Phase**
- `contradiction_signal = 1 - similarity`
- `phase = π * contradiction_signal` (optional; interpretability only)

## What changed
- Contradiction spend is now pressure-weighted:
  `contradiction_spent += pressure * contradiction_signal * k`
- Governor emits `mode` (NORMAL/TIGHTEN/DEGRADE) to orchestrate upstream prompting.

Python 3.10+. No external dependencies.
