"""MuseEngine: structured cross-domain ideation on top of an LLM.

Pipeline (each step is one or more LLM calls with a JSON contract):

1. ANALYZE   - describe the problem's structure (tensions, constraints, failure modes)
               independently of its vocabulary.
2. MAP       - pick archetypes from the library whose *mechanisms* fit that
               structure, say what maps to what, and where the analogy breaks.
               Related past problems from memory are offered as extra context.
3. GENERATE  - turn each analogy into a concrete candidate with tests that could
               falsify it (science) or break it (systems).
4. CRITIQUE  - an adversarial, separate prompt scores novelty and rigor, lists
               fatal flaws, and refutes candidates that don't hold up.
5. SELECT    - keep the Pareto frontier over (novelty, rigor) among survivors.

Without an LLM the engine runs in ``heuristic`` mode: it ranks archetypes by
word overlap and returns them as unvetted suggestions. It does not invent
candidates or scores in that mode.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from .archetypes import Archetype, index_by_id, load_default_archetypes
from .llm import LLM, CountingLLM, as_list, clamp01, complete_json, str_list
from .memory import Episode, MemoryStore

SURVIVES = "survives"
REFUTED = "refuted"
UNREVIEWED = "unreviewed"


@dataclass
class ProblemStructure:
    domain: str
    tensions: List[Dict[str, Any]]
    constraints: List[str]
    failure_modes: List[str]


@dataclass
class Analogy:
    archetype_id: str
    archetype_name: str
    mapping: str
    breaks_where: str
    fit: Optional[float]


@dataclass
class Candidate:
    id: str
    title: str
    thesis: str
    mechanism: List[str]
    tests: List[str]
    source_archetype: str
    novelty: Optional[float] = None
    rigor: Optional[float] = None
    fatal_flaws: List[str] = field(default_factory=list)
    critique: str = ""
    verdict: str = UNREVIEWED
    pareto: bool = False


@dataclass
class Report:
    problem: str
    mode: str  # "llm" or "heuristic"
    structure: Optional[ProblemStructure]
    analogies: List[Analogy]
    candidates: List[Candidate]
    frontier: List[Candidate]
    recalled: List[str]
    llm_calls: int
    episode_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def scaffold(self) -> str:
        """A compact system block to prepend to another agent's prompt."""
        lines = ["<muse_scaffold>"]
        if self.mode == "heuristic" and not self.analogies:
            lines.append("No analogy in the library looked relevant to this problem.")
        elif self.mode == "heuristic":
            lines.append(
                "These cross-domain analogies were matched by keyword only and have not been "
                "checked. Use them only if they genuinely fit; ignore any that don't."
            )
            for a in self.analogies:
                lines.append(f"- {a.archetype_name}: {a.mapping}")
        else:
            s = self.structure
            if s and s.constraints:
                lines.append("Constraints to respect:")
                lines += [f"- {c}" for c in s.constraints]
            if self.frontier:
                lines.append("Candidate directions that survived an adversarial critique:")
                for c in self.frontier:
                    lines.append(f"- {c.title} (novelty {c.novelty:.2f}, rigor {c.rigor:.2f}): {c.thesis}")
                    if c.tests:
                        lines.append(f"  Test that could break it: {c.tests[0]}")
                    if c.fatal_flaws:
                        lines.append(f"  Open concern: {c.fatal_flaws[0]}")
            else:
                lines.append("No candidate survived critique; treat the analogies below as weak leads.")
                for a in self.analogies:
                    lines.append(f"- {a.archetype_name}: {a.mapping} (breaks where: {a.breaks_where})")
        lines.append(
            "Build on these where they help, say plainly where they don't, and prefer a correct "
            "conventional answer over a novel wrong one."
        )
        lines.append("</muse_scaffold>")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

_ANALYZE = """TASK: ANALYZE
Describe the abstract structure of this problem, independent of its domain vocabulary.

Problem:
{problem}

Return JSON:
{{"domain": "<short label, e.g. distributed systems, neuroscience, marketing>",
  "tensions": [{{"axis": "<a trade-off or pressure>", "description": "<one sentence>", "weight": <0-1>}}],
  "constraints": ["<hard limits any solution must respect>"],
  "failure_modes": ["<how naive solutions fail>"]}}
List 2-5 tensions. Be specific to this problem; do not pad."""

_MAP = """TASK: MAP
You are looking for structural analogies: mechanisms from another field whose causal
structure matches this problem, not just shared words.

Problem:
{problem}

Problem structure:
{structure}

{recalled}Analogy library:
{library}

Pick up to {k} archetypes whose mechanisms genuinely fit. It is fine to pick fewer, or
none, if nothing fits. For each, say concretely what maps to what, and where the analogy
breaks down.

Return JSON:
{{"analogies": [{{"archetype_id": "<id from the library>", "mapping": "<what corresponds to what>",
  "breaks_where": "<where the analogy fails>", "fit": <0-1>}}]}}"""

