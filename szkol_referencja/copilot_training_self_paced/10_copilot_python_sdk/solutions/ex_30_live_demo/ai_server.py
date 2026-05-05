"""
Ex 30 — AI Triage Asystent (Live Demo) — serwer FastAPI + GitHub Copilot SDK.

Scenariusz biznesowy:
    Zakładka „AI Asystent" w PetClinic pozwala właścicielowi zwierzęcia opisać
    objawy i otrzymać rekomendację odpowiedniego weterynarza — bazując na ŻYWYCH
    danych z uruchomionego Spring API (GET /vets).

Architektura:
    Spring PetClinic :8080
        └─► POST /api/ai/chat  (proxy)
                └─► Python FastAPI :8081  POST /chat
                        └─► Copilot SDK + custom tools
                                ├─ get_available_vets  → GET :8080/vets
                                ├─ get_visit_load      → symulowane dane
                                └─ search_pet_owners   → GET :8080/owners?lastName=...

Uruchomienie:
    pip install fastapi "uvicorn[standard]" httpx
    uvicorn ai_server:app --port 8081 --reload

Bezpieczeństwo:
    - Serwer nasłuchuje wyłącznie na localhost (127.0.0.1).
    - CORS ograniczony do :8080 (Spring PetClinic).
    - Żadne poświadczenia nie są logowane ani ujawniane.
    - Wejście od użytkownika jest przycinane do 500 znaków.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ─── Lokalizacja _common.py (2 poziomy wyżej: solutions/) ───────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import ensure_copilot_cli_on_path  # noqa: E402

from copilot import CopilotClient, SubprocessConfig, define_tool
from copilot.generated.session_events import AssistantMessageData, SessionIdleData
from copilot.session import PermissionHandler

# ─── Konfiguracja ────────────────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO, format="[ai_server] %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PETCLINIC_BASE = os.getenv("PETCLINIC_BASE_URL", "http://localhost:8080")
MAX_MESSAGE_LEN = 500  # ochrona przed prompt injection / zbyt długimi promptami
COPILOT_MODEL = os.getenv("COPILOT_MODEL", "auto")

# ─── Modele FastAPI ──────────────────────────────────────────────────────────


class ChatRequest(BaseModel):
    """Żądanie do endpointu /chat."""

    message: str = Field(..., min_length=1, max_length=MAX_MESSAGE_LEN)


class ChatResponse(BaseModel):
    """Odpowiedź z endpointu /chat."""

    reply: str
    tools_called: list[str]


# ─── Pydantic modele dla custom tools ────────────────────────────────────────


class GetVetsParams(BaseModel):
    """Parametry narzędzia get_available_vets."""

    specialty_hint: str | None = Field(
        default=None,
        description=(
            "Opcjonalne słowo kluczowe specjalizacji (np. 'dentistry', 'surgery', "
            "'radiology'). Gdy None — zwróć wszystkich weterynarzy."
        ),
    )


class VisitLoadParams(BaseModel):
    """Parametry narzędzia get_visit_load."""

    vet_id: int = Field(description="Identyfikator weterynarza w PetClinic.")


class SearchOwnersParams(BaseModel):
    """Parametry narzędzia search_pet_owners."""

    last_name: str = Field(
        description="Nazwisko właściciela do wyszukania (może być częściowe)."
    )


# ─── Custom tools (rejestrowane w sesji Copilot SDK) ─────────────────────────

_tools_called: list[str] = []  # zbieramy dla ChatResponse (per-sesja, reset w /chat)


@define_tool(
    name="get_available_vets",
    description=(
        "Pobiera listę weterynarzy z ŻYWEGO Spring PetClinic API (/vets). "
        "Zwraca imiona, specjalizacje i dostępność. Użyj aby dopasować weterynarza "
        "do opisanych objawów zwierzęcia."
    ),
    params_type=GetVetsParams,
    skip_permission=True,
)
async def get_available_vets(params: GetVetsParams, _inv) -> str:
    _tools_called.append("get_available_vets")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{PETCLINIC_BASE}/vets")
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()
    except httpx.HTTPError as exc:
        log.warning("Błąd podczas pobierania weterynarzy: %s", exc)
        return "Nie udało się pobrać danych weterynarzy z PetClinic API."

    vet_list: list[dict] = data.get("vetList", [])
    if not vet_list:
        return "Brak weterynarzy w bazie."

    lines: list[str] = ["Lista weterynarzy z PetClinic:"]
    for vet in vet_list:
        specialties = [s.get("name", "brak") for s in vet.get("specialties", [])]
        spec_str = ", ".join(specialties) if specialties else "medycyna ogólna"
        hint = params.specialty_hint or ""
        if hint and not any(hint.lower() in s.lower() for s in specialties):
            continue  # filtrujemy gdy podano hint
        lines.append(
            f"  • ID {vet.get('id')}: {vet.get('firstName')} {vet.get('lastName')}"
            f" — specjalizacje: {spec_str}"
        )
    if len(lines) == 1:
        # brak trafień po filtrze — wróć wszystkich
        lines = ["Lista weterynarzy z PetClinic (wszyscy):"]
        for vet in vet_list:
            specialties = [s.get("name", "brak") for s in vet.get("specialties", [])]
            spec_str = ", ".join(specialties) if specialties else "medycyna ogólna"
            lines.append(
                f"  • ID {vet.get('id')}: {vet.get('firstName')} {vet.get('lastName')}"
                f" — specjalizacje: {spec_str}"
            )
    return "\n".join(lines)


# Symulowane dane obciążenia (w realu: zapytanie do bazy wizyt)
_VISIT_LOAD = {
    1: 2,   # James Carter
    2: 5,   # Helen Leary
    3: 1,   # Linda Douglas
    4: 4,   # Rafael Ortega
    5: 3,   # Henry Stevens
    6: 6,   # Sharon Jenkins
}


@define_tool(
    name="get_visit_load",
    description=(
        "Zwraca bieżące obciążenie wizytami dla konkretnego weterynarza "
        "(liczba zaplanowanych wizyt na dziś). Pomaga wybrać mniej obciążonego "
        "specjalistę gdy kilku pasuje do objawów."
    ),
    params_type=VisitLoadParams,
    skip_permission=True,
)
async def get_visit_load(params: VisitLoadParams, _inv) -> str:
    _tools_called.append("get_visit_load")
    load = _VISIT_LOAD.get(params.vet_id)
    if load is None:
        return f"Brak danych obciążenia dla weterynarza ID {params.vet_id}."
    level = "mała" if load <= 2 else ("średnia" if load <= 4 else "duża")
    return (
        f"Weterynarz ID {params.vet_id}: {load} wizyt zaplanowanych dziś "
        f"(obciążenie: {level})."
    )


@define_tool(
    name="search_pet_owners",
    description=(
        "Wyszukuje właścicieli zwierząt w PetClinic po nazwisku. "
        "Przydatne gdy użytkownik podaje swoje nazwisko i chce zobaczyć historię "
        "wizyt lub dane swoich pupili."
    ),
    params_type=SearchOwnersParams,
    skip_permission=True,
)
async def search_pet_owners(params: SearchOwnersParams, _inv) -> str:
    _tools_called.append("search_pet_owners")
    safe_name = params.last_name[:50]  # ograniczenie długości dla bezpieczeństwa
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                f"{PETCLINIC_BASE}/owners",
                params={"lastName": safe_name},
            )
            resp.raise_for_status()
            owners: list[dict] = resp.json()
    except httpx.HTTPError as exc:
        log.warning("Błąd podczas wyszukiwania właścicieli: %s", exc)
        return "Nie udało się wyszukać właścicieli w PetClinic API."

    if not owners:
        return f"Brak właścicieli o nazwisku '{safe_name}'."

    lines = [f"Właściciele '{safe_name}':"]
    for o in owners[:5]:  # max 5 wyników
        pets = [p.get("name", "?") for p in o.get("pets", [])]
        lines.append(
            f"  • {o.get('firstName')} {o.get('lastName')} "
            f"— zwierzęta: {', '.join(pets) or 'brak'}"
        )
    return "\n".join(lines)


# ─── Sesja Copilot SDK ────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Jesteś inteligentnym asystentem kliniki weterynaryjnej PetClinic.
Odpowiadasz w języku polskim.

Twoje możliwości:
1. Korzystaj z narzędzia get_available_vets aby pobrać AKTUALNĄ listę weterynarzy
   z działającego systemu PetClinic i dopasować specjalistę do objawów zwierzęcia.
2. Korzystaj z get_visit_load aby sprawdzić obciążenie i zaproponować mniej
   zajętego weterynarza gdy kilku pasuje.
3. Korzystaj z search_pet_owners gdy właściciel podaje swoje nazwisko.

Styl odpowiedzi:
- Bądź przyjazny i empatyczny — właściciele martwią się o swoje zwierzęta.
- Wymieniaj konkretne imię i specjalizację weterynarza.
- Jeśli znasz obciążenie — wspomnij który jest mniej zajęty dziś.
- Zakończ krótkim zdaniem zachęcającym do umówienia wizyty.

WAŻNE: Nie wymyślaj danych. Używaj wyłącznie informacji zwróconych przez narzędzia."""


