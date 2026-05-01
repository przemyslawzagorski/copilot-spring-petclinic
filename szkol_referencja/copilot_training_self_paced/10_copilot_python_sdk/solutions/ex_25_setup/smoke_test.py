"""
Rozwiązanie ex_25 — Smoke test SDK.

Co robi:
1. Importuje `copilot` (sprawdza poprawność instalacji `github-copilot-sdk`).
2. Lokalizuje bundled CLI `@github/copilot` (zainstalowane przez VS Code) i
   dokłada je do PATH — bez tego SDK nie ma czego uruchomić jako podproces.
3. Otwiera `CopilotClient` i wywołuje:
   - `get_auth_status()` — czy mamy aktywną sesję / token,
   - `list_models()` — lista modeli dostępnych w Twojej subskrypcji.

Wymagania uruchomieniowe:
- Python 3.11+ (testowane na 3.12).
- `pip install github-copilot-sdk`.
- Autoryzacja: zalogowane `copilot` (CLI) albo `GITHUB_TOKEN` w środowisku.

Wynik: na stdout pojawia się status auth oraz pierwsze ~10 modeli (ID + nazwa).
Exit code 0 = sukces, 2 = brak autoryzacji (świadomy skip), 1 = inny błąd.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from copilot import CopilotClient

# pozwala importowac _common.py z katalogu nadrzednego (solutions/)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import ensure_copilot_cli_on_path  # noqa: E402


async def main() -> int:
    cli_dir = ensure_copilot_cli_on_path()
    print(f"[info] Bundled copilot CLI: {cli_dir or 'NIE ZNALEZIONO (uzyje PATH)'}")

    async with CopilotClient() as client:
        auth = await client.get_auth_status()
        print(
            f"[auth] is_authenticated={auth.isAuthenticated} "
            f"type={auth.authType} login={auth.login}"
        )
        if not auth.isAuthenticated:
            print("[skip] Brak autoryzacji. Uruchom `copilot login` lub ustaw GITHUB_TOKEN.")
            return 2

        models = await client.list_models()
        print(f"[ok] Dostepnych modeli: {len(models)}")
        for m in models[:10]:
            name = getattr(m, "name", None) or getattr(m, "id", "?")
            print(f"  - {m.id}  ({name})")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
