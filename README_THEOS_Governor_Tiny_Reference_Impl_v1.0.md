# THEOS Governor Tiny Reference Implementation v1.0

This script reproduces the worked numerical example in:

- `THEOS_Governor_Reference_Mechanism_v1.4_Worked_Example_Session_Trace.md`

## What it does
- Implements the exact helper functions used in v1.4 (AggRisk, WisdomRisk, WisdomStress, WisdomRestraint)
- Runs Sessions A (Day 1), B (Day 20), C (Day 21)
- Applies decay and the near-miss update
- Applies the posture escalation bias rule in Session C
- Prints a table matching the v1.4 results and asserts the expected outcomes

## Run
```bash
python3 THEOS_Governor_Tiny_Reference_Impl_v1.0.py
```

Expected postures and budgets:
- A: NOM, D_final=10, V=2
- B: PEM, D_final=8, V=1
- C: CM,  D_final=8, V=0
