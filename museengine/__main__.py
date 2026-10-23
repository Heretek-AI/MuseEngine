"""Command line entry point.

    python -m museengine imagine "problem text" [--offline] [--memory mind.db]
    python -m museengine agent --memory mind.db --goal "problem" [--max-steps 5]
    python -m museengine eval problems.txt [--judge-model claude-sonnet-5-5]

Without ``--offline`` the commands call the Anthropic API (``pip install anthropic``
and set credentials). Create the file named by ``--kill-file`` to stop the agent.
"""

from __future__ import annotations

import argparse
import json
import sys

from .agent import MuseAgent
from .engine import MuseEngine
from .evaluation import run_ab_eval
from .governance import Governor, KillSwitch, Policy, console_approver
from .llm import anthropic_llm
from .memory import MemoryStore


def _cmd_imagine(args: argparse.Namespace) -> int:
    memory = MemoryStore(args.memory) if args.memory else None
    llm = None if args.offline else anthropic_llm(model=args.model)
    report = MuseEngine(llm=llm, memory=memory).imagine(args.problem, top_k=args.top_k)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, default=str))
    else:
        print(report.scaffold())
        print(f"\n[mode={report.mode}, llm_calls={report.llm_calls}, "
              f"candidates={len(report.candidates)}, survived={len(report.frontier)}]")
    return 0


def _cmd_agent(args: argparse.Namespace) -> int:
    memory = MemoryStore(args.memory)
    engine = MuseEngine(llm=None if args.offline else anthropic_llm(model=args.model), memory=memory)
    governor = Governor(
        memory,
        Policy(max_steps=args.max_steps),
        approver=console_approver,
        kill_switch=KillSwitch(args.kill_file),
    )
    agent = MuseAgent(engine, memory, governor)
    for goal in args.goal or []:
        agent.add_goal(goal)
    result = agent.run()
    for step in result.steps:
        print(f"- {step.action}: {json.dumps(step.effect, default=str)}")
    print(f"Stopped: {result.stopped_because}")
    return 0


def _cmd_eval(args: argparse.Namespace) -> int:
    with open(args.problems, encoding="utf-8") as fh:
        problems = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    solver = anthropic_llm(model=args.model)
    judge = anthropic_llm(model=args.judge_model)
    engine = MuseEngine(llm=solver, critic=judge)
    result = run_ab_eval(problems, solver, judge, engine, seed=args.seed,
                         on_pair=lambda p: print(f"- {p.outcome:8} {p.problem[:70]}"))
    print(result.summary())
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="museengine")
    parser.add_argument("--model", default="claude-opus-5-5")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("imagine", help="run one ideation cycle")
    p.add_argument("problem")
    p.add_argument("--offline", action="store_true", help="no LLM; keyword suggestions only")
    p.add_argument("--memory")
    p.add_argument("--top-k", type=int, default=3)
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=_cmd_imagine)

    p = sub.add_parser("agent", help="run the governed autonomous loop")
    p.add_argument("--memory", required=True)
    p.add_argument("--goal", action="append")
    p.add_argument("--max-steps", type=int, default=5)
    p.add_argument("--kill-file", default="STOP")
    p.add_argument("--offline", action="store_true")
    p.set_defaults(fn=_cmd_agent)

    p = sub.add_parser("eval", help="blinded A/B eval of the scaffold")
    p.add_argument("problems", help="text file, one problem per line")
    p.add_argument("--judge-model", default="claude-sonnet-5-5")
    p.add_argument("--seed", type=int, default=0)
    p.set_defaults(fn=_cmd_eval)

    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