_GENERATE = """TASK: GENERATE
Turn this analogy into one concrete candidate {kind}.

Problem:
{problem}

Analogy ({name}): {mapping}
It breaks down where: {breaks}

Return JSON:
{{"title": "<short name>",
  "thesis": "<the claim or design in 1-3 sentences>",
  "mechanism": ["<concrete steps or components>"],
  "tests": ["<{test_kind}>"]}}
Give 2-4 tests. Each must name a specific measurement or scenario and the outcome that
would count against the candidate."""

_CRITIQUE = """TASK: CRITIQUE
You are an adversarial reviewer. Your job is to find what is wrong with this candidate,
not to praise it.

Problem:
{problem}

Candidate: {title}
Thesis: {thesis}
Mechanism: {mechanism}
Proposed tests: {tests}

Score honestly:
- novelty: 0 if this is a standard textbook answer or a known technique renamed with
  metaphors; high only if it is a genuinely different approach.
- rigor: is it internally consistent, physically/technically plausible, and are the
  tests real tests that could fail?
Refute it if it is wrong, incoherent, untestable, or only a relabelled known idea.

Return JSON:
{{"novelty": <0-1>, "rigor": <0-1>, "fatal_flaws": ["..."],
  "verdict": "survives" | "refuted", "reasoning": "<2-4 sentences>"}}"""

