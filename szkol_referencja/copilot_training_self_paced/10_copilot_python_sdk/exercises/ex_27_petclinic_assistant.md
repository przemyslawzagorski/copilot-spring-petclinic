# Ex 27: PetClinic assistant — automatyzacja w repo

> Faza 8 · ~25 min · Moduł 10

**Po co:** SDK uruchamia agenta z dostępem do narzędzi (read/write/shell). Wykorzystaj to do realnego zadania w repo: każ Copilotowi przeczytać kod PetClinic i wygenerować artefakt — np. listę encji domenowych, raport o testach, podsumowanie modułu.

> **Uwaga o uprawnieniach:** Domyślnie SDK z `PermissionHandler.approve_all` ma takie same uprawnienia jak Ty: czyta i **edytuje pliki**, **uruchamia komendy shell**. W ćwiczeniu prosimy tylko o read i analizę. Jeśli chcesz pełne bezpieczeństwo — użyj custom handlera (przykład na końcu).

## Wymagania
- Wykonane [ex_26](ex_26_hello_chat.md)
- Workspace: `copilot-spring-petclinic` na branchu `main`

## Co zrobić

### 1. Utwórz `petclinic_assistant.py`

Skrypt poprosi Copilota o przeanalizowanie repo i zapisanie raportu.

```python
"""PetClinic assistant — analizuje encje domenowe i zapisuje raport."""
from __future__ import annotations

import asyncio
from pathlib import Path

from copilot import CopilotClient, SubprocessConfig
from copilot.generated.session_events import (
    AssistantMessageData,
    SessionIdleData,
)
from copilot.session import PermissionHandler

# Workspace = katalog repo PetClinic (3 poziomy w górę od tego pliku)
REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).resolve().parent / "petclinic_domain_report.md"

PROMPT = f"""\
Jesteś asystentem analizującym kod Java Spring Boot.
Workspace: Spring PetClinic (Spring Boot 4.0.3, Java 17).

Zadanie:
1. Przejrzyj pakiet src/main/java/org/springframework/samples/petclinic/owner/.
2. Wypisz wszystkie klasy encji JPA (z @Entity).
3. Dla każdej encji podaj: nazwę, kluczowe pola, relacje (np. @OneToMany, @ManyToOne).
4. Zapisz wynik jako tabelę Markdown do pliku: {OUTPUT.as_posix()}

Nie modyfikuj kodu Java. Tylko czytaj i zapisz raport.
"""


async def main() -> None:
    config = SubprocessConfig(cwd=str(REPO_ROOT))
    async with CopilotClient(config) as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="gpt-5",
        ) as session:
            done = asyncio.Event()

            def on_event(event) -> None:
                match event.data:
                    case AssistantMessageData() as data:
                        # Drukujemy tylko ostatni komunikat asystenta
                        print(data.content[:500] + ("..." if len(data.content) > 500 else ""))
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(PROMPT)
            await done.wait()

    if OUTPUT.exists():
        print(f"\n[OK] Raport zapisany: {OUTPUT}")
    else:
        print(f"\n[WARN] Brak pliku {OUTPUT} — model mógł nie wykonać zapisu.")


if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Uruchom

```powershell
python petclinic_assistant.py
```

Skrypt może trwać 20-60 sekund (model czyta wiele plików). W trakcie zobaczysz strumień komunikatów asystenta.

**Spodziewany wynik:**
- Powstaje plik `petclinic_domain_report.md` z tabelą encji (`Owner`, `Pet`, `PetType`, `Visit`).
- Konsola: ostatnie zdanie asystenta typu „Raport zapisany do ...".

### 3. Zweryfikuj raport

```powershell
type petclinic_domain_report.md
```

Otwórz plik i sprawdź czy lista encji pokrywa się z faktycznym kodem. Jeśli model coś pominął — zobacz `src/main/java/org/springframework/samples/petclinic/owner/` ręcznie.

### 4. Wariant z ograniczonym shellem (opcjonalnie)

Jeśli chcesz zablokować polecenia shell, podmień handler:

```python
from copilot.generated.session_events import PermissionRequest
from copilot.session import PermissionRequestResult


def deny_shell(request: PermissionRequest, invocation: dict) -> PermissionRequestResult:
    if request.kind.value == "shell":
        return PermissionRequestResult(kind="denied-interactively-by-user")
    return PermissionRequestResult(kind="approved")


# ... potem:
on_permission_request=deny_shell,
```

## Co właśnie się stało

- Ustawiliśmy `cwd` na root repo (`SubprocessConfig(cwd=...)`) — Copilot ma widoczność na kod Java.
- Custom prompt opisuje **zadanie + ścieżki + format wyniku + ograniczenia** (nie modyfikuj kodu).
- Agent użył wewnętrznych narzędzi: `view`, `glob`, `read_file`, `edit_file` (utworzenie raportu).
- `approve_all` automatycznie zatwierdził wszystkie te wywołania.

## Częste problemy

| Symptom | Rozwiązanie |
|---------|-------------|
| Brak pliku raportu | Sprzecznie sformułowany prompt — dopisz „Po skończeniu uruchom narzędzie do zapisu pliku" |
| Skrypt nie kończy | Dodaj `case _ as data: print(type(data).__name__)` w match — zobaczysz na czym wisi |
| Model edytuje kod Java | **Wzmocnij prompt:** „TYLKO READ-ONLY. Nie wywołuj `edit_file` na plikach `.java`." |
| Kosztuje za dużo premium requests | Skróć zakres do jednej encji albo użyj `gpt-4o-mini` |

**Spodziewany wynik:** Plik `petclinic_domain_report.md` istnieje i zawiera 4 encje z relacjami.

**Następne ćwiczenie (bonus):** [ex_28](ex_28_streaming.md) — streaming odpowiedzi w czasie rzeczywistym.
