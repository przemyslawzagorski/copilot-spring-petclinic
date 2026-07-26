"""Wspólne utility dla rozwiązań modułu 10."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Zwraca katalog główny repozytorium (5 poziomów nad plikiem)."""
    return Path(__file__).resolve().parents[4]
