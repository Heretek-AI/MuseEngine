"""A small, governed autonomous loop around MuseEngine.

The agent works through a persistent goal queue. It decides its next step by a
fixed, readable rule (no hidden scoring):

1. If there is a queued goal, ``explore`` it with the engine.
2. Otherwise, if enough new episodes have piled up, ``reflect``: ask the LLM to
   distill lessons from them into notes.
3. Otherwise, if some past problems are still open (nothing survived critique),
   ``propose_goal``: ask the LLM to draft one follow-up problem. Drafting has no
   side effects.
4. If a draft is pending, ``adopt_goal`` queues it. By default this needs human
   approval, and the approver sees the exact problem text, because it is the
   agent choosing its own work.
5. Otherwise stop: there is nothing to do, and the agent does not make work up.

Every step passes through the ``Governor``. The loop stops on the first denial,
on the kill switch, on the step budget, or when idle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .engine import MuseEngine
from .governance import GovernanceError, Governor, ProposedAction
from .llm import complete_json, str_list
from .memory import MemoryStore

_REFLECT = """TASK: REFLECT
Here are recent problems and what came of them:
{episodes}

Write 1-3 short, specific lessons that would help with future problems. Only include
lessons that the evidence above supports. If there is nothing worth keeping, return an
empty list.

Return JSON: {{"lessons": ["..."]}}"""

_PROPOSE = """TASK: PROPOSE_GOAL
These problems are still open (no idea survived critique):
{episodes}

Lessons so far:
{notes}

Propose exactly one narrower or reframed follow-up problem that is more likely to get a
useful answer, and say why.

Return JSON: {{"problem": "...", "why": "..."}}"""


@dataclass
class StepResult:
    action: str
    effect: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RunResult:
    steps: List[StepResult]
    stopped_because: str


class MuseAgent:
    def __init__(self, engine: MuseEngine, memory: MemoryStore, governor: Governor, reflect_every: int = 3):
        if engine.memory is not memory:
            raise ValueError("engine and agent must share the same MemoryStore")
        self.engine = engine
        self.memory = memory
        self.governor = governor
        self.reflect_every = reflect_every

    # -- goal queue (persisted) -----------------------------------------------

    def goals(self) -> List[str]:
        return list(self.memory.get_state("goals", []))

    def add_goal(self, problem: str) -> None:
        self.memory.set_state("goals", self.goals() + [problem])

    def _pop_goal(self) -> str:
        goals = self.goals()
        goal = goals.pop(0)
        self.memory.set_state("goals", goals)
        return goal

    # -- loop -----------------------------------------------------------------

    def next_action(self) -> Optional[ProposedAction]:
        goals = self.goals()
        if goals:
            return ProposedAction("explore", "a goal is queued", {"problem": goals[0]})
        if self.engine.llm is None:
            return None
        episodes = self.memory.episodes()
        reflected = self.memory.get_state("reflected_count", 0)
        if len(episodes) - reflected >= self.reflect_every:
            return ProposedAction("reflect", f"{len(episodes) - reflected} episodes since last reflection")
        pending = self.memory.get_state("pending_proposal")
        if pending:
            return ProposedAction("adopt_goal", pending["why"], {"problem": pending["problem"]})
        open_eps = self.memory.episodes(only_open=True)
        if open_eps and not self.memory.get_state("proposal_declined", False):
            return ProposedAction(
                "propose_goal", f"{len(open_eps)} problems are still open", {"open": [e.problem for e in open_eps]}
            )
        return None

    def step(self) -> Optional[StepResult]:
        action = self.next_action()
        if action is None:
            return None
        try:
            self.governor.authorize(action)
        except GovernanceError:
            if action.name == "adopt_goal":
                # Drop the draft and don't keep asking every tick.
                self.memory.set_state("pending_proposal", None)
                self.memory.set_state("proposal_declined", True)
            raise
        try:
            effect = getattr(self, f"_do_{action.name}")(action)
        except Exception as exc:
            self.governor.record_failure(action, exc)
            raise
        self.governor.record_outcome(action, effect)
        return StepResult(action.name, effect)

    def run(self) -> RunResult:
        steps: List[StepResult] = []
        while True:
            stop = self.governor.should_stop()
            if stop:
                return RunResult(steps, stop)
            try:
                result = self.step()
            except GovernanceError as exc:
                return RunResult(steps, f"denied: {exc}")
            if result is None:
                return RunResult(steps, "nothing to do")
            steps.append(result)

    # -- actions --------------------------------------------------------------

    def _do_explore(self, action: ProposedAction) -> Dict[str, Any]:
        problem = action.payload["problem"]
        report = self.engine.imagine(problem)
        # Only dequeue once the work succeeded, so a failed call keeps the goal.
        self._pop_goal()
        return {
            "problem": problem,
            "mode": report.mode,
            "episode_id": report.episode_id,
            "candidates": len(report.candidates),
            "refuted": sum(1 for c in report.candidates if c.verdict == "refuted"),
            "frontier": [c.title for c in report.frontier],
            "llm_calls": report.llm_calls,
        }

    def _do_reflect(self, action: ProposedAction) -> Dict[str, Any]:
        episodes = self.memory.episodes()
        start = self.memory.get_state("reflected_count", 0)
        recent = episodes[start:]
        data = complete_json(
            self.engine.llm,
            _REFLECT.format(episodes="\n".join(f"- {e.problem} -> {e.summary}" for e in recent)),
        )
        lessons = str_list(data.get("lessons"))
        for lesson in lessons:
            self.memory.add_note(lesson, [e.id for e in recent])
        self.memory.set_state("reflected_count", len(episodes))
        return {"episodes_reviewed": len(recent), "lessons_saved": lessons}

    def _do_propose_goal(self, action: ProposedAction) -> Dict[str, Any]:
        open_eps = self.memory.episodes(only_open=True)
        data = complete_json(
            self.engine.llm,
            _PROPOSE.format(
                episodes="\n".join(f"- {e.problem} -> {e.summary}" for e in open_eps),
                notes="\n".join(f"- {n}" for n in self.memory.notes()) or "(none)",
            ),
        )
        problem = str(data.get("problem", "")).strip()
        # The open problems have now been followed up; close them so the agent
        # doesn't propose again from the same evidence.
        for ep in open_eps:
            self.memory.set_open(ep.id, False)
        if not problem:
            return {"drafted": None, "why": "model proposed nothing"}
        why = str(data.get("why", ""))
        self.memory.set_state("pending_proposal", {"problem": problem, "why": why})
        return {"drafted": problem, "why": why}

    def _do_adopt_goal(self, action: ProposedAction) -> Dict[str, Any]:
        problem = action.payload["problem"]
        self.add_goal(problem)
        self.memory.set_state("pending_proposal", None)
        return {"queued": problem}
