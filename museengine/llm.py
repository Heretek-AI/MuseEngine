"""LLM plumbing: the callable protocol, JSON extraction, call budgets, and an
optional Anthropic adapter.

The engine is provider-neutral. Anything with the shape ``(prompt: str) -> str``
works as an LLM, so you can plug in any SDK, a local model, or a test double.
"""

from __future__ import annotations

import json
import re
from typing import Any, Callable, Dict, Optional

LLM = Callable[[str], str]


class LLMError(RuntimeError):
    """The model returned something we could not use."""


class BudgetExceeded(RuntimeError):
    """A hard call budget was hit."""


class CountingLLM:
    """Wraps an LLM, counts calls, and optionally enforces a hard ceiling."""

    def __init__(self, llm: LLM, max_calls: Optional[int] = None):
        self._llm = llm
        self.max_calls = max_calls
        self.calls = 0

    def __call__(self, prompt: str) -> str:
        if self.max_calls is not None and self.calls >= self.max_calls:
            raise BudgetExceeded(f"LLM call budget of {self.max_calls} exhausted")
        self.calls += 1
        return self._llm(prompt)


_JSON_INSTRUCTION = (
    "\n\nRespond with a single JSON object and nothing else. "
    "No markdown fences, no commentary."
)


def _extract_json_object(text: str) -> Dict[str, Any]:
    text = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object found")
    value = json.loads(text[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value is not an object")
    return value


def complete_json(llm: LLM, prompt: str, retries: int = 1) -> Dict[str, Any]:
    """Ask for JSON, parse it, and retry with the parse error if it is malformed."""
    attempt_prompt = prompt + _JSON_INSTRUCTION
    last_error: Optional[Exception] = None
    for _ in range(retries + 1):
        raw = llm(attempt_prompt)
        try:
            return _extract_json_object(raw)
        except (ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            attempt_prompt = (
                prompt
                + _JSON_INSTRUCTION
                + f"\n\nYour previous reply could not be parsed ({exc}). Reply again with valid JSON only."
            )
    raise LLMError(f"model did not return valid JSON: {last_error}")


def clamp01(value: Any, default: float = 0.0) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return default


def anthropic_llm(
    model: str = "claude-opus-5-5",
    effort: str = "medium",
    max_tokens: int = 16000,
    system: Optional[str] = None,
    client: Any = None,
) -> LLM:
    """Build an LLM callable backed by the Anthropic Messages API.

    Requires ``pip install anthropic`` and credentials in the environment
    (``ANTHROPIC_API_KEY`` or an ``ant auth login`` profile). Server-side
    refusal fallbacks are enabled so a declined request is retried on a
    fallback model instead of silently returning nothing.
    """
    if client is None:
        import anthropic  # optional dependency

        client = anthropic.Anthropic()

    def call(prompt: str) -> str:
        kwargs: Dict[str, Any] = dict(
            model=model,
            max_tokens=max_tokens,
            output_config={"effort": effort},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            messages=[{"role": "user", "content": prompt}],
        )
        if system:
            kwargs["system"] = system
        response = client.beta.messages.create(**kwargs)
        if response.stop_reason == "refusal":
            raise LLMError("model declined the request")
        return "".join(b.text for b in response.content if b.type == "text")

    return call
