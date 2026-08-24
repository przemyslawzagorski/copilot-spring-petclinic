# MCP Server

## 🎯 Cele modułu

- Zrozumieć architekturę Model Context Protocol (MCP).
- Podłączyć gotowy MCP server do VS Code.
- Zbudować własny MCP server w Python/FastAPI od zera.
- Przetestować MCP przez Copilot Chat.

---

## 📚 Teoria

### Czym jest MCP?

**Model Context Protocol** to standard łączenia agentów AI z zewnętrznymi źródłami danych i narzędziami. MCP server udostępnia:
- **Tools** — funkcje wywoływane przez agenta (np. `get_exchange_rate`, `create_issue`)
- **Prompts** — gotowe szablony promptów
- **Resources** — dane kontekstowe (pliki, bazy danych)

### Architektura

```
VS Code (Copilot)  ──MCP──>  MCP Server  ──>  API / DB / pliki
     klient                    serwer           źródło danych
```

Copilot jest **klientem MCP**. Serwer MCP to osobny proces (Python, Node.js, itp.) komunikujący się przez stdio lub HTTP.

### Konfiguracja w VS Code

Plik `.vscode/mcp.json` w workspace:

```json
{
  "servers": {
    "moj-server": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "cwd": "${workspaceFolder}/mcp_ex_api"
    }
  }
}
```

Albo w `settings.json` → `"mcp.servers"`.

### Gotowe MCP servery w tym repo

W workspace są gotowe implementacje MCP do nauki i eksperymentów:

| Folder | Opis |
|--------|------|
| `mcp_ex_api/` | **Benchmark** — MCP server FastAPI z publicznym API |
| `mcp_jira_wiki/` | MCP łączący się z Jira/Wiki |
| `mcp_for_databases/` | MCP do baz danych |
| `mcp_agent/` | Agent wykorzystujący MCP |

**Zacznij od `mcp_ex_api/`** — to wzorcowa implementacja.

### Budowa MCP server od zera (flow)

1. **Bootstrap** — `pip install fastmcp` + struktura projektu
2. **Definicja tools** — dekoratory `@mcp.tool()` z opisami
3. **Connector** — wywołania do zewnętrznego API/bazy
4. **Test** — uruchom server, podłącz do VS Code, przetestuj w Chat
5. **Hardening** — timeout, obsługa błędów, walidacja

---

## 📝 Ćwiczenia

| # | Ćwiczenie | Czas |
|---|-----------|------|
| ex_22 | Podłącz gotowy MCP server do VS Code | ~10 min |
| ex_23 | Zbuduj MCP server od zera (FastAPI) | ~30 min |
| ex_24 | Test MCP przez Copilot Chat | ~10 min |
| 🅱️ ex_24b | Bonus: dodaj nowe tool do istniejącego MCP | ~15 min |

Pliki ćwiczeń: `exercises/`

---

## 🚀 Poziom zaawansowany: MCP w realnej pracy programisty

| Materiał | Co pokazuje |
|---|---|
| [`../mcp_ex_api/`](../mcp_ex_api/INSTRUKCJA_UCZESTNIK.md) | Podstawy: narzędzia + zasoby + przepływy na publicznych API |
| [`../mcp_devkit/`](../mcp_devkit/README.md) | Poziom produkcyjny: RAG (Tavily/Jina), pamięć wektorowa (Qdrant), RAG po własnym repo, delegowanie podzadań do szybkiego modelu (Groq) |

`mcp_devkit` odpowiada na pytanie „po co mi własny serwer MCP, skoro agent i tak umie
czytać pliki?” — pokazuje **ekonomię kontekstu**: ciężką robotę wykonuje tani model
i baza wektorowa, a do głównego okna wraca sam wynik.
