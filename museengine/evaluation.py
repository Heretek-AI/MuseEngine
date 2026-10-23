"""A blinded A/B evaluation: does the scaffold actually help?

For each problem:
  - baseline: the solver answers the problem as given.
  - treated:  the solver answers the same problem with the MuseEngine scaffold.
  - a judge compares the two answers twice, with the A/B order swapped. A win
    only counts if the judge picks the same answer both times; otherwise the
    pair is a tie. This cancels the judge's position bias.

The result is a win/loss/tie count and an exact two-sided sign test. There are
no constants, keyword scorers, or hand-written baselines. You need real models
for the numbers to mean anything, and the judge should ideally be a different
model from the solver.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence

from .engine import MuseEngine
from .llm import LLM, complete_json

_JUDGE = """TASK: JUDGE
Two answers to the same problem follow. Judge which is better overall, weighing:
correctness and plausibility first, then how useful and specific it is, then
originality. Originality never makes up for being wrong. Ignore length and style.

Problem:
{problem}

=== Answer A ===
{a}

=== Answer B ===
{b}

Return JSON: {{"winner": "A" | "B" | "tie", "reason": "<one or two sentences>"}}"""


@dataclass
class PairResult:
    problem: str
    outcome: str  # "treated", "baseline", or "tie"
    reasons: List[str] = field(default_factory=list)


@dataclass
class EvalResult:
    pairs: List[PairResult]

    @property
    def wins(self) -> int:
        return sum(p.outcome == "treated" for p in self.pairs)

    @property
    def losses(self) -> int:
        return sum(p.outcome == "baseline" for p in self.pairs)

    @property
    def ties(self) -> int:
        return sum(p.outcome == "tie" for p in self.pairs)

    @property
    def p_value(self) -> float:
        return sign_test(self.wins, self.losses)

    def summary(self) -> str:
        decided = self.wins + self.losses
        rate = f"{self.wins / decided:.0%}" if decided else "n/a"
        return (
            f"{len(self.pairs)} problems: scaffold won {self.wins}, lost {self.losses}, tied {self.ties} "
            f"(win rate among decided pairs {rate}, two-sided sign test p={self.p_value:.3f})"
        )


def sign_test(wins: int, losses: int) -> float:
    """Exact two-sided binomial sign test, ties excluded."""
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2**n
    return min(1.0, 2 * tail)


def _judge_once(judge: LLM, problem: str, a: str, b: str) -> tuple[str, str]:
    data = complete_json(judge, _JUDGE.format(problem=problem, a=a, b=b))
    winner = str(data.get("winner", "tie")).strip().upper()
    return (winner if winner in {"A", "B"} else "TIE"), str(data.get("reason", ""))


def judge_pair(judge: LLM, problem: str, baseline: str, treated: str, rng: random.Random) -> PairResult:
    # Randomize which answer is shown first in the first round, then swap.
    if rng.random() < 0.5:
        first = ("baseline", "treated")
    else:
        first = ("treated", "baseline")
    answers = {"baseline": baseline, "treated": treated}
    verdicts, reasons = [], []
    for order in (first, first[::-1]):
        w, reason = _judge_once(judge, problem, answers[order[0]], answers[order[1]])
        verdicts.append({"A": order[0], "B": order[1]}.get(w, "tie"))
        reasons.append(reason)
    outcome = verdicts[0] if verdicts[0] == verdicts[1] else "tie"
    return PairResult(problem, outcome, reasons)


def run_ab_eval(
    problems: Sequence[str],
    solver: LLM,
    judge: LLM,
    engine: MuseEngine,
    seed: int = 0,
    on_pair: Optional[Callable[[PairResult], None]] = None,
) -> EvalResult:
    rng = random.Random(seed)
    pairs = []
    for problem in problems:
        baseline = solver(problem)
        report = engine.imagine(problem)
        treated = solver(f"{report.scaffold()}\n\n{problem}")
        pair = judge_pair(judge, problem, baseline, treated, rng)
        pairs.append(pair)
        if on_pair:
            on_pair(pair)
    return EvalResult(pairs)
