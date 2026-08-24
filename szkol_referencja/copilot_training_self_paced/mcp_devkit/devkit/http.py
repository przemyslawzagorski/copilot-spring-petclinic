"""Wspolna warstwa HTTP: jeden klient, retry, twarde limity i ochrona przed SSRF."""

from __future__ import annotations

import ipaddress
import logging
import socket
import time
from typing import Any
from urllib.parse import urlparse

import httpx

from .config import settings

log = logging.getLogger("devkit.http")

USER_AGENT = "devkit-mcp/1.0 (+training; https://github.com/spring-projects/spring-petclinic)"
RETRY_STATUSES = {408, 425, 429, 500, 502, 503, 504}
MAX_ATTEMPTS = 3


class DevKitError(RuntimeError):
    """Blad domenowy - tresc trafia wprost do agenta, wiec musi byc dzialaniem do wykonania."""


_client: httpx.Client | None = None


def client() -> httpx.Client:
    """Leniwy singleton - jedno polaczenie keep-alive na caly proces serwera."""
    global _client
    if _client is None:
        _client = httpx.Client(
            timeout=httpx.Timeout(settings().http_timeout),
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        )
    return _client


def close() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def validate_public_url(url: str) -> str:
    """Blokuje SSRF: tylko http/https i tylko adresy publiczne.

    Bez tego `read_page("http://169.254.169.254/latest/meta-data/")` pozwolilby
    agentowi wyciagnac metadane instancji chmurowej. Guard mozna swiadomie
    wylaczyc przez DEVKIT_ALLOW_PRIVATE_URLS=true (np. do lokalnego Swaggera).
    """
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise DevKitError(f"Niedozwolony schemat URL: '{parsed.scheme or url}'. Uzyj http:// lub https://.")
    if not parsed.hostname:
        raise DevKitError(f"URL bez hosta: {url}")

    if settings().allow_private_urls:
        return url.strip()

    try:
        infos = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror as exc:
        raise DevKitError(f"Nie udalo sie rozwiazac hosta '{parsed.hostname}': {exc}") from exc

    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            raise DevKitError(
                f"URL '{url}' wskazuje na adres prywatny/lokalny ({ip}) - zablokowane (ochrona SSRF). "
                "Swiadomie odblokujesz to przez DEVKIT_ALLOW_PRIVATE_URLS=true."
            )
    return url.strip()


def request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    json_body: Any = None,
    data: Any = None,
    timeout: float | None = None,
    service: str = "http",
) -> httpx.Response:
    """Zapytanie z wykladniczym backoffem dla bledow przejsciowych i 429."""
    last_error: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client().request(
                method,
                url,
                headers=headers,
                params=params,
                json=json_body,
                data=data,
                timeout=timeout or settings().http_timeout,
            )
        except httpx.RequestError as exc:
            last_error = exc
            log.warning("%s: proba %s/%s nieudana (%s)", service, attempt, MAX_ATTEMPTS, exc)
            if attempt == MAX_ATTEMPTS:
                raise DevKitError(f"{service}: brak polaczenia po {MAX_ATTEMPTS} probach ({exc}).") from exc
            time.sleep(0.6 * attempt)
            continue

        if response.status_code in RETRY_STATUSES and attempt < MAX_ATTEMPTS:
            wait = float(response.headers.get("Retry-After", 0.8 * attempt))
            log.warning("%s: HTTP %s, ponawiam za %.1fs", service, response.status_code, wait)
            time.sleep(min(wait, 5.0))
            continue

        if response.status_code == 401:
            raise DevKitError(f"{service}: HTTP 401 - klucz API odrzucony lub brakujacy.")
        if response.status_code == 429:
            raise DevKitError(f"{service}: HTTP 429 - limit zapytan wyczerpany. Sprobuj pozniej lub dodaj klucz API.")
        if response.status_code >= 400:
            raise DevKitError(f"{service}: HTTP {response.status_code} - {response.text[:300]}")
        return response

    raise DevKitError(f"{service}: nieoczekiwany blad ({last_error}).")


def truncate(text: str, limit: int) -> tuple[str, bool]:
    """Przycina tekst do limitu znakow. Oszczednosc kontekstu to funkcja, nie detal."""
    if len(text) <= limit:
        return text, False
    cut = text[:limit]
    boundary = cut.rfind("\n")
    if boundary > limit * 0.6:
        cut = cut[:boundary]
    return cut + f"\n\n[...przyciete: {len(text) - len(cut)} znakow wiecej]", True
