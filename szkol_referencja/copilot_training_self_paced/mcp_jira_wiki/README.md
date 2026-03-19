# MCP Server — Jira & Confluence Wiki

## 📚 Opis

MCP server integrujący Copilot z **Atlassian Jira** i **Confluence Wiki**. Serwer działa lokalnie (transport `stdio`) i udostępnia narzędzia do zarządzania ticketami Jira oraz stronami Wiki bezpośrednio z poziomu Copilot Chat.

### Architektura

```
VS Code (Copilot)  ──stdio──>  jira_wiki_mcpserver.py  ──REST API──>  Atlassian Cloud
     klient MCP                    serwer MCP                        Jira / Confluence
```

Serwer używa transportu **stdio** — VS Code uruchamia go jako podproces i komunikuje się przez `stdin`/`stdout`. Dane uwierzytelniające do Atlassian przekazywane są przez zmienne środowiskowe.

---

## 🔧 Dostępne narzędzia (tools)

### Jira

| Tool | Opis |
|------|------|
| `jira_get_ticket` | Pobierz informacje o tickecie po ID (np. `TRAIN-1`) |
| `jira_search` | Szukaj ticketów za pomocą JQL (Jira Query Language) |
| `jira_my_open_tickets` | Lista otwartych ticketów przypisanych do bieżącego użytkownika |
| `jira_create_ticket` | Utwórz nowy ticket (rate limit: 5/h) |
| `jira_add_comment` | Dodaj komentarz do ticketa (rate limit: 5/h) |

### Wiki (opcjonalnie, gdy `ENABLE_WIKI_INTEGRATION=true`)

| Tool | Opis |
|------|------|
| `wiki_get_page` | Pobierz stronę Confluence po ID |
| `wiki_search` | Szukaj stron za pomocą CQL (Confluence Query Language) |
| `wiki_get_page_by_url` | Pobierz stronę po pełnym URL |

---

## ⚙️ Konfiguracja

### 1. Wymagania

```bash
pip install fastmcp requests python-dotenv
```

### 2. Zmienne środowiskowe

Skopiuj szablon i uzupełnij wartości:

```powershell
copy .env.template .env
```

Wymagane zmienne:

| Zmienna | Opis |
|---------|------|
| `JIRA_BASE_URL` | URL REST API Jira, np. `https://INSTANCJA.atlassian.net/rest/api/2` |
| `JIRA_AUTH_TYPE` | `basic` (Atlassian Cloud) lub `bearer` (on-premise) |
| `JIRA_USER_EMAIL` | Email konta Atlassian (dla `basic` auth) |
| `JIRA_API_TOKEN` | API token — wygeneruj na https://id.atlassian.com/manage-profile/security/api-tokens |
| `JIRA_DEFAULT_PROJECT_KEY` | Domyślny klucz projektu (np. `TRAIN`) |
| `ENABLE_WIKI_INTEGRATION` | `true` aby włączyć integrację z Confluence |
| `WIKI_BASE_URL` | URL REST API Wiki (np. `https://INSTANCJA.atlassian.net/wiki/rest/api`) |

### 3. Konfiguracja w VS Code (`.vscode/mcp.json`)

Serwer jest już skonfigurowany w workspace. Przy starcie VS Code zapyta o email i token (używa `inputs` z maskowanym hasłem):

```json
{
  "servers": {
    "jira-wiki": {
      "command": "python",
      "args": ["jira_wiki_mcpserver.py"],
      "cwd": "<ścieżka-do-folderu>",
      "env": {
        "JIRA_BASE_URL": "https://adk-training.atlassian.net/rest/api/2",
        "JIRA_AUTH_TYPE": "basic",
        "JIRA_USER_EMAIL": "${input:jiraUserEmail}",
        "JIRA_API_TOKEN": "${input:jiraApiToken}",
        "JIRA_DEFAULT_PROJECT_KEY": "TRAIN",
        "ENABLE_WIKI_INTEGRATION": "true",
        "WIKI_BASE_URL": "https://adk-mcp-training.atlassian.net/wiki/rest/api",
        "WIKI_USER_EMAIL": "${input:jiraUserEmail}",
        "WIKI_API_TOKEN": "${input:jiraApiToken}"
      }
    }
  },
  "inputs": [
    {
      "id": "jiraUserEmail",
      "type": "promptString",
      "description": "Jira/Wiki user email"
    },
    {
      "id": "jiraApiToken",
      "type": "promptString",
      "description": "Jira/Wiki API token",
      "password": true
    }
  ]
}
```

> **Bezpieczeństwo:** Tokeny API nigdy nie powinny być commitowane do repozytorium. Użycie `${input:...}` z `password: true` zapewnia, że VS Code pyta o token przy każdym starcie i maskuje go w UI.

---

## 🚀 Użycie

### Uruchomienie lokalne (test)

```powershell
.\run_mcp_server.ps1
```

### Użycie w Copilot Chat

Po skonfigurowaniu serwera w `mcp.json`, otwórz Copilot Chat i zadaj pytanie:

- *"Pokaż mi otwarte tickety Jira w projekcie TRAIN"*
- *"Utwórz ticket: Dodać walidację formularza właściciela"*
- *"Znajdź stronę Wiki o architekturze systemu"*
- *"Pobierz szczegóły ticketa TRAIN-1"*
- *"Szukaj JQL: project = TRAIN AND status = 'To Do'"*

---

## 📁 Struktura plików

| Plik | Opis |
|------|------|
| `jira_wiki_mcpserver.py` | Główny serwer MCP — rejestruje tools za pomocą `@mcp.tool()` |
| `jira_client.py` | Klient REST API Jira (GET/POST/search) |
| `wiki_client.py` | Klient REST API Confluence Wiki |
| `.env.template` | Szablon zmiennych środowiskowych |
| `requirements.txt` | Zależności Python |
| `run_mcp_server.ps1` | Skrypt startowy (Windows PowerShell) |
| `1_test_jira_api.py` | Test połączenia z Jira API |

---

## 🔍 Rozwiązywanie problemów

| Problem | Rozwiązanie |
|---------|-------------|
| `JIRA_BASE_URL must be set` | Brak pliku `.env` lub pustą zmienną — skopiuj `.env.template` |
| `401 Unauthorized` | Nieprawidłowy email lub token API |
| `403 Forbidden` | Konto nie ma uprawnień do projektu |
| Brak narzędzi Wiki | Sprawdź `ENABLE_WIKI_INTEGRATION=true` w env |
| Serwer się nie uruchamia | `MCP: List Servers` → wybierz serwer → `Show Output` |
