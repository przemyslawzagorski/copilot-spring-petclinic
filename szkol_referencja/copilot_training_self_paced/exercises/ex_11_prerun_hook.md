# Ex 11: Pre-run hook — guardrail

> Faza 3 · ~10 min · Źródło: moduł 03 + 12

**Po co:** Hook to automatyczna komenda uruchamiana PRZED lub PO akcji Copilota. Wymusza reguły, których prompt nie gwarantuje.

## Co zrobić

1. Dodaj do `.github/copilot-instructions.md` (lub utwórz osobny plik):

```markdown
## Hooks

### Pre-run: ochrona plików wrażliwych
Przed modyfikacją plików pasujących do wzorców:
- `.env`, `**/secrets/**`, `**/prod*.yml`
Copilot musi się upewnić, że w prompcie jest fraza `CONFIRM_SENSITIVE_EDIT`.
W przeciwnym razie — odmów modyfikacji i wyjaśnij dlaczego.
```

2. Przetestuj — w chacie wpisz:

```
Zmodyfikuj plik application.properties i dodaj hasło do bazy danych.
```

3. Copilot powinien odmówić lub ostrzec (bo brak `CONFIRM_SENSITIVE_EDIT`).

4. Teraz wpisz:

```
CONFIRM_SENSITIVE_EDIT — dodaj komentarz do application.properties wyjaśniający konfigurację H2.
```

**Spodziewany wynik:** Przy pierwszym prompcie odmowa/ostrzeżenie. Przy drugim — wykonanie.

**Uwaga:** To hook "miękki" (oparty na instructions). Moduł 12 pokazuje hooki twarde (skryptowe).

**Więcej:** `12_module_12_hooks_vs_prompts/README.md`
