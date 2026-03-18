# Ex 18: Hook vs Prompt — kiedy co

> Faza 5 · ~10 min · Źródło: moduł 12

**Po co:** Najważniejsza decyzja architektoniczna w customizacji: co wymuszać hookiem (plik JSON + skrypt), a co sugerować promptem/instrukcją (tekst dla modelu).

> Oficjalna dokumentacja hooków: https://code.visualstudio.com/docs/copilot/customization/hooks

## Przypomnienie: czym jest hook

Hook to **nie** reguła w `copilot-instructions.md`. To plik JSON w `.github/hooks/` uruchamiający komendę shell na zdarzeniu agenta:

```json
{
  "hooks": {
    "PreToolUse": [{
      "type": "command",
      "command": "python3 scripts/hooks/block-sensitive.py"
    }]
  }
}
```

**8 zdarzeń lifecycle:** SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PreCompact, SubagentStart, SubagentStop, Stop.

## Co zrobić

W Copilot Chat wpisz:

```
Dla poniższych 6 przypadków zaproponuj: Hook, Prompt, czy Hook+Prompt.
Odpowiedz w tabeli: przypadek | wybór | dlaczego | ryzyko jeśli źle wybierzesz.

1. Ochrona plików z sekretami (.env, credentials)
2. Wymuszenie stylu commit message (conventional commits)
3. Refaktoryzacja metody na mniejsze
4. Auto-lint po każdej zmianie
5. Security review przed mergem
6. Generowanie dokumentacji API
```

## Ocena odpowiedzi

| # | Optymalnie | Dlaczego | Ryzyko złego wyboru |
|---|---|---|---|
| 1 | **Hook** | Musi deterministycznie blokować — prompt może „zapomnieć" | Wyciek sekretów |
| 2 | **Hook** | Walidacja formatu to enforcement, nie kreacja | Niespójne commity |
| 3 | **Prompt** | Kreatywna zmiana, wynik zależy od kontekstu kodu | Sztywny refactoring bez sensu |
| 4 | **Hook** | Automatyzacja niezależna od promptu | Niespójne formatowanie |
| 5 | **Hook+Prompt** | Hook uruchamia skan, prompt analizuje wyniki | Fałszywe poczucie bezpieczeństwa lub blokada bez analizy |
| 6 | **Prompt** | Generowanie treści wymaga modelu | Pusta dokumentacja (hook nie „myśli") |

## Zasada ogólna

```
Enforcement (blokada, walidacja, format, audit)  →  Hook
Kreacja (generowanie, refactoring, analiza)      →  Prompt
Enforcement + analiza                            →  Hook + Prompt
```

## Które zdarzenie hook do którego przypadku?

| Przypadek | Zdarzenie hook | Mechanizm |
|---|---|---|
| Ochrona sekretów | **PreToolUse** | `permissionDecision: "deny"` |
| Wymuszenie commit msg | **PreToolUse** (na narzędziu git) | Walidacja formatu komendy |
| Auto-lint | **PostToolUse** | Uruchomienie lintera po edycji |
| Security review | **PreToolUse** + **Stop** | Skan przed operacją + raport na koniec |
| Audyt | **UserPromptSubmit** | Logowanie promptów |

**Więcej:** `04_hooks_i_guardrails/EXERCISES.md`
