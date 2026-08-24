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
| `get_rate_history` | Historia kursu z min/max/średnią i zmianą % | "Jak zmieniał się CHF przez 30 notowań?" |

## Zasoby (resources)

Zasób to kontekst adresowany przez URI — wciągasz go **jawnie**, model nie ładuje go sam.

| URI | Zawartość |
|---|---|
| `nbp://rates/table-a` | Cała tabela A NBP (wszystkie waluty w jednym odczycie) |
| `nbp://rates/{currency_code}` | Kurs pojedynczej waluty (resource template), np. `@nbp://rates/EUR` |
| `api://catalog` | Katalog użytych API wraz z limitami i pułapkami |

## Przepływy (prompts)

Widoczne w Claude Code jako slash-komendy:

| Prompt | Wywołanie |
|---|---|
| `analiza_kursu` | `/mcp__publiczne-api__analiza_kursu` |
| `porownaj_pokemony` | `/mcp__publiczne-api__porownaj_pokemony` |

> **Trzy filary MCP:** narzędzie *robi coś* (model wywołuje je sam), zasób *jest czymś*
> (użytkownik wciąga go świadomie), prompt *prowadzi przez przepływ* (użytkownik uruchamia
> go jak komendę). Serwer wysokiej jakości używa wszystkich trzech.

## Dalej: serwer produkcyjny

`mcp_ex_api` to poziom podstawowy. Wersja produkcyjna tych samych idei — RAG, pamięć
wektorowa, delegowanie do taniego modelu — jest w
[`../mcp_devkit/`](../mcp_devkit/README.md).

---

## Różnica vs Copilot

| Copilot | Claude Code |
|---|---|
| `.vscode/mcp.json` z `"servers":` | `.mcp.json` z `"mcpServers":` |
| Zarządzanie przez VS Code GUI | `claude mcp add/list/remove` |
| Restart VS Code po zmianie | Automatyczne przeładowanie |

**Kod serwera (`api_sever.py`) — bez zmian!** FastMCP jest transport-agnostic.
