# MuseEngine

MuseEngine sits in front of an LLM agent and pushes it toward cross-domain ideas. It looks for mechanisms from other fields (slime-mold networks, immune selection, estuary flushing, and so on) that structurally fit your problem. It turns each fit into a concrete candidate with tests that could break it, has a separate adversarial critic try to refute each candidate, and hands the survivors to your agent as a short scaffold.

It also includes a small autonomous loop. That loop is governed: every step goes through an allowlist, a step budget and a kill switch, and taking on a goal the agent proposed itself needs human approval.

> **v0.2 is a rewrite.** The original upload, kept in [`legacy/`](legacy/), never called a model. Its "cognition" was keyword matching and string templates, and its benchmark was rigged; [`legacy/README.md`](legacy/README.md) has the details. This version uses an LLM for every reasoning step, and it comes with an evaluation that can actually show the scaffold doesn't help.

## Install

```bash
pip install -e ".[anthropic,dev]"   # the core has no dependencies; anthropic is optional
pytest -q
```

## Use

```python
from museengine import MuseEngine, MuseMiddleware, MemoryStore, anthropic_llm

engine = MuseEngine(
    llm=anthropic_llm(),                                # any (prompt: str) -> str callable works
    critic=anthropic_llm(model="claude-sonnet-5-5"),    # optional: a different model as critic
    memory=MemoryStore("mind.db"),                      # optional: recall past problems
)

report = engine.imagine("Design a rate limiter for tenants with wildly different burst patterns")
for c in report.frontier:
    print(c.title, c.novelty, c.rigor, c.tests[0])

# Or wrap an existing agent: it gets the scaffold as a system message.
@MuseMiddleware(engine)
def agent(messages):
    ...
```

From the command line:

```bash
python -m museengine imagine "your problem"            # needs Anthropic credentials
python -m museengine imagine "your problem" --offline  # no model: keyword suggestions only
python -m museengine agent --memory mind.db --goal "your problem" --max-steps 5
python -m museengine eval examples/problems.txt
```

## How it works

| Step | What happens |
|---|---|
| Analyze | The LLM describes the problem's structure: tensions, hard constraints, and how naive fixes fail. |
| Map | The LLM picks archetypes from [`archetypes.json`](museengine/archetypes.json) whose mechanisms fit, says what maps to what and where the analogy breaks. It may pick none. Unknown ids are dropped. Related past problems from memory are included as context. |
| Generate | Each analogy becomes a candidate design or hypothesis with 2–4 tests that name the observation that would count against it. |
| Critique | A separate adversarial prompt (optionally a different model) scores novelty and rigor and refutes weak candidates. A candidate with no tests can't survive. |
| Select | Survivors on the Pareto frontier of (novelty, rigor) go into the scaffold. |

**Offline mode** (`llm=None`) ranks archetypes by word overlap and labels them as unchecked suggestions. It produces no candidates and no scores, because without a model there is nothing to base them on.

## The autonomous loop

`MuseAgent` picks its next step with a fixed rule you can read in [`agent.py`](museengine/agent.py):

1. **explore** the next queued goal.
2. **reflect** once enough new episodes have built up, saving lessons as notes.
3. **propose_goal**: draft one follow-up when past problems are still open. Drafting has no side effects.
4. **adopt_goal**: queue that draft. This step **requires approval by default**, and the approver sees the exact text.
5. Otherwise **stop**. When idle, it stops rather than inventing work.

`Governor` enforces `Policy.allowed_actions`, `Policy.approval_required`, `Policy.max_steps` and a `KillSwitch` (call `trip()`, or create the file passed as `--kill-file`). It writes every allow, deny, completion and failure, with the action's real effect, to the SQLite audit log. The loop's only side effects are writes to its own memory database. It has no tools, no network access beyond the LLM, and no shell.

## Does it help? Measure it

`run_ab_eval` asks the same solver each problem twice, once with the scaffold and once without. A judge compares the two answers twice with the order swapped, and a win only counts if both verdicts agree. The output is wins/losses/ties and an exact sign test:

```
6 problems: scaffold won 3, lost 1, tied 2 (win rate among decided pairs 75%, two-sided sign test p=0.625)
```

(Illustrative format only; no real run is checked in.) Use a different model as judge, use more problems than the six in `examples/`, and expect the honest answer to sometimes be "no effect."

## Layout

```
museengine/   engine, llm, archetypes, memory, middleware, governance, agent, evaluation, CLI
tests/        offline test suite using a scripted fake LLM
legacy/       the original upload, unchanged, plus notes on what was wrong with it
```
