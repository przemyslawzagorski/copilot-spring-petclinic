# Ex 24: Hardening i smoke test MCP

> Faza 7 · ~10 min · Źródło: moduł 11

**Po co:** Serwer działa, ale nie jest gotowy na realny świat. Dodajesz: timeout, error handling, limit output, scenariusze testowe.

## Co zrobić

1. W Copilot Chat wpisz:

```
Do MCP servera dodaj:
1. Globalny timeout klienta HTTP: 5s
2. Obsługę błędów: nigdy nie zwracaj stack trace do klienta, loguj pełny błąd na serwerze
3. Limit długości odpowiedzi: max 1200 znaków
4. Utwórz plik TEST_SCENARIOS.md z 4 testami curl: 2 pozytywne, 2 negatywne (userId=abc, brak messages)
```

2. Uruchom każdy test z `TEST_SCENARIOS.md` ręcznie.

**Checklist gotowości:**
- [ ] Healthcheck działa (GET /)
- [ ] Pozytywny test zwraca dane (max 5 postów)
- [ ] Negatywny test zwraca czytelny błąd (nie stack trace)
- [ ] Timeout nie zawiesza serwera
- [ ] Odpowiedź nie przekracza 1200 znaków

**Brawo!** Zbudowałeś MCP Server od zera. To jest moduł który na szkoleniach robi największe wrażenie.

**Więcej:** `11_module_11_mcp_fastapi_from_scratch/EXERCISES.md` — ćwiczenie 3
