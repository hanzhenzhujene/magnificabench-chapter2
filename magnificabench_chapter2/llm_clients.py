from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass


class LLMClientError(RuntimeError):
    pass


@dataclass
class ChatClient:
    provider: str
    model: str
    temperature: float = 0.0
    max_tokens: int = 900

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if self.provider == "demo":
            return demo_response(user_prompt)
        if self.provider in {"openai", "openai-compatible"}:
            return openai_compatible_chat(
                provider=self.provider,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        if self.provider == "anthropic":
            return anthropic_chat(
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        if self.provider == "ollama":
            return ollama_chat(
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=self.temperature,
            )
        raise LLMClientError(f"unknown provider: {self.provider}")


def post_json(url: str, payload: dict, headers: dict[str, str], timeout: int = 120) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise LLMClientError(f"{url} returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise LLMClientError(f"could not reach {url}: {exc}") from exc


def openai_compatible_chat(
    provider: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
) -> str:
    if provider == "openai":
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        api_key = os.environ.get("OPENAI_API_KEY")
    else:
        base_url = os.environ.get("OPENAI_COMPATIBLE_BASE_URL", "http://localhost:8000/v1").rstrip("/")
        api_key = os.environ.get("OPENAI_COMPATIBLE_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if provider == "openai" and not api_key:
        raise LLMClientError("OPENAI_API_KEY is required for provider=openai")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    data = post_json(f"{base_url}/chat/completions", payload, headers)
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMClientError(f"unexpected OpenAI-compatible response shape: {data}") from exc


def anthropic_chat(model: str, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise LLMClientError("ANTHROPIC_API_KEY is required for provider=anthropic")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    data = post_json(f"{base_url}/v1/messages", payload, headers)
    try:
        parts = data["content"]
        return "".join(part.get("text", "") for part in parts if part.get("type") == "text")
    except (KeyError, TypeError) as exc:
        raise LLMClientError(f"unexpected Anthropic response shape: {data}") from exc


def ollama_chat(model: str, system_prompt: str, user_prompt: str, temperature: float) -> str:
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {"temperature": temperature},
    }
    data = post_json(f"{base_url}/api/chat", payload, {"Content-Type": "application/json"})
    try:
        return data["message"]["content"]
    except (KeyError, TypeError) as exc:
        raise LLMClientError(f"unexpected Ollama response shape: {data}") from exc


def demo_response(user_prompt: str) -> str:
    lowered = user_prompt.lower()
    pieces = [
        "A Chapter 2 answer should begin from inherent human dignity rather than efficiency alone.",
        "It should connect rights, common good, participation, solidarity, and social justice to the concrete AI or digital system.",
    ]
    if "platform" in lowered or "algorithm" in lowered:
        pieces.append(
            "If platform or algorithmic power is opaque, the remedy should include transparency, accountability, affected-community participation, independent checks, and appeal or recourse."
        )
    if "data" in lowered or "compute" in lowered or "infrastructure" in lowered:
        pieces.append(
            "Data, algorithms, platforms, infrastructure, and patents can be digital goods when concentrated control blocks participation."
        )
    if "migrant" in lowered or "refugee" in lowered or "asylum" in lowered:
        pieces.append(
            "Migrants and refugees should not be treated only as risk classes; dignity, due process, safe routes, and integration matter."
        )
    if "environment" in lowered or "ecology" in lowered or "future generations" in lowered:
        pieces.append(
            "Integral development also requires care for the common home and future generations."
        )
    pieces.append(
        "A strong answer should end with concrete governance mechanisms such as audit, human review, data access where appropriate, monitoring, and repair."
    )
    return " ".join(pieces)
