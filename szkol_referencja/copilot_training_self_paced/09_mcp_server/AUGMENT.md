# Moduł 09 - MCP Server: adaptacja dla Augmenta

> Kod serwerów FastMCP pozostaje bez zmian. Zmienia się klient i lokalizacja
> konfiguracji. Repo nie aktywuje MCP automatycznie.

## Ex 22: bootstrap serwera

W WSL utwórz środowisko Python i wykonaj bootstrap FastAPI/FastMCP zgodnie z
oryginalnym ćwiczeniem. Do analizy planu użyj `/plan`, a kod zweryfikuj tym samym
healthcheckiem co w materiale bazowym.

Gdy serwer jest gotowy, dodaj go lokalnie do Auggie:

```bash
auggie mcp add publiczne-api -- python3 szkol_referencja/copilot_training_self_paced/mcp_ex_api/api_sever.py
auggie mcp list
```

Po ćwiczeniu usuń wpis:

```bash
auggie mcp remove publiczne-api
```

Nie commituj konfiguracji zawierającej tokeny, hasła ani adres prywatnej usługi.

## Ex 23: endpoint z publicznym API

Zaimplementuj endpoint i integrację z publicznym API według oryginalnego
ćwiczenia. W sesji Auggie sprawdź, czy model odnajduje narzędzie, czy argumenty
są walidowane i czy błędy zewnętrznego API nie ujawniają szczegółów serwera. Kod
FastMCP pozostaje provider-agnostic.

## Ex 24: hardening i smoke test

Poproś Auggie o dodanie timeoutu, bezpiecznej obsługi błędów, limitu odpowiedzi i
`TEST_SCENARIOS.md`. Uruchom dwa pozytywne i dwa negatywne testy. Nie pozwalaj
agentowi logować tokenów ani zwracać stack trace klientowi.

Przy wielu serwerach można użyć `enableToolSearch`, aby schematy wszystkich
narzędzi nie zajmowały stale kontekstu. Agent dostaje wtedy `find-tool` i
`execute-tool`.

## Ex 24b: projekt końcowy

W fazie planowania użyj `/plan`. Cykl test-first deleguj do `tdd-expert`, a
kontroler do read-only `reviewer`. Oglądaj `/diffs` po każdej fazie i zakończ
pełnym testem Maven. Augment nie używa deklaratywnego `handoffs:`; kolejność
delegacji koordynuje agent główny.

Konfigurację localhost utrzymuj lokalnie. Nie zmieniaj commitowanego
`.augment/settings.json` i nie wpisuj sekretu do frontmattera agenta.

Szczegóły i transporty `stdio`, `http`, `sse` opisuje
`../../augment_guide/README.md`.