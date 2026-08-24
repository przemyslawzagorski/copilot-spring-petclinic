"""Wyszukiwarka dla agenta - Tavily, z lancuchem fallbackow.

Kolejnosc: Tavily (najlepszy kontekst dla RAG) -> Jina Search -> DuckDuckGo HTML.
Ostatni krok dziala bez zadnego klucza, wiec demo zawsze da sie uruchomic,
ale zwraca same tytuly i krotkie snippety - dlatego jest oznaczony `degraded`.
"""

from __future__ import annotations

import html
import logging
import re
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from .config import settings
from .http import DevKitError, request

log = logging.getLogger("devkit.search")

TAVILY_ENDPOINT = "https://api.tavily.com/search"
JINA_SEARCH_ENDPOINT = "https://s.jina.ai/"
DDG_ENDPOINT = "https://html.duckduckgo.com/html/"

_DDG_RESULT_RE = re.compile(
    r'<a[^>]+class="result__a"[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>'
    r'(?:.*?class="result__snippet"[^>]*>(?P<snippet>.*?)</a>)?',
    re.DOTALL,
)
_TAG_RE = re.compile(r"<[^>]+>")


def _clean(text: str) -> str:
    return html.unescape(_TAG_RE.sub("", text or "")).strip()


def _tavily(query: str, max_results: int, depth: str, include_domains: list[str] | None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "query": query,
        "max_results": max_results,
        "search_depth": "advanced" if depth == "advanced" else "basic",
        "include_answer": "basic",
    }
    if include_domains:
        body["include_domains"] = include_domains

    response = request(
        "POST",
        TAVILY_ENDPOINT,
        headers={
            "Authorization": f"Bearer {settings().tavily_api_key}",
            "Content-Type": "application/json",
        },
        json_body=body,
        service="tavily",
    )
    data = response.json()
    return {
        "provider": "tavily",
        "degraded": False,
        "answer": data.get("answer") or "",
        "results": [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": (item.get("content") or "")[:1200],
                "score": round(float(item.get("score", 0.0)), 4),
            }
            for item in data.get("results", [])[:max_results]
        ],
    }


def _jina(query: str, max_results: int) -> dict[str, Any]:
    response = request(
        "GET",
        JINA_SEARCH_ENDPOINT,
        params={"q": query},
        headers={
            "Authorization": f"Bearer {settings().jina_api_key}",
            "Accept": "application/json",
            "X-Respond-With": "no-content",
        },
        service="jina-search",
    )
    data = response.json().get("data", []) or []
    return {
        "provider": "jina-search",
        "degraded": False,
        "answer": "",
        "results": [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": (item.get("description") or item.get("content") or "")[:1200],
                "score": None,
            }
            for item in data[:max_results]
        ],
    }


def _duckduckgo(query: str, max_results: int) -> dict[str, Any]:
    response = request(
        "POST",
        DDG_ENDPOINT,
        data={"q": query},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) devkit-mcp/1.0",
        },
        service="duckduckgo",
    )
    results = []
    for match in _DDG_RESULT_RE.finditer(response.text):
        href = html.unescape(match.group("href"))
        if "duckduckgo.com/l/" in href:  # DDG opakowuje linki w redirect
            target = parse_qs(urlparse(href).query).get("uddg", [])
            href = unquote(target[0]) if target else href
        if not href.startswith("http"):
            continue
        results.append(
            {
                "title": _clean(match.group("title")),
                "url": href,
                "snippet": _clean(match.group("snippet") or "")[:600],
                "score": None,
            }
        )
        if len(results) >= max_results:
            break
    return {"provider": "duckduckgo-html", "degraded": True, "answer": "", "results": results}


def web_search(
    query: str,
    *,
    max_results: int = 5,
    depth: str = "basic",
    include_domains: list[str] | None = None,
) -> dict[str, Any]:
    """Szuka w sieci najlepszym dostepnym providerem i normalizuje wynik."""
    query = query.strip()
    if not query:
        raise DevKitError("Pusta fraza wyszukiwania.")
    max_results = max(1, min(max_results, 15))
    s = settings()
    errors: list[str] = []

    if s.tavily_api_key:
        try:
            return {"query": query, **_tavily(query, max_results, depth, include_domains)}
        except DevKitError as exc:
            errors.append(f"tavily: {exc}")
            log.warning("Tavily zawiodl, schodze nizej: %s", exc)

    if s.jina_api_key:
        try:
            return {"query": query, "notes": errors, **_jina(query, max_results)}
        except DevKitError as exc:
            errors.append(f"jina: {exc}")
            log.warning("Jina Search zawiodl, schodze nizej: %s", exc)

    try:
        result = _duckduckgo(query, max_results)
    except DevKitError as exc:
        errors.append(f"duckduckgo: {exc}")
        raise DevKitError("Zaden provider wyszukiwania nie odpowiedzial: " + " | ".join(errors)) from exc

    if include_domains:
        allowed = tuple(domain.lower() for domain in include_domains)
        result["results"] = [
            item for item in result["results"] if any(domain in item["url"].lower() for domain in allowed)
        ]
    result["notes"] = errors + [
        "Fallback DuckDuckGo: brak rankingu i pelnych snippetow. Ustaw TAVILY_API_KEY dla wynikow klasy RAG."
    ]
    return {"query": query, **result}
