# Moduł 09 — MCP Server: adaptacja dla Claude Code

> FastMCP serwery z tego szkolenia działają **bez zmian** w Claude Code — zmienia się tylko konfiguracja połączenia.

---

## Porównanie konfiguracji MCP

| GitHub Copilot | Claude Code |
|---|---|
| `.vscode/mcp.json` | `.mcp.json` (root projektu) — project scope |
| `~/.copilot/mcp.json` (user) | `~/.claude.json` (user scope) |
| Restartuj VSCode po zmianie | `claude mcp list` / automatyczne przeładowanie |

**Format `.mcp.json` jest identyczny** — Claude Code i Copilot używają tego samego schematu JSON!

---

## Format `.mcp.json`

```json
{
  "mcpServers": {
    "nazwa-serwera": {
      "type": "stdio",
      "command": "python",
      "args": ["ścieżka/do/serwera.py"],
      "env": {
        "KLUCZ": "wartość"
      }
    }
  }
}
```

Ten projekt już ma `.mcp.json` — otwórz go i przejrzyj.

---

## Ex 22 (CC): Podłącz istniejący serwer MCP

**Odpowiednik ex_22_mcp_serwer.md**

Ten projekt ma gotowy serwer MCP Jira+Wiki w:
`szkol_referencja/copilot_training_self_paced/mcp_jira_wiki/`

**Podłączenie przez CLI:**
```bash
claude mcp add jira-wiki -- python szkol_referencja/copilot_training_self_paced/mcp_jira_wiki/jira_wiki_mcpserver.py
```

**Lub ręcznie** dodaj do `.mcp.json`:
```json
{
  "mcpServers": {
    "jira-wiki": {
      "type": "stdio",
      "command": "python",
      "args": ["szkol_referencja/copilot_training_self_paced/mcp_jira_wiki/jira_wiki_mcpserver.py"]
    }
  }
}
```

**Weryfikacja:**
```bash
claude mcp list
```

---

## Ex 22b (CC): Polecenia CLI do zarządzania MCP

**Odpowiednik ex_22b_mcp_cli.md**

Copilot zarządza MCP przez GUI w VSCode. Claude Code ma dedykowane CLI:

```bash
# Lista serwerów
claude mcp list

# Dodaj serwer stdio
claude mcp add moj-serwer -- python mcp_server.py

# Dodaj serwer HTTP
claude mcp add api-server --transport http --url http://localhost:8080

# Usuń serwer
claude mcp remove moj-serwer

# Status serwera
claude mcp get moj-serwer

# Dodaj z zmiennymi środowiskowymi
claude mcp add jira-server -e JIRA_URL=https://my.atlassian.net -- python server.py
```

---

## Ex 23 (CC): Twój własny serwer FastMCP

**Odpowiednik ex_23_twoj_serwer_mcp.md**

FastMCP jest w pełni kompatybilny z Claude Code — ten sam kod Python, inna konfiguracja.

**Serwer przykładowy** `scripts/mcp/petclinic-tools.py`:
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("petclinic-tools")

@mcp.tool()
def get_owner_count() -> str:
    """Zwraca liczbę właścicieli zwierząt w bazie danych."""
    # W realnym kodzie: zapytanie do bazy
    return "Właściciele: 10 (dane przykładowe)"

@mcp.tool()
def list_vets() -> str:
    """Lista weterynarzy zarejestrowanych w klinice."""
    vets = ["James Carter", "Helen Leary", "Linda Douglas"]
    return "\n".join(f"- {v}" for v in vets)

if __name__ == "__main__":
    mcp.run()
```

**Podłącz do Claude Code:**
```bash
claude mcp add petclinic -- python scripts/mcp/petclinic-tools.py
```

**Użyj w sesji:**
```
Ile właścicieli zwierząt jest w klinice?
```
Claude automatycznie wywołuje `get_owner_count` przez MCP.

---

## Ex 24 (CC): Zakres MCP — projekt vs użytkownik

**Odpowiednik ex_24_mcp_scope.md**

| Zakres | Lokalizacja | Dla kogo |
|---|---|---|
| Project | `.mcp.json` w root repo | Wszyscy w projekcie (commitujemy) |
| User | `~/.claude.json` → `mcpServers` | Tylko Twoja maszyna |
| Local | `.mcp.json` + gitignore | Lokalny eksperyment |

**Kiedy używać zakresu user:**
- Serwery z credentials (klucze API do Jira, GitHub)
- Serwery specyficzne dla Twojej maszyny (lokalna baza, localhost)

**Kiedy używać zakresu project:**
- Serwery wspólne dla całego zespołu
- Dokumentacja, narzędzia testowe, CI data

**Dodaj do zakresu user:**
```bash
claude mcp add --scope user moj-prywatny-serwer -- python serwer.py
```

---

## Ex 24b (CC): MCP w frontmatterze subagenta

**Odpowiednik ex_24b_mcp_agent.md**

Możesz przypisać MCP serwer tylko do konkretnego subagenta:

```markdown
---
name: jira-assistant
description: "Asystent do pracy z Jira — tworzy tickety, sprawdza status, przypisuje zadania."
tools: Read
mcpServers:
  - name: jira-wiki
---

Jesteś asystentem do pracy z Jira w projekcie Spring PetClinic.
Masz dostęp do narzędzi MCP: create_issue, get_issue, list_issues.

Zawsze pytaj o projekt (PET), priorytet i assignee przed stworzeniem ticketu.
```

Serwer `jira-wiki` z `.mcp.json` jest dostępny tylko gdy ten subagent jest aktywny.

---

## Kompatybilność FastMCP z Claude Code

| Funkcja | Copilot | Claude Code |
|---|---|---|
| `@mcp.tool()` | ✅ | ✅ |
| `@mcp.resource()` | ✅ | ✅ |
| `@mcp.prompt()` | ✅ | ✅ |
| Transport `stdio` | ✅ | ✅ |
| Transport `http`/SSE | ✅ | ✅ |
| Zmienne środowiskowe | ✅ | ✅ |
| CLI zarządzanie | VS Code GUI | `claude mcp *` |

Kodu serwera **nie trzeba zmieniać** — tylko konfiguracja połączenia.
