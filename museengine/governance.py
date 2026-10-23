"""Guardrails for the autonomous loop.

Every action the agent wants to take goes through ``Governor.authorize`` first.
The governor enforces an allowlist, a step budget, a kill switch, and human
approval for actions you mark as needing it. Every decision, allowed or not,
goes to the audit log together with what the action actually did.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, FrozenSet, Optional

from .memory import MemoryStore


class GovernanceError(RuntimeError):
    """An action was refused."""


@dataclass(frozen=True)
class ProposedAction:
    name: str
    reason: str
    payload: Dict[str, Any] = field(default_factory=dict)


Approver = Callable[[ProposedAction], bool]


def deny_all(action: ProposedAction) -> bool:
    return False


def console_approver(action: ProposedAction) -> bool:
    """Ask on stdin. Anything but an explicit 'y' is a no."""
    print(f"\nThe agent wants to: {action.name}\n  Why: {action.reason}\n  Details: {action.payload}")
    return input("Allow? [y/N] ").strip().lower() == "y"


class KillSwitch:
    """Trip it in code with ``trip()``, or by creating the file at ``path``."""

    def __init__(self, path: Optional[str | Path] = None):
        self.path = Path(path) if path else None
        self._tripped = False

    def trip(self) -> None:
        self._tripped = True

    def tripped(self) -> bool:
        return self._tripped or bool(self.path and self.path.exists())


@dataclass
class Policy:
    allowed_actions: FrozenSet[str] = frozenset({"explore", "reflect", "propose_goal", "adopt_goal"})
    # Taking on a goal the agent invented itself needs a human by default.
    approval_required: FrozenSet[str] = frozenset({"adopt_goal"})
    max_steps: int = 10


class Governor:
    def __init__(
        self,
        memory: MemoryStore,
        policy: Optional[Policy] = None,
        approver: Approver = deny_all,
        kill_switch: Optional[KillSwitch] = None,
    ):
        self.memory = memory
        self.policy = policy or Policy()
        self.approver = approver
        self.kill_switch = kill_switch or KillSwitch()
        self.steps_taken = 0

    def should_stop(self) -> Optional[str]:
        if self.kill_switch.tripped():
            return "kill switch tripped"
        if self.steps_taken >= self.policy.max_steps:
            return f"step budget of {self.policy.max_steps} reached"
        return None

    def authorize(self, action: ProposedAction) -> None:
        stop = self.should_stop()
        if stop:
            self._deny(action, stop)
        if action.name not in self.policy.allowed_actions:
            self._deny(action, "action not on the allowlist")
        if action.name in self.policy.approval_required and not self.approver(action):
            self._deny(action, "human approval not given")
        self.steps_taken += 1
        self.memory.audit(action.name, "allowed", {"reason": action.reason, "payload": action.payload})

    def record_outcome(self, action: ProposedAction, effect: Dict[str, Any]) -> None:
        """Log what the action actually did (not what it was supposed to do)."""
        self.memory.audit(action.name, "completed", effect)

    def record_failure(self, action: ProposedAction, error: Exception) -> None:
        self.memory.audit(action.name, "failed", {"error": f"{type(error).__name__}: {error}"})

    def _deny(self, action: ProposedAction, why: str) -> None:
        self.memory.audit(action.name, "denied", {"why": why, "reason": action.reason})
        raise GovernanceError(f"{action.name}: {why}")
