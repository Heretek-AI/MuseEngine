import random

import pytest

from museengine import (
    BudgetExceeded,
    CountingLLM,
    Governor,
    KillSwitch,
    MemoryStore,
    MuseAgent,
    MuseEngine,
    Policy,
    run_ab_eval,
    sign_test,
)
from museengine.evaluation import judge_pair

from .conftest import FakeLLM

REFUTE_ALL = dict(
    analyze={"domain": "x"},
    map={"analogies": [{"archetype_id": "mycelial_physarum", "mapping": "m", "fit": 0.5}]},
    generate={"title": "t", "thesis": "t", "tests": ["t"]},
    critique={"novelty": 0.1, "rigor": 0.1, "verdict": "refuted"},
    reflect={"lessons": ["narrow the scope"]},
    propose_goal={"problem": "a narrower problem", "why": "the first was too broad"},
)


def make_agent(llm=None, approver=lambda a: False, **policy):
    memory = MemoryStore()
    engine = MuseEngine(llm=llm, memory=memory)
    governor = Governor(memory, Policy(**policy) if policy else None, approver=approver)
    return MuseAgent(engine, memory, governor, reflect_every=2), memory


def test_memory_persists_across_reopen(tmp_path):
    path = tmp_path / "mind.db"
    m = MemoryStore(path)
    m.add_episode("p", "s")
    m.set_state("goals", ["g"])
    m.close()
    m2 = MemoryStore(path)
    assert [e.problem for e in m2.episodes()] == ["p"]
    assert m2.get_state("goals") == ["g"]


def test_agent_idles_instead_of_inventing_work():
    agent, memory = make_agent()
    result = agent.run()
    assert result.steps == [] and result.stopped_because == "nothing to do"


def test_agent_explores_queued_goals_offline():
    agent, memory = make_agent()
    agent.add_goal("estuary tidal clearance")
    result = agent.run()
    assert [s.action for s in result.steps] == ["explore"]
    assert result.steps[0].effect["mode"] == "heuristic"
    decisions = [(e["action"], e["decision"]) for e in memory.audit_log()]
    assert decisions == [("explore", "allowed"), ("explore", "completed")]


def test_self_chosen_goal_needs_approval_and_denial_stops():
    agent, memory = make_agent(FakeLLM(**REFUTE_ALL))
    agent.add_goal("problem one")
    agent.add_goal("problem two")
    result = agent.run()
    actions = [s.action for s in result.steps]
    assert actions == ["explore", "explore", "reflect", "propose_goal"]
    assert result.stopped_because.startswith("denied: adopt_goal")
    assert agent.goals() == []  # nothing queued without approval
    assert memory.notes() == ["narrow the scope"]
    # and it doesn't ask again
    assert agent.run().stopped_because == "nothing to do"


def test_approved_goal_is_queued_and_explored():
    seen = []
    agent, memory = make_agent(FakeLLM(**REFUTE_ALL), approver=lambda a: seen.append(a) or True, max_steps=6)
    agent.add_goal("problem one")
    agent.add_goal("problem two")
    result = agent.run()
    assert [s.action for s in result.steps] == [
        "explore", "explore", "reflect", "propose_goal", "adopt_goal", "explore",
    ]
    assert seen[0].payload["problem"] == "a narrower problem"  # approver saw the exact text
    assert result.stopped_because == "step budget of 6 reached"


def test_disallowed_action_is_denied():
    agent, memory = make_agent(allowed_actions=frozenset({"reflect"}))
    agent.add_goal("x")
    assert agent.run().stopped_because.startswith("denied: explore")
    assert memory.audit_log()[-1]["decision"] == "denied"


def test_kill_switch_file(tmp_path):
    agent, _ = make_agent()
    agent.governor.kill_switch = KillSwitch(tmp_path / "STOP")
    agent.add_goal("a")
    agent.add_goal("b")
    (tmp_path / "STOP").touch()
    assert agent.run().stopped_because == "kill switch tripped"
    assert agent.goals() == ["a", "b"]


def test_llm_budget():
    llm = CountingLLM(lambda p: "{}", max_calls=1)
    llm("a")
    with pytest.raises(BudgetExceeded):
        llm("b")


def test_sign_test():
    assert sign_test(0, 0) == 1.0
    assert sign_test(5, 5) == 1.0
    assert sign_test(10, 0) == pytest.approx(2 / 1024)


def test_judge_win_needs_consistency_across_order():
    # A judge that always picks whichever answer is shown first -> pure position bias.
    biased = FakeLLM(judge={"winner": "A", "reason": "first"})
    assert judge_pair(biased, "p", "base", "treat", random.Random(0)).outcome == "tie"

    # A judge that always prefers the answer containing "treat".
    def fair(prompt):
        a = prompt.split("=== Answer A ===")[1].split("=== Answer B ===")[0]
        return {"winner": "A" if "treat" in a else "B"}

    assert judge_pair(FakeLLM(judge=fair), "p", "base", "treat", random.Random(0)).outcome == "treated"


def test_run_ab_eval_uses_scaffold():
    solver_prompts = []

    def solver(prompt):
        solver_prompts.append(prompt)
        return "treat" if "<muse_scaffold>" in prompt else "base"

    def fair(prompt):
        a = prompt.split("=== Answer A ===")[1].split("=== Answer B ===")[0]
        return {"winner": "A" if "treat" in a else "B"}

    result = run_ab_eval(["slime mold routing", "estuary"], solver, FakeLLM(judge=fair), MuseEngine())
    assert (result.wins, result.losses, result.ties) == (2, 0, 0)
    assert len(solver_prompts) == 4
    assert "scaffold won 2" in result.summary()


def test_failed_explore_keeps_goal():
    def boom(prompt):
        raise RuntimeError("model down")

    agent, memory = make_agent(boom)
    agent.add_goal("keep me")
    with pytest.raises(RuntimeError):
        agent.run()
    assert agent.goals() == ["keep me"]
    assert memory.audit_log()[-1]["decision"] == "failed"


def test_run_ab_eval_rejects_blank_problems_before_calling_models():
    calls = []
    with pytest.raises(ValueError):
        run_ab_eval(["ok", "  "], lambda p: calls.append(p) or "", lambda p: "{}", MuseEngine())
    assert calls == []
