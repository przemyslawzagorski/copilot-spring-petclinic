# Ex 25: Setup SDK i autoryzacja

> Faza 8 · ~15 min · Moduł 10

**Po co:** Zanim napiszesz pierwszy skrypt, musisz mieć działające środowisko: Python 3.11+, pakiet `github-copilot-sdk`, runtime i autoryzację.

## Wymagania
- Python 3.11+ (sprawdź: `python --version`)
- Konto GitHub z aktywnym Copilot (wystarczy free tier)
- Dostęp do internetu

## Co zrobić

### 1. Utwórz wirtualne środowisko dla modułu

```powershell
cd szkol_referencja/copilot_training_self_paced/10_copilot_python_sdk
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

> **Linux/macOS:** `source .venv/bin/activate`

### 2. Zainstaluj SDK

```powershell
pip install github-copilot-sdk
```

Sprawdź wersję:

```powershell
pip show github-copilot-sdk
```

Spodziewasz się wersji `1.x`. Przygotuj zgodny runtime CLI:

```powershell
python -m copilot download-runtime
```

SDK pobierze runtime automatycznie przy pierwszym użyciu, ale jawne polecenie daje
czytelniejszą diagnostykę przed szkoleniem.

### 3. Skonfiguruj autoryzację

**Opcja A (najprostsza — zalogowany user CLI):**

Jeśli używasz standalone Copilot CLI i jesteś zalogowany — SDK użyje istniejących poświadczeń.

**Opcja B (zmienna środowiskowa):**

Wygeneruj **fine-grained personal access token** z uprawnieniami Copilot:
<https://github.com/settings/tokens>

Ustaw zmienną środowiskową na czas sesji:

```powershell
$env:COPILOT_GITHUB_TOKEN = "..."   # tylko bieżąca sesja PowerShell
```

> **Nie commituj tokena.** Trzymaj w zmiennych środowiskowych albo w `.env` dodanym do `.gitignore`.

### 4. Smoke test — sprawdź import

Utwórz plik `smoke_test.py` w katalogu modułu:

```python
"""Smoke test SDK — sprawdza import i listę modeli."""
import asyncio
from copilot import CopilotClient


async def main() -> None:
    async with CopilotClient() as client:
        models = await client.list_models()
        print(f"Dostępne modele ({len(models)}):")
        for model in models[:5]:
            print(f"  - {getattr(model, 'id', model)}")


if __name__ == "__main__":
    asyncio.run(main())
```

Uruchom:

```powershell
python smoke_test.py
```

**Spodziewany wynik:** lista 5+ modeli (np. `gpt-5`, `claude-sonnet-4.5`, ...). Jeśli pojawi się prompt o autoryzację — przejdź flow OAuth w przeglądarce.

## Częste problemy

| Symptom | Przyczyna | Rozwiązanie |
|---------|-----------|-------------|
| `ModuleNotFoundError: No module named 'copilot'` | Niewłaściwe `.venv` | `Activate.ps1` jeszcze raz; potwierdź `(venv)` w prompt |
| `Python 3.10` ostrzeżenie / błąd | SDK wymaga 3.11+ | Zainstaluj nowszy Python lub `pyenv install 3.11.9` |
| `401 Unauthorized` | Brak tokena / brak Copilot | Zaloguj CLI lub ustaw `$env:COPILOT_GITHUB_TOKEN` |
| CLI nie startuje na Windows | Antivirus blokuje binarkę | Wyklucz katalog `.venv\Lib\site-packages\copilot\bin` |

**Spodziewany wynik:** `pip show` pokazuje pakiet, `smoke_test.py` drukuje modele bez wyjątku.

**Więcej:** [README modułu](../README.md) · [10_copilot_python_sdk/EXERCISES.md](../EXERCISES.md)
