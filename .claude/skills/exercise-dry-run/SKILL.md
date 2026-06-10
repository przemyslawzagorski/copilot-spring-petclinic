---
name: exercise-dry-run
description: "Dry-run ćwiczeń z wybranego modułu szkoleniowego — wykonuje kluczowe kroki i raportuje PASS/FAIL/SKIP. Użyj przed szkoleniem lub gdy chcesz sprawdzić moduł."
argument-hint: "Numer modułu do przetestowania: 01, 02, 03, 04, 05, 06, 07, 08, 10"
allowed-tools: Read Bash Grep Glob
disable-model-invocation: true
---

## Cel

Wykonaj dry-run ćwiczeń z modułu **$ARGUMENTS** w `szkol_referencja/copilot_training_self_paced/`.

Obsługiwane moduły: 01, 02, 03, 04, 05, 06, 07, 08, 10.
Moduł 09 (MCP) i `mkdocs_doc/` mają specyficzne wymagania środowiskowe — pomiń jeśli nie poproszono wprost.

## Instrukcje

1. Utwórz branch testowy: `git checkout -b test/dry-run-module-$ARGUMENTS`
2. Przeczytaj plik `README.md` lub `EXERCISES.md` z modułu — pobierz listę ćwiczeń.
3. Dla każdego ćwiczenia:
   a. Przeczytaj plik ćwiczenia z `exercises/`
   b. Jeśli istnieje `CLAUDE_CODE.md` w module — użyj go zamiast oryginału (adaptacja dla Claude Code)
   c. Wykonaj **kluczowy krok** — ten, który tworzy plik, generuje kod, lub uruchamia komendę
   d. Sprawdź rezultat (plik istnieje? kompilacja przechodzi? test przechodzi?)
   e. Zapisz wynik: PASS / FAIL / SKIP (z uzasadnieniem)
4. Po wszystkich ćwiczeniach: `git checkout main` (zostaw branch do review)

## Czego NIE robić

- Nie testuj modułu 09 (MCP) ani mkdocs — chyba że użytkownik poprosi.
- Nie pushuj brancha testowego.
- Nie naprawiaj błędów w ćwiczeniach — tylko raportuj.
- Ćwiczenia subiektywne (np. "zapytaj Claude o...") oznacz jako SKIP.

## Klasyfikacja ćwiczeń

- **Weryfikowalne** (tworzą pliki): ex_08, ex_09, ex_10, ex_11, ex_12, ex_19, ex_20, ex_21 → sprawdź czy plik powstaje
- **Kompilowalne** (generują kod/testy): ex_02, ex_06, ex_07, ex_13, ex_14, ex_15 → wygeneruj, skompiluj, uruchom test
- **Subiektywne** (odpowiedzi tekstowe): ex_01, ex_05, ex_16 → SKIP z adnotacją
- **Konfiguracyjne**: ex_03b, ex_08b, ex_10b → SKIP (wymagają interakcji z UI)
- **Python SDK (moduł 10)** — wymagają `.venv` z `anthropic` (nie Copilot SDK):
  - ex_25 → sprawdź czy `pip install anthropic` przechodzi (SKIP jeśli brak Python 3.11+)
  - ex_26–ex_29 → uruchom skrypt, sprawdź exit code 0. SKIP jeśli brak ANTHROPIC_API_KEY.

## Format raportu

```markdown
## Dry-run: Moduł XX

| # | Ćwiczenie | Status | Uwagi |
|---|-----------|--------|-------|
| ex_XX | nazwa | PASS/FAIL/SKIP | komentarz |

### Podsumowanie
- PASS: X
- FAIL: Y
- SKIP: Z
- Czas: ~X min
```

## Po zakończeniu

`git checkout main` — zostaw branch testowy do ewentualnego review.
