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
| `mcp_local_postgres/` | MCP z lokalnym PostgreSQL |
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
