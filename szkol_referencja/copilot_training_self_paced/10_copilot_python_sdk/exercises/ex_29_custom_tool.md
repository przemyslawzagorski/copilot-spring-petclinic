# Ex 29: Bonus — własne narzędzie (custom tool)

> Faza 8 · ~25 min · Moduł 10 · 🅱️ Bonus

**Po co:** SDK pozwala wystawić agentowi **własne funkcje** jako narzędzia. Model decyduje kiedy je wywołać, my dostajemy strukturalne argumenty (z walidacją Pydantic) i zwracamy wynik. To podstawa integracji z Twoją domeną biznesową (Jira, baza, własne API).

## Wymagania
- Wykonane [ex_26](ex_26_hello_chat.md)
- `pip install pydantic` (zwykle już zainstalowane jako tranzytywna zależność SDK)

## Co zrobić

### 1. Utwórz `custom_tool.py`

Tworzymy fikcyjne narzędzie „pobierz status weterynarza" — w realu mogłoby uderzać w bazę PetClinic.

```python
"""Custom tool dla Copilot SDK — fikcyjny lookup weterynarza."""
import asyncio

from pydantic import BaseModel, Field

from copilot import CopilotClient, define_tool
from copilot.generated.session_events import AssistantMessageData, SessionIdleData
from copilot.session import PermissionHandler

# --- Definicja narzędzia ---

# Pydantic models MUSZĄ być na poziomie modułu (nie w funkcji)
class GetVetParams(BaseModel):
    """Argumenty dla narzędzia get_vet_status."""

    vet_id: int = Field(description="Identyfikator weterynarza w bazie PetClinic")


# Fikcyjna „baza" weterynarzy
_VET_DB = {
    1: {"name": "James Carter", "specialty": "radiology", "available": True},
    2: {"name": "Helen Leary", "specialty": "surgery", "available": False},
    3: {"name": "Linda Douglas", "specialty": "dentistry", "available": True},
}


@define_tool(description="Zwróć status i specjalizację weterynarza po ID")
async def get_vet_status(params: GetVetParams) -> str:
    vet = _VET_DB.get(params.vet_id)
    if vet is None:
        return f"Brak weterynarza o ID {params.vet_id}"
    status = "dostępny" if vet["available"] else "niedostępny"
    return f"{vet['name']} ({vet['specialty']}) — {status}"


# --- Sesja ---

async def main() -> None:
    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="gpt-5",
            tools=[get_vet_status],   # <-- rejestracja narzędzia
        ) as session:
            done = asyncio.Event()

            def on_event(event) -> None:
                match event.data:
                    case AssistantMessageData() as data:
                        print("\n=== Odpowiedź ===")
                        print(data.content)
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(
                "Sprawdź proszę status weterynarzy o ID 1, 2 i 3 "
                "i napisz po polsku, którzy są teraz dostępni."
            )
            await done.wait()


if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Uruchom

```powershell
python custom_tool.py
```

**Spodziewany wynik:** Model wywoła `get_vet_status` 3 razy (raz na każdy ID), a potem podsumuje po polsku, że dostępni są James Carter i Linda Douglas.

### 3. Eksperyment — błędne ID

Zmień prompt na: „Sprawdź ID 99". Model powinien dostać odpowiedź „Brak weterynarza o ID 99" i zaraportować to użytkownikowi.

### 4. (Opcjonalnie) `skip_permission` — pomiń pytanie o zgodę

Dla narzędzi w 100% read-only:

```python
@define_tool(
    description="Zwróć status weterynarza",
    skip_permission=True,   # nie pyta usera/handlera
)
async def get_vet_status(params: GetVetParams) -> str:
    ...
```

## Co właśnie się stało

| Element | Rola |
|---------|------|
| `class GetVetParams(BaseModel)` | Pydantic — auto-generuje JSON schema dla LLM |
| `@define_tool(description=...)` | Rejestruje funkcję jako narzędzie z metadanymi |
| `async def get_vet_status(params)` | Handler — może być sync lub async |
| `tools=[get_vet_status]` przy `create_session` | Lista narzędzi widocznych dla agenta w tej sesji |
| `return str` | Tekst widoczny dla LLM jako wynik wywołania |

Pod spodem SDK:
1. Wysyła schema narzędzia do CLI/modelu w protokole.
2. Model decyduje czy wywołać — emituje `tool.call`.
3. SDK woła Twój handler z deserializowanymi argumentami.
4. Wynik trafia z powrotem do modelu.

## Częste problemy

| Symptom | Rozwiązanie |
|---------|-------------|
| `ValidationError` na argumentach | Sprawdź typy w `GetVetParams` — model wysłał coś innego, dopisz `Field(description=...)` żeby było jasne |
| Model nie woła narzędzia | `description` musi mówić co robi narzędzie i kiedy je wywołać. Bądź konkretny |
| Pydantic błąd `from __future__ import annotations` | Modele Pydantic muszą być na poziomie modułu, nie wewnątrz funkcji |
| `Tool 'X' overrides built-in tool` | Twoje narzędzie ma nazwę istniejącego CLI tool — zmień nazwę albo dodaj `overrides_built_in_tool=True` |

## Co dalej

- **Wersja low-level (bez Pydantic):** użyj `Tool(name=..., parameters={schema}, handler=...)` z `copilot.tools`.
- **MCP zamiast custom tool:** jeśli narzędzie ma być dostępne też w VS Code i Copilot CLI, lepiej zrobić MCP server (moduł 09).
- **Hooks** (`on_pre_tool_use`, `on_post_tool_use`) — modyfikacja argumentów/wyników w trakcie. Patrz: [README.md](../README.md) → sekcja Architektura.

**Spodziewany wynik:** Agent wywołał Twój kod 3 razy i zwrócił poprawne podsumowanie.

**Koniec modułu 10 🎉.** Wracaj do [START_HERE.md](../../START_HERE.md) po kolejne moduły, albo zbuduj własną automatyzację bazując na ex_27.
