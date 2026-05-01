"""
Wspólne utility dla rozwiązań modułu 10.

Ten plik pozwala uruchamiać przykłady niezależnie od tego, czy bundled CLI
(`@github/copilot`) jest na PATH (np. po świeżej instalacji `pip install
github-copilot-sdk`).

VS Code instaluje swoją kopię CLI w globalStorage rozszerzenia
`github.copilot-chat`. SDK domyślnie szuka `copilot` na PATH — jeśli go nie
znajdzie, wyrzuci `FileNotFoundError`. Tutaj wykrywamy obie ścieżki:
zainstalowaną przez VS Code i tę z `pip` (~/.local/...), i dokładamy do PATH.

Bezpieczeństwo: NIE czytamy ani nie ujawniamy żadnych tokenów. Polegamy na:
- zmiennej środowiskowej `GITHUB_TOKEN` (jeśli ustawiona), albo
- aktywnej sesji `copilot login` (poświadczenia w katalogu profilu CLI).
"""

from __future__ import annotations

import os
from pathlib import Path

_VSCODE_COPILOT_CLI_DIRS = [
    Path(os.environ.get("APPDATA", ""))
    / "Code"
    / "User"
    / "globalStorage"
    / "github.copilot-chat"
    / "copilotCli",
    Path.home()
    / ".vscode"
    / "extensions",  # fallback search root (best-effort)
]


def ensure_copilot_cli_on_path() -> str | None:
    """Dokłada do `PATH` katalog z bundled CLI `copilot` jeśli go znajdzie.

    Zwraca ścieżkę dodanego katalogu lub None gdy nic nie zmieniono.
    Idempotentne — kolejne wywołania nie duplikują wpisów.
    """
    for candidate in _VSCODE_COPILOT_CLI_DIRS:
        if not candidate.exists():
            continue
        # Bezpośrednie trafienie (Windows zainstalowany przez VS Code)
        if (candidate / "copilot.bat").exists() or (candidate / "copilot").exists():
            cli_dir = str(candidate)
            paths = os.environ.get("PATH", "").split(os.pathsep)
            if cli_dir not in paths:
                os.environ["PATH"] = cli_dir + os.pathsep + os.environ.get("PATH", "")
            return cli_dir
    return None


def repo_root() -> Path:
    """Zwraca katalog główny repozytorium (4 poziomy nad `solutions/_common.py`)."""
    return Path(__file__).resolve().parents[3]
