"""
Konfiguracja pytesta dla testow modulu 10.

Testy oznaczone markerem `live` wymagaja autoryzacji do GitHub Copilot.
Jesli `CopilotClient.get_auth_status()` zwroci `isAuthenticated=False`, testy
sa AUTOMATYCZNIE pomijane (skip) — to celowe, zeby CI bez tokena nie sypal
falszywymi czerwonymi.

Co tu siedzi:
- `_check_auth()` — bezpieczny, jednorazowy probe statusu autoryzacji.
- fixture `pytestmark` na poziomie sesji wstrzykuje skip jesli brak auth.
- `repo_root_dir` — sciezka do roota repo PetClinic (uzywana przez ex_27).
- `tmp_workdir` — tymczasowy katalog roboczy + chdir, dla testow ktore
  generuja pliki (np. ex_27 raport).
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

import pytest

# pozwala importowac _common z solutions/
SOLUTIONS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOLUTIONS_DIR))
from _common import ensure_copilot_cli_on_path, repo_root  # noqa: E402

from copilot import CopilotClient  # noqa: E402


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "live: test wykonuje realne wywolanie GitHub Copilot SDK (wymaga auth, koszt tokenow)",
    )


def _check_auth() -> tuple[bool, str]:
    """Sprawdza autoryzacje — zwraca (is_auth, status_message)."""
    ensure_copilot_cli_on_path()

    async def _probe() -> tuple[bool, str]:
        async with CopilotClient() as client:
            auth = await client.get_auth_status()
            return bool(auth.isAuthenticated), auth.statusMessage or ""

    try:
        return asyncio.run(_probe())
    except Exception as exc:  # noqa: BLE001
        return False, f"probe error: {exc!r}"


_AUTH_OK, _AUTH_MSG = _check_auth()


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if _AUTH_OK:
        return
    skip_live = pytest.mark.skip(
        reason=(
            "Brak autoryzacji GitHub Copilot. Zaloguj sie: 1) `npm i -g @github/copilot` "
            "2) uruchom `copilot` i wpisz `/login`, ALBO 3) ustaw zmienna srodowiskowa "
            f"GITHUB_TOKEN. Status SDK: {_AUTH_MSG!r}"
        )
    )
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


@pytest.fixture(scope="session")
def repo_root_dir() -> Path:
    return repo_root()


@pytest.fixture
def tmp_workdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture(scope="session")
def event_loop():
    """Wspolny event loop dla wszystkich testow async w sesji."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
