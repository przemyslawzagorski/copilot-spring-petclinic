# Ex 26: Pierwsza sesja — hello chat

> Faza 8 · ~15 min · Moduł 10

**Po co:** Najprostsza interakcja z SDK: utwórz klienta, otwórz sesję, wyślij wiadomość, odbierz odpowiedź modelu. Poznasz async context manager i event-driven API.

## Wymagania
- Wykonane [ex_25](ex_25_setup_sdk.md)
- Aktywne `.venv` z `github-copilot-sdk`

## Co zrobić

### 1. Utwórz `hello_chat.py`

W katalogu `10_copilot_python_sdk/` utwórz plik:

```python
"""Pierwsza sesja Copilot SDK — hello world."""
import asyncio

from copilot import CopilotClient
from copilot.generated.session_events import AssistantMessageData, SessionIdleData
from copilot.session import PermissionHandler


async def main() -> None:
    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="gpt-5",
        ) as session:
            done = asyncio.Event()
            answer: list[str] = []

            def on_event(event) -> None:
                match event.data:
                    case AssistantMessageData() as data:
                        answer.append(data.content)
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send("Powiedz krótko po polsku: po co jest Spring PetClinic?")
            await done.wait()

            print("=== Odpowiedź modelu ===")
            print("\n".join(answer))


if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Uruchom

```powershell
python hello_chat.py
```

**Spodziewany wynik:** kilka zdań po polsku o tym, że PetClinic to przykładowa aplikacja Spring Boot do zarządzania kliniką weterynaryjną.

### 3. Eksperyment — zmień model

Podmień `model="gpt-5"` na `model="claude-sonnet-4.5"` (lub inny z `list_models()` z ex_25). Porównaj odpowiedzi.

## Co właśnie się stało

| Element | Rola |
|---------|------|
| `async with CopilotClient()` | Startuje proces CLI w tle, sprząta po wyjściu z bloku |
| `await client.create_session(...)` | Tworzy nową konwersację (sesję JSON-RPC) |
| `on_permission_request=PermissionHandler.approve_all` | **WYMAGANE** — zatwierdza każde wywołanie narzędzia automatycznie (OK do nauki, w produkcji: custom handler) |
| `session.on(on_event)` | Subskrypcja wszystkich eventów sesji |
| `match event.data:` | Pattern matching — różne typy zdarzeń (`AssistantMessageData` = pełna odpowiedź, `SessionIdleData` = sesja czeka na input) |
| `await done.wait()` | Blokujemy aż model skończy generować |

## Częste problemy

| Symptom | Rozwiązanie |
|---------|-------------|
| Skrypt wisi i nie kończy | Brakuje `SessionIdleData` w match — dodaj `case _: pass` aby logować nieznane eventy |
| `PermissionError` / brak narzędzi | `on_permission_request` jest **wymagany** — nie pomijaj |
| Pusta odpowiedź | Sprawdź czy `model=` jest na liście z `client.list_models()` |

**Spodziewany wynik:** skrypt wypisuje odpowiedź modelu i kończy się czysto (exit code 0).

**Następne ćwiczenie:** [ex_27](ex_27_petclinic_assistant.md) — użyjesz SDK do automatyzacji w repo PetClinic.
