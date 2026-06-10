# MCP for Databases (Toolbox + PostgreSQL) — adaptacja dla Claude Code

> **TL;DR:** Google Toolbox (MCP serwer) działa z Claude Code. `agent.py` używa Google ADK/Gemini — wymaga przepisania na Anthropic SDK.

---

## Co działa bez zmian vs co wymaga zmiany

| Komponent | Status | Uwagi |
|---|---|---|
| `toolbox.yaml` | ✅ Działa | MCP Toolbox jest provider-agnostic |
| Toolbox server binary | ✅ Działa | Standardowy MCP przez HTTP/SSE |
| `setup_db.sql` | ✅ Działa | Czysty SQL, niezależny |
| `agent.py` | ❌ Wymaga przepisania | Używa Google ADK (`google-adk`) + Gemini |

---

## Opcja A: Podłącz Toolbox do Claude Code (bez agent.py)

Po uruchomieniu Toolbox (krok 4 z README.md), dodaj do `.mcp.json`:

```json
{
  "mcpServers": {
    "database-toolbox": {
      "type": "http",
      "url": "http://127.0.0.1:5000/mcp"
    }
  }
}
```

Lub przez CLI:
```bash
claude mcp add database-toolbox --transport http --url http://127.0.0.1:5000/mcp
```

Potem w sesji Claude Code:
```
Znajdź hotele w Warszawie
```

Claude Code automatycznie wywoła narzędzia z Toolbox przez MCP — bez żadnego `agent.py`!

---

## Opcja B: Przepisz agent.py na Anthropic SDK

Zamiast `google-adk` + Gemini, użyj Anthropic SDK:

```python
import anthropic
from anthropic import Anthropic

client = Anthropic()  # wymaga ANTHROPIC_API_KEY

# Pobierz narzędzia z Toolbox przez MCP (opcjonalne - Claude Code robi to automatycznie)
# W sesji Claude Code po prostu podłącz .mcp.json i pytaj!

# Alternatywnie — bezpośrednie wywołanie przez HTTP jeśli chcesz własny skrypt:
import httpx

def search_hotels(query: str) -> list:
    response = httpx.post(
        "http://127.0.0.1:5000/mcp",
        json={"method": "tools/call", "params": {"name": "search-hotels-by-location", "arguments": {"location": query}}}
    )
    return response.json()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Hotele wyniki: {search_hotels('Warsaw')}"}]
)
print(message.content[0].text)
```

---

## Uruchomienie Toolbox (identyczne jak dla Copilot)

Kroki 1–4 z `README.md` są bez zmian:
1. Stwórz PostgreSQL na Neon.tech/Supabase
2. Wykonaj `setup_db.sql`
3. Skonfiguruj `toolbox.yaml` z connection string
4. Uruchom `./toolbox --tools-file toolbox.yaml`

---

## Kluczowa różnica architektoniczna

```
Copilot/ADK flow:            Claude Code flow:
agent.py (Gemini/ADK)        .mcp.json + claude sesja
    ↓                            ↓
MCPToolset (SSE conn)        Claude Code (klient MCP)
    ↓                            ↓
Toolbox Server               Toolbox Server
    ↓                            ↓
PostgreSQL                   PostgreSQL
```

W Claude Code — Toolbox jest podłączony bezpośrednio jako MCP server. Nie potrzebujesz `agent.py`!
