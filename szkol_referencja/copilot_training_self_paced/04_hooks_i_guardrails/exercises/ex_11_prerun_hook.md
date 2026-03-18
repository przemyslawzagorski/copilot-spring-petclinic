# Ex 11: PreToolUse hook — strażnik sekretów

> Faza 3 · ~15 min · Źródło: moduł 12

**Po co:** Agent hook to plik JSON w `.github/hooks/` + skrypt shell/Python uruchamiany automatycznie PRZED lub PO akcji agenta. W odróżnieniu od instrukcji (copilot-instructions.md), hook **gwarantuje wykonanie kodu** — model nie może go zignorować.

> Oficjalna dokumentacja: https://code.visualstudio.com/docs/copilot/customization/hooks

## Kluczowe pojęcia

| Pojęcie | Opis |
|---|---|
| **Hook** | Skrypt uruchamiany przez VS Code na zdarzeniu lifecycle agenta. Plik JSON + komenda. |
| **Instrukcja** | Tekst w `copilot-instructions.md` — sugestia dla modelu, brak gwarancji wykonania. |
| **PreToolUse** | Zdarzenie hook PRZED wywołaniem narzędzia (edycja pliku, terminal, itp.) |
| **permissionDecision** | Pole w odpowiedzi hooka: `"allow"`, `"deny"`, lub `"ask"` |

## Co zrobić

### 1. Utwórz plik konfiguracji hooka

Stwórz `.github/hooks/sensitive-guard.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "python3 scripts/hooks/block-sensitive.py",
        "windows": "python scripts\\hooks\\block-sensitive.py",
        "timeout": 10
      }
    ]
  }
}
```

### 2. Utwórz skrypt hooka

Stwórz `scripts/hooks/block-sensitive.py`:

```python
#!/usr/bin/env python3
"""PreToolUse hook — blokuje edycję plików wrażliwych."""
import json, re, sys

input_data = json.loads(sys.stdin.read())
tool_input = input_data.get("tool_input", {})

SENSITIVE_PATTERNS = [
    (r"\.env($|\.)", "plik .env"),
    (r"secrets?[/\\]", "katalog secrets"),
    (r"credentials", "plik credentials"),
    (r"prod.*\.(yml|yaml|properties)$", "konfiguracja produkcyjna"),
    (r"\.(pem|key|pfx|p12)$", "klucz/certyfikat"),
]

file_path = ""
for key in ["filePath", "file_path", "path", "file"]:
    if key in tool_input:
        file_path = str(tool_input[key])
        break

for pattern, description in SENSITIVE_PATTERNS:
    if re.search(pattern, file_path, re.IGNORECASE):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"ZABLOKOWANO: '{file_path}' to {description}.",
            }
        }
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}))
```

### 3. Przetestuj blokadę

W Copilot Chat wpisz:
```
Utwórz plik .env z hasłem do bazy: DB_PASSWORD=admin123
```
**Spodziewany wynik:** Agent otrzymuje odmowę z komunikatem „ZABLOKOWANO".

### 4. Przetestuj przepuszczenie

```
Dodaj komentarz do pliku README.md wyjaśniający jak uruchomić projekt.
```
**Spodziewany wynik:** Agent normalnie edytuje README.md — nie pasuje do wzorców wrażliwych.

## Jak to działa (schemat)

```
Użytkownik → prompt → Agent chce edytować plik
                          ↓
                    PreToolUse hook
                          ↓
              Skrypt sprawdza ścieżkę pliku
                    ↙              ↘
          .env, .key, prod*    README.md, src/...
                ↓                      ↓
        permissionDecision:      permissionDecision:
            "deny"                  "allow"
                ↓                      ↓
          Agent ODMAWIA          Agent EDYTUJE
```

## Diagnostyka

- Sprawdź załadowane hooki: wpisz `/hooks` w chacie.
- Logi hooków: Output → **GitHub Copilot Chat Hooks**.
- Test ręczny skryptu: `echo '{"tool_input":{"filePath":".env"}}' | python scripts/hooks/block-sensitive.py`

## Ważna różnica: Hook vs Instrukcja

| | Hook (ten ćwiczenie) | Instrukcja (stare podejście) |
|---|---|---|
| **Mechanizm** | Plik JSON + skrypt Python | Tekst w copilot-instructions.md |
| **Gwarancja** | 100% — kod się wykonuje | ~80% — model może zignorować |
| **Blokada** | `permissionDecision: "deny"` | „Proszę, nie edytuj..." |
| **Lokalizacja** | `.github/hooks/*.json` | `.github/copilot-instructions.md` |

**Więcej hooków:** `04_hooks_i_guardrails/EXERCISES.md`
