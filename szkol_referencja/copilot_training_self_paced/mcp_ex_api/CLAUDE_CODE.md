# MCP PublicAPIs — adaptacja dla Claude Code

> Serwer `api_sever.py` używa **FastMCP** — jest **w pełni kompatybilny** z Claude Code bez żadnych zmian w kodzie.

---

## Szybki start

### Krok 1: Zainstaluj zależności

```bash
pip install mcp httpx
# lub z .venv:
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install mcp httpx
```

### Krok 2: Dodaj do `.mcp.json` (root projektu)

Zamiast `.vscode/mcp.json` (Copilot), Claude Code używa `.mcp.json` w root repo.

Ten projekt już ma `.mcp.json` — dodaj wpis `publiczne-api`:

```json
{
  "mcpServers": {
    "publiczne-api": {
      "type": "stdio",
      "command": "python",
      "args": ["szkol_referencja/copilot_training_self_paced/mcp_ex_api/api_sever.py"]
    }
  }
}
```

### Krok 3: Zweryfikuj

```bash
claude mcp list
```

Powinieneś zobaczyć `publiczne-api` na liście.

### Krok 4: Użyj w sesji

Uruchom `claude` i wpisz:
```
Jaki jest dzisiaj kurs USD w PLN?
```

Claude Code automatycznie wywoła narzędzie `get_exchange_rate` przez MCP.

---

## Dostępne narzędzia serwera

| Narzędzie | Opis | Przykład użycia |
|---|---|---|
| `get_exchange_rate` | Kurs waluty z NBP | "Kurs EUR dzisiaj?" |
| `get_pokemon_stats` | Statystyki Pokemon | "Statystyki pikachu?" |
| `get_random_joke` | Losowy żart | "Powiedz żart" |

---

## Różnica vs Copilot

| Copilot | Claude Code |
|---|---|
| `.vscode/mcp.json` z `"servers":` | `.mcp.json` z `"mcpServers":` |
| Zarządzanie przez VS Code GUI | `claude mcp add/list/remove` |
| Restart VS Code po zmianie | Automatyczne przeładowanie |

**Kod serwera (`api_sever.py`) — bez zmian!** FastMCP jest transport-agnostic.
