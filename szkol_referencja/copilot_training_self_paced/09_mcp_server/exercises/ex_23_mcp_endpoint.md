# Ex 23: Endpoint MCP z publicznym API

> Faza 7 · ~12 min · Źródło: moduł 11

**Po co:** MCP Server odbiera prompt od Copilota i zwraca dane z zewnętrznego źródła. Tu: JSONPlaceholder.

## Co zrobić

1. W Copilot Chat wpisz (mając otwarty folder mcp_server/):

```
Dodaj endpoint POST /v1/mcp/prompt do app/mcp_handler.py.
Jeśli prompt zawiera "posts user <id>", pobierz posty użytkownika z https://jsonplaceholder.typicode.com/posts?userId=<id> (max 5 wyników).
Dla innych zapytań zwróć fallback: "Nie rozumiem zapytania."
Zwróć odpowiedź w formacie: {"response": {"choices": [{"message": {"content": "...", "role": "assistant"}}]}}
Waliduj userId jako dodatnią liczbę. Dodaj timeout 5s na HTTP call.
```

2. Przetestuj curlem:

```
curl -X POST http://localhost:8000/v1/mcp/prompt -H "Content-Type: application/json" -d "{\"messages\": [{\"content\": \"posts user 1\", \"role\": \"user\"}]}"
```

**Spodziewany wynik:** JSON z podsumowaniem max 5 postów użytkownika 1.

**Test negatywny:**
```
curl -X POST http://localhost:8000/v1/mcp/prompt -H "Content-Type: application/json" -d "{\"messages\": [{\"content\": \"posts user abc\", \"role\": \"user\"}]}"
```

Powinien zwrócić komunikat błędu, nie 500.

**Więcej:** `09_mcp_server/EXERCISES.md`
