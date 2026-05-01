"""
Rozwiązanie ex_27 — Asystent PetClinic.

Co robi:
- Uruchamia sesję SDK z `cwd` ustawionym na katalog główny repozytorium —
  dzięki temu wbudowane narzędzia agenta (read_file, glob, ...) widzą
  źródła Java (`src/main/java/.../owner/`).
- Wysyła prompt: agent ma przeskanować pakiet `owner`, wykryć encje JPA
  (klasy z @Entity / mapowane do tabel) oraz endpointy REST/MVC kontrolera,
  a wynik zapisać do pliku Markdown w katalogu uruchomienia skryptu.

Bezpieczeństwo:
- Domyślnie używamy `PermissionHandler.approve_all` (proste i wystarczające
  w warsztacie). W prawdziwej automatyzacji rozważ custom handler, który
  blokuje `shell` / `write` poza zdefiniowanym katalogiem roboczym.

Uruchomienie:  `python petclinic_assistant.py`
Wynik:        `petclinic_domain_report.md` w katalogu skryptu.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from copilot import CopilotClient, SubprocessConfig
from copilot.generated.session_events import AssistantMessageData, SessionIdleData
from copilot.session import PermissionHandler

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import ensure_copilot_cli_on_path, repo_root  # noqa: E402


REPORT_NAME = "petclinic_domain_report.md"

PROMPT_TEMPLATE = """
Jestes asystentem analizy kodu Java/Spring. Pracujesz w katalogu repozytorium
Spring PetClinic. Wykonaj nastepujace kroki:

1. Przeskanuj pliki w `src/main/java/org/springframework/samples/petclinic/owner/`.
2. Wymien klasy bedace encjami JPA (z adnotacja `@Entity`) z krotkim opisem (1 zdanie).
3. Wymien wszystkie endpointy HTTP w klasach `@Controller` / `@RestController` w tym
   pakiecie — w formacie tabeli: METODA | sciezka | nazwa metody Java.
4. Zapisz cala odpowiedz po polsku do pliku Markdown o sciezce: `{report_path}`.
   Plik MUSI byc utworzony narzedziem `write` / `edit_file`.

Nie modyfikuj zadnych innych plikow. Nie uruchamiaj polecen powloki.
""".strip()


async def main() -> int:
    ensure_copilot_cli_on_path()

    output_dir = Path.cwd().resolve()
    report_path = output_dir / REPORT_NAME
    if report_path.exists():
        report_path.unlink()  # zaczynamy od czystej kartki

    config = SubprocessConfig(cwd=str(repo_root()))

    async with CopilotClient(config) as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="auto",
        ) as session:
            done = asyncio.Event()

            def on_event(event):
                match event.data:
                    case AssistantMessageData() as data:
                        # logujemy tylko ostatnie 240 znakow per wiadomosc — pelny
                        # wynik i tak trafi do pliku raportu
                        text = (data.content or "").strip()
                        if text:
                            print(f"[asst] {text[-240:]}")
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(PROMPT_TEMPLATE.format(report_path=str(report_path)))
            # generowanie pliku z analizą trwa — dajmy 5 minut zapasu
            await asyncio.wait_for(done.wait(), timeout=300)

    if report_path.exists():
        size = report_path.stat().st_size
        print(f"[ok] Raport zapisany: {report_path} ({size} B)")
        return 0
    print(f"[fail] Brak pliku raportu w: {report_path}")
    return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
