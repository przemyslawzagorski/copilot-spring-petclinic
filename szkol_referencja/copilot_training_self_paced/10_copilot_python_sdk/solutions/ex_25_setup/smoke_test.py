"""
Rozwiązanie ex_25 — Smoke test SDK.

Co robi:
1. Importuje `copilot` (sprawdza poprawność instalacji `github-copilot-sdk`).
2. Otwiera `CopilotClient`, który używa runtime dostarczanego przez SDK, i wywołuje:
   - `get_auth_status()` — czy mamy aktywną sesję / token,
   - `list_models()` — lista modeli dostępnych w Twojej subskrypcji.

Wymagania uruchomieniowe:
- Python 3.11+ (testowane na 3.12).
- `pip install github-copilot-sdk`.
- Autoryzacja: zalogowane `copilot` (CLI) albo `COPILOT_GITHUB_TOKEN` w środowisku.

Wynik: na stdout pojawia się status auth oraz pierwsze ~10 modeli (ID + nazwa).
Exit code 0 = sukces, 2 = brak autoryzacji (świadomy skip), 1 = inny błąd.
"""

from __future__ import annotations

import asyncio
import sys

from copilot import CopilotClient

async def main() -> int:
    async with CopilotClient() as client:
        auth = await client.get_auth_status()
        print(
            f"[auth] is_authenticated={auth.isAuthenticated} "
            f"type={auth.authType} login={auth.login}"
        )
        if not auth.isAuthenticated:
            print(
                "[skip] Brak autoryzacji. Uruchom `copilot login` "
                "lub ustaw COPILOT_GITHUB_TOKEN."
            )
            return 2

        models = await client.list_models()
        print(f"[ok] Dostepnych modeli: {len(models)}")
        for m in models[:10]:
            name = getattr(m, "name", None) or getattr(m, "id", "?")
            print(f"  - {m.id}  ({name})")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
