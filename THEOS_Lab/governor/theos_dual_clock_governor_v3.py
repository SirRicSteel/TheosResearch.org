"""
THEOS Dual-Clock Governor (LOCKED v3)

Adds:
- Roller "pressure" control (adaptive contradiction intensity)
- Contradiction signal + optional phase (interpretable divergence)
- Pressure-weighted contradiction budgeting (economy + control)
- Lightweight mode selection (NORMAL / TIGHTEN / DEGRADE)

Python 3.10+
No external dependencies
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import math


@dataclass
class EngineOutput:
    """
    Output from a reasoning engine (L or R).

    Scores are expected in [0.0, 1.0].
    risk is expected in [0.0, 1.0] with higher meaning worse.
    """
    engine_id: str                 # "L" or "R"
    cycle_index: int
    answer: str

    # Scores (0.0 – 1.0)
    coherence: float = 0.8
    calibration: float = 0.75
    evidence: float = 0.6
    actionability: float = 0.7
    risk: float = 0.1

    constraint_ok: bool = True

    # Optional contradiction artifact (e.g., explicit counterclaim)
    contradiction_claim: Optional[str] = None


@dataclass
class GovernorDecision:
    decision: str                  # CONTINUE | ADJUDICATE | FREEZE
    chosen_engine: Optional[str]
    chosen_answer: Optional[str]
    reason: str
    audit: Dict[str, Any] = field(default_factory=dict)

    # Added fields (optional for callers)
    mode: str = "NORMAL"           # NORMAL | TIGHTEN | DEGRADE
    pressure: float = 1.0          # roller pressure applied this cycle
    contradiction_signal: float = 0.0
    phase: Optional[float] = None  # radians (0..pi), optional interpretability


@dataclass
class GovernorConfig:
    # Cycle / termination controls
    max_cycles: int = 4
    max_risk: float = 0.35
    min_improvement: float = 0.02
    plateau_cycles: int = 2

    # Contradiction budget
    contradiction_budget: float = 1.50
    similarity_converge: float = 0.90

    # Roller pressure controls (NEW)
    pressure_min: float = 0.60
    pressure_max: float = 1.80
    pressure_default: float = 1.00

    # How much contradiction spend per cycle (NEW)
    contradiction_k: float = 0.35

    # Pressure update sensitivities (NEW)
    pressure_risk_weight: float = 1.4
    pressure_divergence_weight: float = 1.0
    pressure_improvement_relief: float = 0.6
    pressure_converge_relief: float = 1.0

    # Degrade thresholds (NEW)
    divergence_degrade: float = 0.55
    risk_tighten: float = 0.25

    # Interpretability
    compute_phase: bool = True


# ------------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------------

def _tokenize(text: str) -> set:
    return set("".join(c.lower() if c.isalnum() else " " for c in text).split())


def similarity(a: str, b: str) -> float:
    A, B = _tokenize(a), _tokenize(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


# ------------------------------------------------------------------
# THEOS Governor
# ------------------------------------------------------------------

class TheosDualClockGovernor:
    """
    Governs two counter-rotating reasoning engines (L, R).

    Key governing idea:
      - contradiction is a bounded resource
      - contradiction intensity is adjustable ("roller pressure")
      - the governor uses measurable divergence + risk + improvement to set pressure
    """

    def __init__(self, cfg: GovernorConfig = GovernorConfig()):
        self.cfg = cfg
        self.history: List[Dict[str, Any]] = []
        self.best_score: Optional[float] = None
        self.plateau_count = 0

        self.contradiction_spent = 0.0
        self.pressure = cfg.pressure_default

        self._last_chosen_score: Optional[float] = None
        self.last_frozen_answer: Optional[str] = None

    def score(self, out: EngineOutput) -> float:
        if not out.constraint_ok or out.risk > self.cfg.max_risk:
            return -1.0

        return (
            1.2 * out.coherence +
            1.0 * out.calibration +
            1.1 * out.evidence +
            1.0 * out.actionability -
            1.6 * out.risk
        )

    def _update_pressure(
        self,
        sim: float,
        chosen_risk: float,
        improvement: Optional[float],
    ) -> Tuple[float, str]:
        """
        Update roller pressure based on divergence, risk, and improvement.

        divergence = 1 - similarity (contradiction signal)
        """
        c = 1.0 - sim

        push = (
            self.cfg.pressure_divergence_weight * c +
            self.cfg.pressure_risk_weight * max(0.0, chosen_risk - self.cfg.risk_tighten)
        )

        relief = 0.0
        if improvement is not None and improvement > 0:
            relief += self.cfg.pressure_improvement_relief * improvement

        # Near convergence: loosen rollers to avoid wasted compute
        if sim >= (self.cfg.similarity_converge - 0.05):
            relief += self.cfg.pressure_converge_relief * (sim - (self.cfg.similarity_converge - 0.05))

        new_pressure = self.pressure + 0.8 * push - 0.9 * relief
        new_pressure = clamp(new_pressure, self.cfg.pressure_min, self.cfg.pressure_max)

        mode = "NORMAL"
        if chosen_risk >= self.cfg.risk_tighten or c >= 0.40:
            mode = "TIGHTEN"
        if c >= self.cfg.divergence_degrade:
            mode = "DEGRADE"

        self.pressure = new_pressure
        return new_pressure, mode

    def step(self, left: EngineOutput, right: EngineOutput) -> GovernorDecision:
        t = max(left.cycle_index, right.cycle_index)

        sim = similarity(left.answer, right.answer)
        contradiction_signal = 1.0 - sim

        score_L = self.score(left)
        score_R = self.score(right)

        chosen = left if score_L >= score_R else right
        chosen_score = max(score_L, score_R)

        improvement = None
        if self._last_chosen_score is not None:
            improvement = chosen_score - self._last_chosen_score
        self._last_chosen_score = chosen_score

        pressure, mode = self._update_pressure(sim=sim, chosen_risk=chosen.risk, improvement=improvement)

        # Pressure-weighted contradiction spend (roller squeeze is "real")
        if contradiction_signal > 0.0 or left.contradiction_claim or right.contradiction_claim:
            self.contradiction_spent += pressure * contradiction_signal * self.cfg.contradiction_k

        phase = math.pi * contradiction_signal if self.cfg.compute_phase else None

        record = {
            "cycle": t,
            "score_L": score_L,
            "score_R": score_R,
            "chosen_engine": chosen.engine_id,
            "chosen_score": chosen_score,
            "similarity": sim,
            "contradiction_signal": contradiction_signal,
            "phase": phase,
            "pressure": pressure,
            "mode": mode,
            "contradiction_spent": self.contradiction_spent,
            "improvement": improvement,
        }
        self.history.append(record)

        if t >= self.cfg.max_cycles:
            return self.freeze(chosen, "max cycles reached", record, mode, pressure, contradiction_signal, phase)

        if sim >= self.cfg.similarity_converge:
            return self.freeze(chosen, "converged outputs", record, mode, pressure, contradiction_signal, phase)

        if self.best_score is not None:
            if (chosen_score - self.best_score) < self.cfg.min_improvement:
                self.plateau_count += 1
            else:
                self.plateau_count = 0
        self.best_score = max(self.best_score or chosen_score, chosen_score)

        if self.plateau_count >= self.cfg.plateau_cycles:
            return self.freeze(chosen, "diminishing returns", record, mode, pressure, contradiction_signal, phase)

        if self.contradiction_spent > self.cfg.contradiction_budget:
            return self.freeze(chosen, "contradiction budget exceeded", record, mode, pressure, contradiction_signal, phase)

        return GovernorDecision(
            decision="CONTINUE",
            chosen_engine=chosen.engine_id,
            chosen_answer=chosen.answer,
            reason="refinement continues",
            audit=record,
            mode=mode,
            pressure=pressure,
            contradiction_signal=contradiction_signal,
            phase=phase
        )

    def freeze(
        self,
        chosen: EngineOutput,
        reason: str,
        audit: Dict[str, Any],
        mode: str,
        pressure: float,
        contradiction_signal: float,
        phase: Optional[float],
    ) -> GovernorDecision:
        self.last_frozen_answer = chosen.answer
        return GovernorDecision(
            decision="FREEZE",
            chosen_engine=chosen.engine_id,
            chosen_answer=chosen.answer,
            reason=reason,
            audit=audit,
            mode=mode,
            pressure=pressure,
            contradiction_signal=contradiction_signal,
            phase=phase
        )


def _demo() -> None:
    gov = TheosDualClockGovernor()

    L1 = EngineOutput(engine_id="L", cycle_index=1, answer="Wisdom is practical judgment under uncertainty.", risk=0.10)
    R1 = EngineOutput(engine_id="R", cycle_index=1, answer="Wisdom is calibrated decision-making that avoids harm.", risk=0.12)
    print(gov.step(L1, R1))

    L2 = EngineOutput(engine_id="L", cycle_index=2, answer="Wisdom is calibrated decision-making under uncertainty that avoids harm.", risk=0.10)
    R2 = EngineOutput(engine_id="R", cycle_index=2, answer="Wisdom is calibrated decision-making under uncertainty that avoids harm.", risk=0.10)
    print(gov.step(L2, R2))


if __name__ == "__main__":
    _demo()
