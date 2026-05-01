"""
Rozwiązanie ex_29 — Custom tool (function calling).

Co pokazuje:
- Definiujemy wlasne narzedzie `get_vet_status` przez dekorator
  `@define_tool` + model Pydantic. SDK automatycznie generuje JSON schema.
- Rejestrujemy je przy `create_session(tools=[...])` — model moze je wywolac
  podczas rozmowy. Nasz handler dostaje sparsowany model parametrow i zwraca
  string, ktory trafia do modelu jako wynik narzedzia.
- `skip_permission=True` — uzywamy go celowo, bo to read-only lookup w
  in-memory dict (nie wymaga potwierdzania); upraszcza UX automatyzacji.

Uruchomienie: `python custom_tool.py`
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from pydantic import BaseModel, Field

from copilot import CopilotClient, define_tool
from copilot.generated.session_events import AssistantMessageData, SessionIdleData
from copilot.session import PermissionHandler

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import ensure_copilot_cli_on_path  # noqa: E402


# Symulowana baza weterynarzy. W realu szlibysmy tu do REST/DB.
_VET_DB: dict[int, dict] = {
    1: {"name": "James Carter", "specialty": "internal medicine", "available": True},
    2: {"name": "Helen Leary", "specialty": "radiology", "available": False},
    3: {"name": "Linda Douglas", "specialty": "surgery", "available": True},
}


class GetVetParams(BaseModel):
    """Parametry narzedzia get_vet_status."""

    vet_id: int = Field(description="Numeryczny identyfikator weterynarza (1..N).")


@define_tool(
    name="get_vet_status",
    description=(
        "Zwraca dostepnosc i specjalizacje weterynarza ze Spring PetClinic "
        "na podstawie jego identyfikatora liczbowego."
    ),
    params_type=GetVetParams,
    skip_permission=True,
)
async def get_vet_status(params: GetVetParams, _invocation) -> str:
    vet = _VET_DB.get(params.vet_id)
    if vet is None:
        return f"Brak weterynarza o id={params.vet_id}."
    avail = "dostepny" if vet["available"] else "niedostepny"
    return f"Vet #{params.vet_id}: {vet['name']} ({vet['specialty']}) — {avail}."


PROMPT = (
    "Sprawdz w narzedziu get_vet_status dostepnosc weterynarzy o id 1, 2 i 3. "
    "Odpowiedz po polsku jednym akapitem: wymien imiona, specjalizacje i "
    "kto jest aktualnie dostepny."
)


async def main() -> int:
    ensure_copilot_cli_on_path()

    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="auto",
            tools=[get_vet_status],
        ) as session:
            done = asyncio.Event()
            answer: list[str] = []

            def on_event(event):
                match event.data:
                    case AssistantMessageData() as data:
                        if data.content:
                            answer.append(data.content)
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(PROMPT)
            await asyncio.wait_for(done.wait(), timeout=180)

            print("--- ODPOWIEDZ ---")
            print("\n".join(answer).strip())
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
