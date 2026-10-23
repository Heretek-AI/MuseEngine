import json
import re

import pytest


class FakeLLM:
    """Routes on the ``TASK: X`` marker in each prompt and returns canned JSON.

    ``responses`` maps a task name to a dict, a list of dicts (consumed in
    order), or a callable taking the prompt.
    """

    def __init__(self, **responses):
        self.responses = {k.upper(): v for k, v in responses.items()}
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        task = re.search(r"TASK: (\w+)", prompt).group(1)
        value = self.responses[task]
        if callable(value):
            value = value(prompt)
        elif isinstance(value, list):
            value = value.pop(0) if len(value) > 1 else value[0]
        return value if isinstance(value, str) else json.dumps(value)

    def count(self, task):
        return sum(f"TASK: {task.upper()}" in p for p in self.prompts)


ANALYZE = {
    "domain": "distributed systems",
    "tensions": [{"axis": "throughput vs coordination", "description": "locks serialize", "weight": 0.9}],
    "constraints": ["Little's law bounds in-flight work"],
    "failure_modes": ["retry storms"],
}

MAP = {
    "analogies": [
        {"archetype_id": "mycelial_physarum", "mapping": "links = tubes", "breaks_where": "no fluid", "fit": 0.8},
        {"archetype_id": "made_up_id", "mapping": "x", "breaks_where": "y", "fit": 0.99},
        {"archetype_id": "spin_glass_annealing", "mapping": "conflicts = defects", "breaks_where": "no energy", "fit": 0.6},
    ]
}

GENERATE = {
    "title": "Flux-weighted routing",
    "thesis": "Route by recent ack rate.",
    "mechanism": ["track ack flux", "prune idle links"],
    "tests": ["Sever 30% of links; fails if p99 doubles"],
}


@pytest.fixture
def fake_llm():
    return FakeLLM(
        analyze=ANALYZE,
        map=MAP,
        generate=GENERATE,
        critique=[
            {"novelty": 0.7, "rigor": 0.6, "fatal_flaws": [], "verdict": "survives", "reasoning": "ok"},
            {"novelty": 0.9, "rigor": 0.2, "fatal_flaws": ["incoherent"], "verdict": "refuted", "reasoning": "no"},
        ],
    )
