# Ex 22: Bootstrap MCP Server w FastAPI

> Faza 7 · ~10 min · Źródło: moduł 11

**Po co:** MCP Server rozszerza Copilot o zewnętrzne dane i narzędzia. Budujesz go od pustego folderu.

## Wymagania
- Python 3.10+ zainstalowany
- `pip` dostępny w terminalu

## Co zrobić

1. W Copilot Chat (tryb agent) wpisz:

```
Utwórz od zera projekt Python FastAPI MCP server w folderze mcp_server/ w tym repo.
Struktura: app/main.py, app/models.py, app/mcp_handler.py, requirements.txt.
Zależności: fastapi, uvicorn, httpx, pydantic.
Dodaj endpoint healthcheck GET / zwracający {"status": "ok"}.
Dodaj README_RUN.md z instrukcją uruchomienia na Windows i Linux.
```

2. Po wygenerowaniu plików:

```
cd mcp_server
pip install -r requirements.txt
uvicorn app.main:app --reload
```

3. Otwórz `http://localhost:8000` w przeglądarce.

**Spodziewany wynik:** `{"status": "ok"}` — serwer działa.

**Nie działa?** Sprawdź czy Python jest w PATH: `python --version`. Jeśli pip nie działa: `python -m pip install -r requirements.txt`.

**Więcej:** `11_module_11_mcp_fastapi_from_scratch/EXERCISES.md` — ćwiczenie 1