async def run_copilot_session(message: str) -> tuple[str, list[str]]:
    """Uruchamia sesję Copilot SDK dla jednej wiadomości użytkownika."""
    global _tools_called
    _tools_called = []

    ensure_copilot_cli_on_path()

    full_prompt = f"{SYSTEM_PROMPT}\n\n---\nPytanie właściciela: {message}"

    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model=COPILOT_MODEL,
            tools=[get_available_vets, get_visit_load, search_pet_owners],
        ) as session:
            done = asyncio.Event()
            answer_parts: list[str] = []

            def on_event(event) -> None:
                match event.data:
                    case AssistantMessageData() as data:
                        if data.content:
                            answer_parts.append(data.content)
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(full_prompt)
            await asyncio.wait_for(done.wait(), timeout=120)

    reply = "\n".join(answer_parts).strip() or "Przepraszam, nie udało się wygenerować odpowiedzi."
    called = list(_tools_called)
    return reply, called


# ─── FastAPI app ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="PetClinic AI Triage Asystent",
    description="Serwis łączący Spring PetClinic z GitHub Copilot SDK.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Endpoint zdrowia — Spring proxy może go odpytywać."""
    return {"status": "ok", "service": "petclinic-ai-assistant"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Główny endpoint czatu — odbiera pytanie, zwraca odpowiedź AI."""
    log.info("Pytanie: %.100s", request.message)
    try:
        reply, tools = await run_copilot_session(request.message)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Copilot SDK timeout.")
    except Exception as exc:
        log.exception("Błąd sesji Copilot SDK: %s", exc)
        raise HTTPException(status_code=500, detail="Błąd serwisu AI.")
    log.info("Narzędzia: %s", tools)
    return ChatResponse(reply=reply, tools_called=tools)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("ai_server:app", host="127.0.0.1", port=8081, reload=False)
