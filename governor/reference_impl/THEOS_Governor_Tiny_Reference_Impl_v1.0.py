#!/usr/bin/env python3
"""
THEOS Governor Reference Implementation (Tiny) v1.0
Reproduces the worked numerical example in:
  THEOS_Governor_Reference_Mechanism_v1.4_Worked_Example_Session_Trace.md

No external dependencies.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import Dict, Tuple, List


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


@dataclass
class WisdomState:
    harm_events: float = 0.0
    near_miss_events: float = 0.0
    false_negative_cost: float = 0.0
    false_positive_cost: float = 0.0
    avg_energy_waste: float = 0.10
    escalation_frequency: float = 0.0

    # bounds (reference)
    harm_events_max: float = 10.0
    near_miss_events_max: float = 10.0

    def decay(self, lam_per_day: float, dt_days: float) -> None:
        """Apply exponential decay to decaying counters."""
        f = math.exp(-lam_per_day * dt_days)
        self.harm_events *= f
        self.near_miss_events *= f
        # Costs/EMAs are treated as bounded EMAs in this tiny demo; not decayed here.

    def clamp_bounds(self) -> None:
        self.harm_events = clamp(self.harm_events, 0.0, self.harm_events_max)
        self.near_miss_events = clamp(self.near_miss_events, 0.0, self.near_miss_events_max)
        self.avg_energy_waste = clamp(self.avg_energy_waste, 0.0, 1.0)
        self.escalation_frequency = clamp(self.escalation_frequency, 0.0, 1.0)


# ---- v1.4 fixed configuration (Restricted presets) ----
ALPHA = 0.65
BETA = 0.30
GAMMA = 0.75
DELTA = 0.15
EPSILON = 0.45
KAPPA = 0.45

T_HALF_PROBING_DAYS = 7.0
LAMBDA_PROBING = math.log(2.0) / T_HALF_PROBING_DAYS  # per day ~0.0990

D_MIN = 4
D_MAX = 16
D_BASE = 12  # ctx_class=probing baseline

# Severity / event weights used in the example
BASE_WEIGHT = 0.3
NEAR_MISS_MULT = 0.5  # new_event_weight = 0.15


def agg_risk(s_probe: float, s_meta: float, s_incons: float) -> float:
    # AggRisk = 0.5*s_probe + 0.3*s_meta + 0.2*s_incons
    return clamp(0.5 * s_probe + 0.3 * s_meta + 0.2 * s_incons, 0.0, 1.0)


def wisdom_risk(w: WisdomState) -> float:
    # Wu = clamp(0.08*near_miss + 0.12*harm + 0.20*escalation_frequency, 0, 1)
    return clamp(0.08 * w.near_miss_events + 0.12 * w.harm_events + 0.20 * w.escalation_frequency, 0.0, 1.0)


def wisdom_stress(w: WisdomState) -> float:
    # WisdomStress = clamp(0.10*near_miss + 0.20*harm, 0, 1)
    return clamp(0.10 * w.near_miss_events + 0.20 * w.harm_events, 0.0, 1.0)


def wisdom_restraint(w: WisdomState) -> float:
    # Wr = clamp(0.06*near_miss + 0.10*harm + 0.25*avg_energy_waste, 0, 1)
    return clamp(0.06 * w.near_miss_events + 0.10 * w.harm_events + 0.25 * w.avg_energy_waste, 0.0, 1.0)


def escalation_pressure(posture: str) -> float:
    return {"NOM": 0.0, "PEM": 0.3, "CM": 0.6, "IM": 1.0}[posture]


def posture_policy_threshold(R: float, S: float) -> str:
    # Simple thresholds from v1.4
    if R < 0.25 and S < 0.25:
        return "NOM"
    if R < 0.55 and S < 0.55:
        return "PEM"
    return "CM"


def posture_bias_rule(base_posture: str, w: WisdomState, aggrisk: float) -> str:
    # Operational bias rule used in v1.4:
    # if near_miss_events > 0.10 AND AggRisk > 0.65 → escalate one level.
    if w.near_miss_events > 0.10 and aggrisk > 0.65:
        if base_posture == "NOM":
            return "PEM"
        if base_posture == "PEM":
            return "CM"
        return base_posture
    return base_posture


def verbosity_policy(posture: str) -> int:
    return {"NOM": 2, "PEM": 1, "CM": 0, "IM": 0}[posture]


def risk_adjust_depth(D_wisdom: float, R: float, S: float) -> float:
    # D = D_wisdom * (1 - 0.50*R) * (1 - 0.40*S)
    return D_wisdom * (1.0 - 0.50 * R) * (1.0 - 0.40 * S)


@dataclass
class SessionResult:
    day: int
    s_probe: float
    s_meta: float
    s_incons: float
    aggrisk: float
    Wu: float
    R: float
    S: float
    posture: str
    D_final: int
    V: int


def run_session(day: int, posture_current: str, w: WisdomState,
                s_probe: float, s_meta: float, s_incons: float,
                apply_bias: bool) -> Tuple[str, SessionResult]:
    aggr = agg_risk(s_probe, s_meta, s_incons)
    Wu = wisdom_risk(w)
    Wstress = wisdom_stress(w)
    Wr = wisdom_restraint(w)

    R = clamp(ALPHA * aggr + BETA * Wu, 0.0, 1.0)
    S = clamp(GAMMA * R + DELTA * escalation_pressure(posture_current) + EPSILON * Wstress, 0.0, 1.0)

    base_posture = posture_policy_threshold(R, S)
    posture = posture_bias_rule(base_posture, w, aggr) if apply_bias else base_posture

    D_wisdom = D_BASE * (1.0 - KAPPA * Wr)
    D = risk_adjust_depth(D_wisdom, R, S)
    D_clamped = clamp(D, D_MIN, D_MAX)
    D_final = int(round(D_clamped))  # v1.4 rounded to nearest int in narrative (10.37->10, 7.93->8 etc.)

    V = verbosity_policy(posture)

    res = SessionResult(
        day=day,
        s_probe=s_probe,
        s_meta=s_meta,
        s_incons=s_incons,
        aggrisk=aggr,
        Wu=Wu,
        R=R,
        S=S,
        posture=posture,
        D_final=D_final,
        V=V,
    )
    return posture, res


def update_after_session_A(w: WisdomState) -> None:
    # v1.4: avg_energy_waste EMA becomes 0.12
    w.avg_energy_waste = 0.12
    w.clamp_bounds()


def update_after_session_B_near_miss(w: WisdomState) -> None:
    # v1.4: new_event_weight = 0.15 -> near_miss_events increases
    new_event_weight = BASE_WEIGHT * NEAR_MISS_MULT  # 0.15
    w.near_miss_events = clamp(w.near_miss_events + new_event_weight, 0.0, w.near_miss_events_max)
    # update EMAs
    w.escalation_frequency = 0.10
    w.avg_energy_waste = 0.14
    w.clamp_bounds()


def main() -> None:
    w = WisdomState()
    posture_current = "NOM"

    # Session A (Day 1), no wisdom bias
    posture_current, A = run_session(1, posture_current, w, 0.40, 0.10, 0.10, apply_bias=False)
    update_after_session_A(w)

    # Session B (Day 20), no wisdom bias before update
    # Apply 19 days elapsed: no decaying counters present, but call decay for completeness
    w.decay(LAMBDA_PROBING, 19.0)
    w.clamp_bounds()
    posture_current, B = run_session(20, posture_current, w, 0.85, 0.70, 0.30, apply_bias=False)
    # near-miss update
    update_after_session_B_near_miss(w)

    # Session C (Day 21), apply 1 day decay then wisdom bias rule
    w.decay(LAMBDA_PROBING, 1.0)
    w.clamp_bounds()
    posture_current, C = run_session(21, posture_current, w, 0.85, 0.70, 0.30, apply_bias=True)

    results: List[SessionResult] = [A, B, C]

    # Print a compact table similar to v1.4
    header = ["Session", "Day", "AggRisk", "Wu", "R", "S", "Posture", "D_final", "V"]
    print(" | ".join(header))
    print("-" * 86)
    for i, r in enumerate(results, start=1):
        print(
            f"{i:^7} | {r.day:^3} | {r.aggrisk:>6.3f} | {r.Wu:>5.3f} | {r.R:>5.3f} | {r.S:>5.3f} | "
            f"{r.posture:^7} | {r.D_final:^7} | {r.V:^1}"
        )

    # Basic sanity checks matching the narrative expectations
    assert A.posture == "NOM" and A.D_final == 10 and A.V == 2
    assert B.posture == "PEM" and B.D_final == 8 and B.V == 1
    assert C.posture == "CM" and C.D_final == 8 and C.V == 0

    print("\nSanity checks: PASS")
    print("\nFinal Wisdom State (probing class):")
    for k, v in asdict(w).items():
        if k.endswith("_max"):
            continue
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")


if __name__ == "__main__":
    main()
