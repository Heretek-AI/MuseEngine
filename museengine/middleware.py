"""Wrap any agent function so it receives a MuseEngine scaffold first."""

from __future__ import annotations

import functools
from typing import Any, Callable, Dict, List, Optional, Union

from .engine import MuseEngine, Report

Messages = List[Dict[str, Any]]


class MuseMiddleware:
    """Decorator for ``fn(prompt: str, ...)`` or ``fn(messages: list[dict], ...)``.

    For a string prompt, the scaffold is prepended. For a message list, a system
    message holding the scaffold is inserted at the front (or merged into an
    existing leading system message). The latest user message is what gets
    analyzed. The report from the last call is kept on ``last_report``.
    """

    def __init__(self, engine: Optional[MuseEngine] = None, top_k: int = 3, return_report: bool = False):
        self.engine = engine or MuseEngine()
        self.top_k = top_k
        self.return_report = return_report
        self.last_report: Optional[Report] = None

    def __call__(self, agent_fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(agent_fn)
        def wrapped(prompt_or_messages: Union[str, Messages], *args: Any, **kwargs: Any) -> Any:
            if isinstance(prompt_or_messages, str):
                report = self.engine.imagine(prompt_or_messages, top_k=self.top_k)
                result = agent_fn(f"{report.scaffold()}\n\n{prompt_or_messages}", *args, **kwargs)
            elif isinstance(prompt_or_messages, list):
                user_text = _latest_user_text(prompt_or_messages)
                if not user_text:
                    raise ValueError("MuseMiddleware needs at least one user message with text")
                report = self.engine.imagine(user_text, top_k=self.top_k)
                result = agent_fn(_inject_system(prompt_or_messages, report.scaffold()), *args, **kwargs)
            else:
                raise TypeError("expected a str prompt or a list of message dicts")
            self.last_report = report
            return {"response": result, "report": report} if self.return_report else result

        return wrapped


def _latest_user_text(messages: Messages) -> str:
    for msg in reversed(messages):
        if msg.get("role") != "user":
            continue
        content = msg.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):  # content blocks
            return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _inject_system(messages: Messages, scaffold: str) -> Messages:
    if messages and messages[0].get("role") == "system" and isinstance(messages[0].get("content"), str):
        first = dict(messages[0], content=f"{messages[0]['content']}\n\n{scaffold}")
        return [first, *messages[1:]]
    return [{"role": "system", "content": scaffold}, *messages]
