"""Jina AI Reader - dowolny URL zamieniony na czysty Markdown dla modelu.

r.jina.ai dziala **bez klucza** (niski limit + odpowiedzi z cache). JINA_API_KEY
podnosi limity i wylacza cache (`x-no-cache`).
"""

from __future__ import annotations

import logging
import re
from typing import Any

from .config import settings
from .http import DevKitError, request, truncate, validate_public_url

log = logging.getLogger("devkit.readers")

READER_ENDPOINT = "https://r.jina.ai/"
_HEADER_RE = re.compile(r"^(Title|URL Source|Published Time|Warning|Markdown Content):\s*(.*)$")


def _headers(*, with_links: bool, with_images: bool, no_cache: bool) -> dict[str, str]:
    s = settings()
    headers = {"X-Return-Format": "markdown", "Accept": "text/plain"}
    if s.jina_api_key:
        headers["Authorization"] = f"Bearer {s.jina_api_key}"
        if no_cache:
            headers["x-no-cache"] = "true"
    headers["X-With-Links-Summary"] = "true" if with_links else "false"
    headers["X-With-Images-Summary"] = "true" if with_images else "false"
    return headers


def _parse(raw: str) -> dict[str, str]:
    """Reader zwraca naglowki `Title:` / `URL Source:` przed trescia - rozdzielamy je."""
    meta: dict[str, str] = {}
    lines = raw.splitlines()
    body_start = 0
    for index, line in enumerate(lines[:12]):
        match = _HEADER_RE.match(line)
        if match:
            key, value = match.group(1), match.group(2)
            if key == "Markdown Content":
                body_start = index + 1
                break
            meta[key.lower().replace(" ", "_")] = value.strip()
            body_start = index + 1
        elif line.strip() == "" and meta:
            body_start = index + 1
    return {"meta": meta, "body": "\n".join(lines[body_start:]).strip()}  # type: ignore[dict-item]


def read_page(
    url: str,
    *,
    max_chars: int | None = None,
    with_links: bool = False,
    with_images: bool = False,
    no_cache: bool = False,
) -> dict[str, Any]:
    """Pobiera strone i zwraca czysty Markdown wraz z metadanymi."""
    safe_url = validate_public_url(url)
    limit = max_chars or settings().max_page_chars

    response = request(
        "GET",
        READER_ENDPOINT + safe_url,
        headers=_headers(with_links=with_links, with_images=with_images, no_cache=no_cache),
        service="jina-reader",
    )
    parsed = _parse(response.text)
    meta: dict[str, str] = parsed["meta"]  # type: ignore[assignment]
    body: str = parsed["body"]  # type: ignore[assignment]
    if not body:
        raise DevKitError(f"Jina Reader nie zwrocil tresci dla {safe_url} (strona pusta lub zablokowana).")

    content, was_truncated = truncate(body, limit)
    return {
        "url": meta.get("url_source", safe_url),
        "title": meta.get("title", ""),
        "published": meta.get("published_time", ""),
        "content": content,
        "chars": len(body),
        "truncated": was_truncated,
        "cached": "cached snapshot" in meta.get("warning", "").lower(),
        "provider": "jina-reader" + ("" if settings().jina_api_key else " (anonimowo)"),
    }
