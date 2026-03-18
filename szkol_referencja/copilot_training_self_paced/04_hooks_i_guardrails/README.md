# Hooks i guardrails

> Źródło: https://code.visualstudio.com/docs/copilot/customization/hooks
> Status: **Preview** (marzec 2026)

## 🎯 Cele modułu

- Zrozumieć czym są agent hooks — komendy shell uruchamiane automatycznie w kluczowych momentach sesji.
- Odróżnić hooki (enforcement = gwarantowane wykonanie kodu) od promptów/instrukcji (guidance = sugestie).
- Skonfigurować hooki dla każdego z **8 zdarzeń cyklu życia** sesji agenta.
- Umieć zdecydować: kiedy hook, kiedy prompt, kiedy oba.

---

## 📚 Teoria

### Czym jest hook?

Hook to **plik JSON** w `.github/hooks/` definiujący komendę shell, która uruchamia się automatycznie w określonym momencie pracy agenta. W odróżnieniu od instrukcji, hook:

- **wykonuje prawdziwy kod** — skrypt, komendę, narzędzie,
- **ma gwarantowany wynik** — exit code, JSON output, blokada operacji,
- **działa niezależnie od promptu** — nie zależy od „dobrej woli" modelu.

### Anatomia hooka

```
.github/hooks/security.json          ← plik konfiguracyjny
scripts/hooks/block-sensitive.py     ← skrypt wykonywany przez hook
```

Minimalny plik hooka:
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

### 8 zdarzeń cyklu życia (lifecycle events)

| Zdarzenie | Kiedy | Przykład użycia |
|-----------|-------|-----------------|
| **SessionStart** | Nowa sesja | Wstrzyknięcie kontekstu projektu |
| **UserPromptSubmit** | Użytkownik wysyła prompt | Audyt/logowanie promptów |
| **PreToolUse** | Przed wywołaniem narzędzia | Blokada operacji niebezpiecznych |
| **PostToolUse** | Po zakończeniu narzędzia | Auto-format, walidacja, motywator |
| **PreCompact** | Przed kompakcją kontekstu | Zapis stanu przed utratą kontekstu |
| **SubagentStart** | Uruchomienie subagenta | Śledzenie subagentów |
| **SubagentStop** | Zakończenie subagenta | Agregacja wyników |
| **Stop** | Koniec sesji | Przypomnienie o testach, raport |

### Komunikacja hook ↔ VS Code

**Wejście (stdin):** Hook otrzymuje JSON:
```json
{
  "hookEventName": "PreToolUse",
  "tool_name": "replace_string_in_file",
  "tool_input": { "filePath": "src/main.ts" },
  "sessionId": "abc-123",
  "cwd": "/path/to/workspace"
}
```

**Wyjście (stdout):** Hook zwraca JSON kontrolujący zachowanie agenta:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Plik wrażliwy!"
  }
}
```

**Exit codes:**

| Kod | Znaczenie |
|-----|-----------|
| `0` | Sukces — stdout parsowany jako JSON |
| `2` | Błąd blokujący — zatrzymaj operację |
| inny | Ostrzeżenie — warning, kontynuuj |

### PreToolUse — szczegóły decyzji

| `permissionDecision` | Efekt |
|----------------------|-------|
| `"allow"` | Pozwól na operację bez pytania |
| `"deny"` | Zablokuj operację |
| `"ask"` | Pokaż użytkownikowi dialog potwierdzenia |

Dodatkowe pola w odpowiedzi:
- `updatedInput` — zmień parametry narzędzia przed wykonaniem
- `additionalContext` — dodaj kontekst dla modelu

### Hook vs Prompt — kiedy co?

| Potrzeba | Mechanizm | Dlaczego |
|----------|-----------|----------|
| **Wymusić działanie** (blokada, walidacja) | **Hook** | Gwarantowane wykonanie kodu |
| **Ukierunkować treść** (styl, konwencje) | **Prompt/Instructions** | Model potrzebuje swobody |
| **Wymusić + ukierunkować** | **Hook + Prompt** | Hook uruchamia, prompt analizuje |

### Agent-scoped hooks (Preview)

Hooki mogą być ograniczone do konkretnego agenta — definiujesz je w frontmatter `.agent.md`:

```yaml
---
name: SecureAgent
description: "Agent z dodatkową ochroną"
hooks:
  PreToolUse:
    - type: command
      command: python scripts/hooks/block-sensitive.py
---
```

Wymaga ustawienia: `chat.useCustomAgentHooks: true`

### Gdzie żyją pliki hooków

| Lokalizacja | Zasięg |
|-------------|--------|
| `.github/hooks/*.json` | Workspace (główna) |
| `.claude/settings.json` | Kompatybilność z Claude Code |
| Pole `hooks` w `.agent.md` | Tylko dla konkretnego agenta (Preview) |

### Szybki start z UI

- `/hooks` w Copilot Chat → interaktywna konfiguracja
- `/create-hook` → AI wygeneruje hook z opisu

---

## 🔗 Żywe przykłady w tym repo

W `.github/hooks/` masz **2 działające hooki** — uruchom je i zobacz efekt:

| Hook | Zdarzenie | Co robi |
|------|-----------|---------|
| `06-motivator.json` | PostToolUse | Losowa wiadomość motywacyjna po edycji pliku |
| `07-precompact.json` | PreCompact | Zapisuje notkę o kompakcji kontekstu |

Skrypty: `scripts/hooks/motivator.py` i `scripts/hooks/precompact-save.py`

Dodatkowe przykłady hookowe (gotowe do kopiowania): folder `examples/hooks/` w tym module.

---

## ⚠️ Bezpieczeństwo

- Hooki wykonują się z **takimi samymi uprawnieniami jak VS Code** — przeglądaj skrypty.
- **Nigdy nie hardcoduj sekretów** — używaj zmiennych środowiskowych.
- **Waliduj input** — hook otrzymuje dane od agenta.

---

## 📝 Ćwiczenia

| # | Ćwiczenie | Czas |
|---|-----------|------|
| ex_11 | Pre-run hook — guardrail | ~10 min |
| ex_18 | Hook vs Prompt — kiedy co | ~10 min |
| 🅱️ ex_21d | Scoped Hooks (Preview) — hooki na agenta | ~8 min |

Pliki ćwiczeń: `exercises/`

Pełny zestaw 10 ćwiczeń hookowych (zaawansowane): `examples/hooks/` + stary `EXERCISES.md` z modułu 12.
