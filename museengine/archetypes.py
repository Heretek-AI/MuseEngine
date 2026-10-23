"""The cross-domain analogy library.

Archetypes are hand-curated descriptions of mechanisms from other fields. They
are prompts for analogy, not knowledge the engine "has": the LLM decides whether
any of them actually fits a problem, and the critic decides whether the result
holds up.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List

_LIBRARY_PATH = Path(__file__).with_name("archetypes.json")


@dataclass(frozen=True)
class Archetype:
    id: str
    name: str
    source_domain: str
    summary: str
    mechanisms: List[str] = field(default_factory=list)
    invariants: List[str] = field(default_factory=list)
    operators: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Archetype":
        return cls(**{k: data[k] for k in cls.__dataclass_fields__ if k in data})

    def brief(self) -> str:
        """Compact text used inside prompts."""
        return (
            f"[{self.id}] {self.name} ({self.source_domain})\n"
            f"  Summary: {self.summary}\n"
            f"  Mechanisms: {'; '.join(self.mechanisms)}\n"
            f"  Transferable operators: {'; '.join(self.operators)}\n"
            f"  Known failure modes: {'; '.join(self.failure_modes)}"
        )

    def search_text(self) -> str:
        return " ".join(
            [self.name, self.source_domain, self.summary, *self.mechanisms, *self.operators, *self.tags]
        ).lower()


def load_default_archetypes() -> List[Archetype]:
    with _LIBRARY_PATH.open(encoding="utf-8") as fh:
        return [Archetype.from_dict(d) for d in json.load(fh)]


def load_archetypes(path: str | Path) -> List[Archetype]:
    with Path(path).open(encoding="utf-8") as fh:
        return [Archetype.from_dict(d) for d in json.load(fh)]


def index_by_id(archetypes: Iterable[Archetype]) -> Dict[str, Archetype]:
    return {a.id: a for a in archetypes}
