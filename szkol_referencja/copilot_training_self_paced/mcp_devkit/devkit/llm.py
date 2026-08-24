"""Delegowanie podzadan do szybkiego, taniego modelu (Groq) + opcjonalnie Hugging Face.

Sens biznesowy: glowny agent (Claude) nie musi wciagac 30 tysiecy tokenow logow do
swojego okna kontekstu, zeby je sklasyfikowac. Wysyla je do Groqa (setki tokenow/s),
dostaje 10-liniowy werdykt i pracuje dalej. To jest ekonomia kontekstu w praktyce.
"""

from __future__ import annotations

import logging
from typing import Any

from .config import settings
from .http import DevKitError, request, truncate

log = logging.getLogger("devkit.llm")

MAX_INPUT_CHARS = 60000


def available() -> bool:
    return bool(settings().groq_api_key)


def _require_key() -> str:
    key = settings().groq_api_key
    if not key:
        raise DevKitError(
            "Brak GROQ_API_KEY - delegowanie do szybkiego modelu jest wylaczone. "
            "Zaloz darmowy klucz na https://console.groq.com i dodaj go do mcp_devkit/.env."
        )
    return key


def complete(
    prompt: str,
    *,
    system: str | None = None,
    model: str | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.2,
) -> dict[str, Any]:
    """Jedno wywolanie chat-completions na Groq (API zgodne z OpenAI)."""
    key = _require_key()
    s = settings()
    chosen = model or s.groq_model
    prompt, _ = truncate(prompt, MAX_INPUT_CHARS)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = request(
            "POST",
            f"{s.groq_base_url}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json_body={
                "model": chosen,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            service="groq",
            timeout=max(s.http_timeout, 60),
        )
    except DevKitError as exc:
        if "model" in str(exc).lower() and "not" in str(exc).lower():
            raise DevKitError(
                f"{exc}\nDostepne modele sprawdzisz w resource `devkit://llm/models` "
                "lub ustaw inny w GROQ_MODEL (np. llama-3.1-8b-instant)."
            ) from exc
        raise

    data = response.json()
    choice = (data.get("choices") or [{}])[0]
    usage = data.get("usage", {})
    return {
        "model": data.get("model", chosen),
        "output": (choice.get("message") or {}).get("content", "").strip(),
        "finish_reason": choice.get("finish_reason", ""),
        "usage": {
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "total_time_s": round(float(usage.get("total_time", 0.0)), 3),
        },
    }


def list_models() -> list[dict[str, Any]]:
    key = _require_key()
    s = settings()
    response = request(
        "GET", f"{s.groq_base_url}/models", headers={"Authorization": f"Bearer {key}"}, service="groq"
    )
    return [
        {"id": item.get("id"), "context_window": item.get("context_window"), "owned_by": item.get("owned_by")}
        for item in response.json().get("data", [])
    ]


SYNTHESIS_SYSTEM = (
    "Jestes precyzyjnym asystentem researchu dla programisty. Odpowiadasz WYLACZNIE na podstawie "
    "dostarczonych zrodel. Kazde twierdzenie oznaczasz numerem zrodla w nawiasach kwadratowych, np. [2]. "
    "Jesli zrodla nie odpowiadaja na pytanie, mowisz to wprost. Bez lania wody, bez powtarzania pytania."
)


def synthesize(question: str, sources: list[dict[str, Any]], *, model: str | None = None) -> dict[str, Any]:
    """Buduje odpowiedz RAG z ponumerowanych zrodel (z wymuszonym cytowaniem)."""
    blocks = []
    for index, source in enumerate(sources, start=1):
        label = source.get("title") or source.get("source") or source.get("url") or f"zrodlo {index}"
        origin = source.get("url") or source.get("source") or ""
        blocks.append(f"[{index}] {label} ({origin})\n{source.get('text', '')}")
    context, _ = truncate("\n\n---\n\n".join(blocks), MAX_INPUT_CHARS)

    prompt = (
        f"PYTANIE:\n{question}\n\n"
        f"ZRODLA:\n{context}\n\n"
        "Odpowiedz zwiezle (maks. 12 zdan), z cytowaniami [n]. Na koncu dodaj linie "
        "'Pewnosc: wysoka|srednia|niska' wraz z jednozdaniowym uzasadnieniem."
    )
    result = complete(prompt, system=SYNTHESIS_SYSTEM, model=model, max_tokens=1200, temperature=0.1)
    result["sources_used"] = len(sources)
    return result


def hf_infer(model: str, inputs: Any, *, parameters: dict[str, Any] | None = None) -> Any:
    """Surowe wywolanie Hugging Face Inference API (OCR, ASR, klasyfikacja obrazu itd.)."""
    s = settings()
    if not s.hf_api_key:
        raise DevKitError(
            "Brak HF_API_KEY - narzedzie hf_infer jest wylaczone. "
            "Token wygenerujesz na https://huggingface.co/settings/tokens."
        )
    payload: dict[str, Any] = {"inputs": inputs}
    if parameters:
        payload["parameters"] = parameters
    response = request(
        "POST",
        f"{s.hf_api_url.rstrip('/')}/{model}",
        headers={"Authorization": f"Bearer {s.hf_api_key}", "Content-Type": "application/json"},
        json_body=payload,
        service="huggingface",
        timeout=max(s.http_timeout, 60),
    )
    try:
        return response.json()
    except ValueError:
        return {"raw": response.text[:2000]}
