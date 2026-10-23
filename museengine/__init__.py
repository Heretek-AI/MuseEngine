"""MuseEngine: structured cross-domain ideation for LLM agents."""

from .agent import MuseAgent, RunResult
from .archetypes import Archetype, load_archetypes, load_default_archetypes
from .engine import Analogy, Candidate, MuseEngine, ProblemStructure, Report, pareto_frontier
from .evaluation import EvalResult, run_ab_eval, sign_test
from .governance import (
    GovernanceError,
    Governor,
    KillSwitch,
    Policy,
    ProposedAction,
    console_approver,
    deny_all,
)
from .llm import LLM, BudgetExceeded, CountingLLM, LLMError, anthropic_llm, complete_json
from .memory import Episode, MemoryStore
from .middleware import MuseMiddleware

__all__ = [
    "Analogy", "Archetype", "BudgetExceeded", "Candidate", "CountingLLM", "Episode", "EvalResult",
    "GovernanceError", "Governor", "KillSwitch", "LLM", "LLMError", "MemoryStore", "MuseAgent",
    "MuseEngine", "MuseMiddleware", "Policy", "ProblemStructure", "ProposedAction", "Report",
    "RunResult", "anthropic_llm", "complete_json", "console_approver", "deny_all",
    "load_archetypes", "load_default_archetypes", "pareto_frontier", "run_ab_eval", "sign_test",
]
