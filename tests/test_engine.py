import pytest

from museengine import (
    Candidate,
    LLMError,
    MemoryStore,
    MuseEngine,
    MuseMiddleware,
    complete_json,
    load_default_archetypes,
    pareto_frontier,
)

from .conftest import FakeLLM


def test_library_loads():
    archetypes = load_default_archetypes()
    assert len(archetypes) == 6
    assert all(a.operators for a in archetypes)


def test_heuristic_mode_invents_nothing():
    report = MuseEngine().imagine("Why does tidal shear help estuary clearance?")
    assert report.mode == "heuristic"
    assert report.llm_calls == 0
    assert report.candidates == [] and report.frontier == []
    assert all(a.fit is None for a in report.analogies)
    assert "not been checked" in report.scaffold()


def test_heuristic_mode_returns_nothing_for_unrelated_input():
    assert MuseEngine().imagine("asdf qwerty").analogies == []


def test_llm_pipeline_end_to_end(fake_llm):
    report = MuseEngine(llm=fake_llm).imagine("Design a backpressure mesh", top_k=3)
    assert report.mode == "llm"
    # the hallucinated archetype id is dropped
    assert [a.archetype_id for a in report.analogies] == ["mycelial_physarum", "spin_glass_annealing"]
    assert len(report.candidates) == 2
    verdicts = [c.verdict for c in report.candidates]
    assert verdicts == ["survives", "refuted"]
    assert [c.id for c in report.frontier] == [report.candidates[0].id]
    assert report.llm_calls == 1 + 1 + 2 + 2
    assert "survived an adversarial critique" in report.scaffold()


def test_separate_critic_is_used(fake_llm):
    critic = FakeLLM(critique={"novelty": 0.5, "rigor": 0.5, "verdict": "survives", "reasoning": ""})
    report = MuseEngine(llm=fake_llm, critic=critic).imagine("Design a backpressure mesh")
    assert fake_llm.count("critique") == 0
    assert critic.count("critique") == 2
    assert report.llm_calls == 6


def test_candidate_without_tests_cannot_survive(fake_llm):
    fake_llm.responses["GENERATE"] = dict(fake_llm.responses["GENERATE"], tests=[])
    fake_llm.responses["CRITIQUE"] = {"novelty": 1, "rigor": 1, "verdict": "survives"}
    report = MuseEngine(llm=fake_llm).imagine("Design a backpressure mesh")
    assert report.frontier == []
    assert all(c.verdict == "refuted" for c in report.candidates)


def test_memory_recall_feeds_mapping(fake_llm):
    memory = MemoryStore()
    engine = MuseEngine(llm=fake_llm, memory=memory)
    engine.imagine("Backpressure mesh for hot-key traffic")
    report = engine.imagine("Hot-key traffic in a cache cluster")
    assert report.recalled == ["Backpressure mesh for hot-key traffic"]
    map_prompts = [p for p in fake_llm.prompts if "TASK: MAP" in p]
    assert "Backpressure mesh for hot-key traffic" in map_prompts[-1]
    assert len(memory.episodes()) == 2


def test_episode_open_when_nothing_survives():
    llm = FakeLLM(
        analyze={"domain": "x"},
        map={"analogies": [{"archetype_id": "mycelial_physarum", "mapping": "m", "fit": 0.5}]},
        generate={"title": "t", "thesis": "t", "tests": ["t"]},
        critique={"novelty": 0.1, "rigor": 0.1, "verdict": "refuted"},
    )
    memory = MemoryStore()
    MuseEngine(llm=llm, memory=memory).imagine("some problem")
    assert memory.episodes(only_open=True)


def _cand(cid, n, r, verdict="survives"):
    return Candidate(cid, cid, "", [], ["t"], "a", novelty=n, rigor=r, verdict=verdict)


def test_pareto_frontier():
    cs = [_cand("a", 0.9, 0.2), _cand("b", 0.5, 0.5), _cand("c", 0.4, 0.4), _cand("d", 1.0, 1.0, "refuted")]
    frontier = pareto_frontier(cs)
    assert {c.id for c in frontier} == {"a", "b"}
    assert not cs[2].pareto


def test_complete_json_retries_then_fails():
    replies = iter(["not json", '```json\n{"ok": 1}\n```'])
    assert complete_json(lambda p: next(replies), "q") == {"ok": 1}
    with pytest.raises(LLMError):
        complete_json(lambda p: "still not json", "q", retries=1)


def test_middleware_injects_system_message():
    seen = {}

    @MuseMiddleware(MuseEngine())
    def agent(messages):
        seen["messages"] = messages
        return "ok"

    assert agent([{"role": "user", "content": "estuary tidal clearance"}]) == "ok"
    assert seen["messages"][0]["role"] == "system"
    assert "<muse_scaffold>" in seen["messages"][0]["content"]
    assert seen["messages"][1] == {"role": "user", "content": "estuary tidal clearance"}


def test_middleware_merges_existing_system_message():
    seen = {}

    @MuseMiddleware(MuseEngine())
    def agent(messages):
        seen["messages"] = messages

    agent([{"role": "system", "content": "be brief"}, {"role": "user", "content": "slime mold routing"}])
    assert len(seen["messages"]) == 2
    assert seen["messages"][0]["content"].startswith("be brief")


def test_anthropic_adapter_with_stub_client():
    from types import SimpleNamespace

    from museengine import anthropic_llm

    calls = []

    class Messages:
        def create(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text="hi")])

    client = SimpleNamespace(beta=SimpleNamespace(messages=Messages()))
    assert anthropic_llm(client=client)("hello") == "hi"
    assert calls[0]["model"] == "claude-opus-5-5"
    assert calls[0]["messages"] == [{"role": "user", "content": "hello"}]
