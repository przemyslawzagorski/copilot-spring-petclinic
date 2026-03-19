# MCP Agent — Zewnętrzny serwer MCP (SSE)

## 📚 Wstęp teoretyczny

### Czym jest MCP?

**Model Context Protocol (MCP)** to otwarty standard opracowany przez Anthropic, który definiuje sposób komunikacji między agentami AI (klientami) a zewnętrznymi źródłami danych i narzędziami (serwerami). MCP pozwala agentowi Copilot na:

- **Tools** — wywoływanie funkcji (np. `get_exchange_rate`, `navigate_pirate_ship`)
- **Resources** — odczyt danych kontekstowych (pliki, bazy danych, odpowiedzi API)
- **Prompts** — korzystanie z gotowych szablonów promptów udostępnianych przez serwer

```
VS Code (Copilot)  ──MCP──>  MCP Server  ──>  API / DB / pliki
     klient                    serwer           źródło danych
```

Copilot jest **klientem MCP**. Serwer MCP to osobny proces komunikujący się z klientem przez jeden z obsługiwanych transportów.

---

### Typy transportu MCP

Specyfikacja MCP definiuje **dwa standardowe mechanizmy transportu** oraz możliwość tworzenia transportów niestandardowych:

#### 1. `stdio` (Standard Input/Output)

Najprostszy i najczęściej używany transport do serwerów **lokalnych**.

| Cecha | Opis |
|-------|------|
| **Jak działa** | Klient uruchamia serwer MCP jako podproces. Komunikacja odbywa się przez `stdin`/`stdout` procesu. |
| **Format** | Wiadomości JSON-RPC rozdzielane znakiem nowej linii. |
| **Kiedy używać** | Serwery lokalne — narzędzia CLI, skrypty Python/Node.js, integracje z lokalną bazą danych. |
| **Bezpieczeństwo** | Proces działa z uprawnieniami użytkownika. Brak ekspozycji sieciowej. |
| **Przykład w VS Code** | `"command": "python", "args": ["server.py"]` |

```
Klient                     Serwer (subprocess)
  │── uruchom proces ──────>│
  │── stdin (JSON-RPC) ────>│
  │<── stdout (JSON-RPC) ───│
  │<── stderr (logi, opcj.) │
  │── zamknij stdin ────────>│ (koniec)
```

#### 2. `sse` (Server-Sent Events) — HTTP+SSE (starszy protokół)

Transport **sieciowy** z wersji specyfikacji 2024-11-05. Klient łączy się przez HTTP, a serwer streamuje odpowiedzi przez SSE.

| Cecha | Opis |
|-------|------|
| **Jak działa** | Klient wysyła GET na endpoint SSE, otrzymuje URL do wysyłania POST-ów. Serwer streamuje odpowiedzi przez Server-Sent Events. |
| **Kiedy używać** | Serwery **zdalne** — usługi w chmurze, współdzielone narzędzia zespołowe. |
| **Bezpieczeństwo** | Wymaga walidacji `Origin`, autentykacji; serwery lokalne powinny nasłuchiwać tylko na `localhost`. |
| **Przykład w VS Code** | `"type": "sse", "url": "https://example.com/mcp"` |

> **Uwaga:** SSE jest de facto **deprecated** w nowszych wersjach specyfikacji MCP na rzecz Streamable HTTP, ale wiele serwerów nadal go używa i VS Code obsługuje oba.

#### 3. Streamable HTTP (nowy standard, od 2025-03-26)

**Następca HTTP+SSE** — uproszczony i bardziej elastyczny transport sieciowy.

| Cecha | Opis |
|-------|------|
| **Jak działa** | Jeden endpoint HTTP obsługuje POST (wysyłanie żądań) i opcjonalnie GET (nasłuchiwanie). Serwer może odpowiadać zwykłym JSON lub strumieniem SSE. |
| **Sesje** | Opcjonalne zarządzanie sesjami przez nagłówek `Mcp-Session-Id`. |
| **Resumability** | Obsługa wznawiania przerwanych połączeń przez `Last-Event-ID`. |
| **Kiedy używać** | Nowe zdalne serwery MCP — pełna kontrola nad połączeniem, streaming, wieloklientowość. |
| **Przykład w VS Code** | `"type": "http", "url": "https://example.com/mcp"` |

#### 4. Custom Transports

Specyfikacja MCP jest **transport-agnostic** — klienci i serwery mogą implementować dowolne niestandardowe mechanizmy transportu (np. WebSocket, gRPC), pod warunkiem zachowania formatu JSON-RPC i cyklu życia MCP.

### Porównanie transportów

| Transport | Lokalny/Zdalny | Streaming | Sesje | Status |
|-----------|---------------|-----------|-------|--------|
| **stdio** | Lokalny | Nie | Nie | ✅ Standard |
| **SSE (HTTP+SSE)** | Zdalny | Tak | Nie | ⚠️ Deprecated (ale wspierany) |
| **Streamable HTTP** | Zdalny | Opcjonalny | Opcjonalne | ✅ Nowy standard |
| **Custom** | Dowolny | Zależy | Zależy | 🔧 Niestandardowy |

---

## 🔧 Konfiguracja

### Zewnętrzny serwer MCP (Pirat Agent)

URL serwera: `https://pirate-navigator-28948426345.us-central1.run.app`

W tym ćwiczeniu podłączamy **zdalny** serwer MCP przez transport **SSE**. Serwer udostępnia narzędzia pirackie (nawigacja, mapy skarbów itp.) i działa w Google Cloud Run.

### Konfiguracja w `.vscode/mcp.json`

Wpis dodany do pliku `.vscode/mcp.json`:

```json
{
  "servers": {
    "Zewnetrzny_Pirat_Agent": {
      "type": "sse",
      "url": "https://pirate-navigator-28948426345.us-central1.run.app/mcp"
    }
  }
}
```

- **`type: "sse"`** — transport Server-Sent Events (HTTP+SSE). Copilot łączy się z serwerem przez sieć.
- **`url`** — pełny adres endpointu MCP serwera.

> Dla porównania, serwer lokalny (np. `publiczne-api`) używa transportu `stdio` i definiuje `command` + `args` zamiast `url`.

### Jak przetestować

1. Otwórz Copilot Chat (`Ctrl+Alt+I`).
2. Sprawdź, czy serwer się uruchomił — w czacie kliknij **Configure Tools** i poszukaj narzędzi z serwera `Zewnetrzny_Pirat_Agent`.
3. Zadaj pytanie wykorzystujące narzędzia pirackie, np.:
   - *"Użyj narzędzi pirackich do nawigacji"*
   - *"Jakie narzędzia udostępnia piracki serwer MCP?"*

### Rozwiązywanie problemów

- **Serwer się nie uruchamia** — sprawdź logi: `MCP: List Servers` → wybierz serwer → `Show Output`.
- **Brak narzędzi** — upewnij się, że ufasz serwerowi (VS Code pyta o trust przy pierwszym uruchomieniu).
- **Timeout** — serwer zdalny może być cold-startowany (Google Cloud Run). Poczekaj kilka sekund i spróbuj ponownie.