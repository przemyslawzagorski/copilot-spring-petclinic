# Ex 28: Bonus — streaming odpowiedzi

> Faza 8 · ~15 min · Moduł 10 · 🅱️ Bonus

**Po co:** Domyślnie dostajesz pełną odpowiedź dopiero gdy model skończy generować. Streaming pokazuje tekst „literka po literce" — UX jak w VS Code Chat.

## Wymagania
- Wykonane [ex_26](ex_26_hello_chat.md)

## Co zrobić

### 1. Utwórz `streaming_chat.py`

```python
"""Streaming Copilot SDK — odpowiedź przychodzi w kawałkach."""
import asyncio

from copilot import CopilotClient
from copilot.generated.session_events import (
    AssistantMessageData,
    AssistantMessageDeltaData,
    SessionIdleData,
)
from copilot.session import PermissionHandler


async def main() -> None:
    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="gpt-5",
            streaming=True,  # <-- włącza eventy delta
        ) as session:
            done = asyncio.Event()

            def on_event(event) -> None:
                match event.data:
                    case AssistantMessageDeltaData() as data:
                        # Drukuj każdy fragment od razu, bez nowej linii
                        print(data.delta_content or "", end="", flush=True)
                    case AssistantMessageData():
                        # Pełna wiadomość — sygnał końca konkretnej tury
                        print()  # \n po skończonej odpowiedzi
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(
                "Wytłumacz w 5 zdaniach po polsku jak działa async/await w Pythonie."
            )
            await done.wait()


if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Uruchom

```powershell
python streaming_chat.py
```

**Spodziewany wynik:** tekst pojawia się stopniowo (kilka znaków na sekundę), zamiast jednego dużego bloku po pauzie.

### 3. Eksperyment — porównaj z ex_26

Uruchom ex_26 i ex_28 obok siebie. Różnica w UX jest spora.

## Co właśnie się stało

| Element | Rola |
|---------|------|
| `streaming=True` | Włącza emisję `AssistantMessageDeltaData` po drodze |
| `data.delta_content` | Inkrementalny fragment tekstu (może być pusty string) |
| `print(..., end="", flush=True)` | Bez `\n` i z natychmiastowym fluszowaniem buffera stdout |
| `AssistantMessageData` (final) | Wciąż przychodzi na końcu — z pełną treścią. Dobry moment na log/persist |

## Reasoning delta (modele z reasoning)

Jeśli używasz modelu z reasoning (np. `gpt-5` w trybie wysokim), dostaniesz też `AssistantReasoningDeltaData`:

```python
from copilot.generated.session_events import AssistantReasoningDeltaData

# w match:
case AssistantReasoningDeltaData() as data:
    print(f"[reasoning] {data.delta_content}", end="", flush=True)
```

## Częste problemy

| Symptom | Rozwiązanie |
|---------|-------------|
| Brak strumieniowania, pełna odpowiedź na koniec | Brakuje `streaming=True` w `create_session` |
| Tekst pojawia się dużymi blokami | To naturalne — model emituje tokeny w paczkach. Mniejsze ≠ lepsze |
| `delta_content` to czasem `None` | Dodaj `or ""` jak w przykładzie |

**Spodziewany wynik:** odpowiedź pojawia się na żywo w terminalu.

**Następne ćwiczenie:** [ex_29](ex_29_custom_tool.md) — własne narzędzie dla agenta.
