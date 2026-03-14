# Ex 18: Hook vs Prompt — kiedy co

> Faza 5 · ~10 min · Źródło: moduł 12

**Po co:** Najważniejsza decyzja architektoniczna w customizacji: co wymuszać hookiem, a co sugerować promptem.

## Co zrobić

W Copilot Chat wpisz:

```
Dla poniższych 6 przypadków zaproponuj: Hook, Prompt, czy Hook+Prompt. Odpowiedz w tabeli: przypadek | wybór | dlaczego | ryzyko jeśli źle wybierzesz.

1. Ochrona plików z sekretami (.env, credentials)
2. Wymuszenie stylu commit message (conventional commits)
3. Refaktoryzacja metody na mniejsze
4. Auto-lint po każdej zmianie
5. Security review przed mergem
6. Generowanie dokumentacji API
```

## Ocena odpowiedzi

Prawidłowe odpowiedzi:
| # | Optymalnie |
|---|-----------|
| 1 | **Hook** — musi blokować, prompt nie gwarantuje |
| 2 | **Hook** — walidacja formatu to enforcement |
| 3 | **Prompt** — kreatywna zmiana, nie da się wymusić |
| 4 | **Hook** — automatyzacja, nie zależy od promptu |
| 5 | **Hook+Prompt** — hook uruchamia, prompt analizuje |
| 6 | **Prompt** — generowanie treści, nie enforcement |

**Zasada:** Enforcement → Hook. Kreacja → Prompt. Kombinacja → oba.

**Więcej:** `12_module_12_hooks_vs_prompts/EXERCISES.md` — ćwiczenie 3
