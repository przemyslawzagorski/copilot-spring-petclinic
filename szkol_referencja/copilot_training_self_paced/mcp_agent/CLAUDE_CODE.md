# MCP Agent (zewnętrzny SSE) — adaptacja dla Claude Code

> Zewnętrzny serwer MCP przez SSE działa identycznie w Claude Code — ten sam format konfiguracji.

---

## Konfiguracja w Claude Code

Zamiast `.vscode/mcp.json` (Copilot) → `.mcp.json` w root projektu.

**Format identyczny:**

```json
{
  "mcpServers": {
    "pirat-agent": {
      "type": "sse",
      "url": "https://pirate-navigator-28948426345.us-central1.run.app/mcp"
    }
  }
}
```

Lub przez CLI:
```bash
claude mcp add pirat-agent --transport sse --url https://pirate-navigator-28948426345.us-central1.run.app/mcp
```

---

## Typy transportu MCP w Claude Code

| Transport | Format konfiguracji | Kiedy |
|---|---|---|
| `stdio` | `command` + `args` | Lokalne serwery Python/Node |
| `sse` | `url` (HTTP+SSE) | Zdalne serwery (deprecated w spec, ale wspierane) |
| `http` | `url` (Streamable HTTP) | Nowe zdalne serwery |

---

## Weryfikacja

```bash
# Lista serwerów
claude mcp list

# Status konkretnego serwera
claude mcp get pirat-agent
```

W sesji Claude Code: "Jakie narzędzia pirackie są dostępne?"

---

## Kluczowa informacja: transporty w Claude Code

Claude Code obsługuje **wszystkie typy transportu** opisane w tym module:
- `stdio` (lokalne serwery) ✅
- `sse` (zewnętrzne serwery HTTP+SSE) ✅
- `http` (Streamable HTTP — nowy standard) ✅

Materiał README.md z tego modułu jest w pełni aktualny — dotyczy zarówno Copilot jak i Claude Code.

**Jedyna różnica:** plik konfiguracyjny (`.vscode/mcp.json` vs `.mcp.json`).