_SCIENCE_HINTS = re.compile(
    r"\b(hypothes\w*|mechanis\w*|disease|cell\w*|protein\w*|neuro\w*|brain|gene\w*|"
    r"molecul\w*|clinical|physics|chemical|species|ecolog\w*|experiment\w*)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class MuseEngine:
    def __init__(
        self,
        llm: Optional[LLM] = None,
        archetypes: Optional[Sequence[Archetype]] = None,
        memory: Optional[MemoryStore] = None,
        critic: Optional[LLM] = None,
    ):
        """
        llm:     the model that analyzes, maps and generates. ``None`` -> heuristic mode.
        critic:  optional separate model for critique (defaults to ``llm``). Using a
                 different model reduces self-grading bias.
        memory:  optional store; past problems are recalled as context and each run
                 is recorded as an episode.
        """
        self.llm = llm
        self.critic = critic or llm
        self.archetypes = list(archetypes) if archetypes is not None else load_default_archetypes()
        self.by_id = index_by_id(self.archetypes)
        self.memory = memory

    def imagine(self, problem: str, top_k: int = 3) -> Report:
        problem = problem.strip()
        if not problem:
            raise ValueError("problem must be non-empty")
        recalled = self.memory.recall(problem, k=3) if self.memory else []
        if self.llm is None:
            report = self._heuristic(problem, top_k)
        else:
            report = self._with_llm(problem, top_k, recalled)
        report.recalled = [ep.problem for ep in recalled]
        if self.memory:
            ep = self.memory.add_episode(problem, self._summarize(report), is_open=not report.frontier)
            report.episode_id = ep.id
        return report

    # -- heuristic mode -------------------------------------------------------

    def _heuristic(self, problem: str, top_k: int) -> Report:
        words = set(re.findall(r"[a-z][a-z-]{3,}", problem.lower()))
        ranked = []
        for arch in self.archetypes:
            text = arch.search_text()
            hits = sum(1 for w in words if w in text)
            if hits:
                ranked.append((hits, arch))
        ranked.sort(key=lambda t: t[0], reverse=True)
        analogies = [
            Analogy(
                archetype_id=a.id,
                archetype_name=a.name,
                mapping="; ".join(a.operators),
                breaks_where="unknown (not analyzed)",
                fit=None,
            )
            for _, a in ranked[:top_k]
        ]
        return Report(problem, "heuristic", None, analogies, [], [], [], llm_calls=0)

    # -- LLM mode -------------------------------------------------------------

    def _with_llm(self, problem: str, top_k: int, recalled: List[Episode]) -> Report:
        llm = CountingLLM(self.llm)
        critic = llm if self.critic is self.llm else CountingLLM(self.critic)

        structure = self._analyze(llm, problem)
        analogies = self._map(llm, problem, structure, recalled, top_k)
        candidates = [self._generate(llm, problem, structure, a, i) for i, a in enumerate(analogies)]
        for c in candidates:
            self._critique(critic, problem, c)
        frontier = pareto_frontier(candidates)

        calls = llm.calls + (critic.calls if critic is not llm else 0)
        return Report(problem, "llm", structure, analogies, candidates, frontier, [], llm_calls=calls)

    def _analyze(self, llm: LLM, problem: str) -> ProblemStructure:
        data = complete_json(llm, _ANALYZE.format(problem=problem))
        tensions = [
            {"axis": str(t.get("axis", "")), "description": str(t.get("description", "")),
             "weight": clamp01(t.get("weight"), 0.5)}
            for t in as_list(data.get("tensions")) if isinstance(t, dict)
        ]
        return ProblemStructure(
            domain=str(data.get("domain", "unknown")),
            tensions=tensions,
            constraints=str_list(data.get("constraints")),
            failure_modes=str_list(data.get("failure_modes")),
        )

    def _map(
        self, llm: LLM, problem: str, structure: ProblemStructure, recalled: List[Episode], top_k: int
    ) -> List[Analogy]:
        recalled_text = ""
        if recalled:
            recalled_text = "Related problems worked on before (may or may not help):\n" + "\n".join(
                f"- {ep.problem} -> {ep.summary}" for ep in recalled
            ) + "\n\n"
        data = complete_json(
            llm,
            _MAP.format(
                problem=problem,
                structure=_structure_text(structure),
                recalled=recalled_text,
                library="\n".join(a.brief() for a in self.archetypes),
                k=top_k,
            ),
        )
        out: List[Analogy] = []
        seen = set()
        for item in as_list(data.get("analogies")):
            if not isinstance(item, dict):
                continue
            arch = self.by_id.get(str(item.get("archetype_id", "")))
            if arch is None or arch.id in seen:
                continue  # drop hallucinated or duplicate ids
            seen.add(arch.id)
            out.append(
                Analogy(
                    archetype_id=arch.id,
                    archetype_name=arch.name,
                    mapping=str(item.get("mapping", "")),
                    breaks_where=str(item.get("breaks_where", "")),
                    fit=clamp01(item.get("fit"), 0.5),
                )
            )
        out.sort(key=lambda a: a.fit or 0.0, reverse=True)
        return out[:top_k]

    def _generate(
        self, llm: LLM, problem: str, structure: ProblemStructure, analogy: Analogy, idx: int
    ) -> Candidate:
        science = bool(_SCIENCE_HINTS.search(problem + " " + structure.domain))
        data = complete_json(
            llm,
            _GENERATE.format(
                problem=problem,
                kind="hypothesis" if science else "design",
                name=analogy.archetype_name,
                mapping=analogy.mapping,
                breaks=analogy.breaks_where,
                test_kind="an experiment and the result that would falsify it"
                if science
                else "a stress or failure scenario and the observation that would show the design fails",
            ),
        )
        return Candidate(
            id=f"c{idx + 1}_{analogy.archetype_id}",
            title=str(data.get("title", analogy.archetype_name)),
            thesis=str(data.get("thesis", "")),
            mechanism=str_list(data.get("mechanism")),
            tests=str_list(data.get("tests")),
            source_archetype=analogy.archetype_id,
        )

    def _critique(self, critic: LLM, problem: str, cand: Candidate) -> None:
        data = complete_json(
            critic,
            _CRITIQUE.format(
                problem=problem,
                title=cand.title,
                thesis=cand.thesis,
                mechanism="; ".join(cand.mechanism),
                tests="; ".join(cand.tests),
            ),
        )
        cand.novelty = clamp01(data.get("novelty"))
        cand.rigor = clamp01(data.get("rigor"))
        cand.fatal_flaws = str_list(data.get("fatal_flaws"))
        cand.critique = str(data.get("reasoning", ""))
        verdict = str(data.get("verdict", "")).strip().lower()
        # Anything other than an explicit "survives" counts as refuted, and a
        # candidate without any test cannot survive.
        cand.verdict = SURVIVES if verdict == SURVIVES and cand.tests else REFUTED

    @staticmethod
    def _summarize(report: Report) -> str:
        if report.frontier:
            best = report.frontier[0]
            return f"Best surviving idea: {best.title}: {best.thesis}"
        if report.mode == "heuristic":
            return "Unvetted suggestions: " + ", ".join(a.archetype_name for a in report.analogies)
        return "No candidate survived critique."


def pareto_frontier(candidates: Sequence[Candidate]) -> List[Candidate]:
    """Non-dominated surviving candidates over (novelty, rigor), best first."""
    alive = [c for c in candidates if c.verdict == SURVIVES and c.novelty is not None and c.rigor is not None]
    frontier = []
    for c in alive:
        dominated = any(
            o is not c and o.novelty >= c.novelty and o.rigor >= c.rigor and (o.novelty > c.novelty or o.rigor > c.rigor)
            for o in alive
        )
        c.pareto = not dominated
        if c.pareto:
            frontier.append(c)
    frontier.sort(key=lambda c: c.novelty + c.rigor, reverse=True)
    return frontier


def _structure_text(s: ProblemStructure) -> str:
    lines = [f"Domain: {s.domain}"]
    lines += [f"Tension: {t['axis']} - {t['description']} (weight {t['weight']:.2f})" for t in s.tensions]
    lines += [f"Constraint: {c}" for c in s.constraints]
    lines += [f"Naive failure mode: {f}" for f in s.failure_modes]
    return "\n".join(lines)
