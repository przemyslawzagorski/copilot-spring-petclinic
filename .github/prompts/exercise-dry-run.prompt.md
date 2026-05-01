---
agent: "agent"
argument-hint: "Numer modułu (01-08, 10) do przetestowania"
description: "Dry-run ćwiczeń z wybranego modułu — wykonuje kluczowe kroki i raportuje pass/fail"
---

## Cel

Wykonaj dry-run ćwiczeń z modułu **${input:module}** w `szkol_referencja/copilot_training_self_paced/`.

Obsługiwane moduły: 01, 02, 03, 04, 05, 06, 07, 08, 10. Moduł 09 (MCP) i `mkdocs_doc/` mają specyficzne wymagania środowiskowe — pomiń jeśli user nie poprosi wprost.

## Instrukcje

1. Utwórz branch testowy: `git checkout -b test/dry-run-module-${input:module}`
2. Przeczytaj `EXERCISES.md` z modułu — pobierz listę ćwiczeń.
3. Dla każdego ćwiczenia:
   a. Przeczytaj plik ćwiczenia z `exercises/`
   b. Wykonaj **kluczowy krok** — ten, który tworzy plik, generuje kod, lub uruchamia komendę
   c. Sprawdź rezultat (plik istnieje? kompilacja przechodzi? test przechodzi?)
   d. Zapisz wynik: PASS / FAIL / SKIP (z uzasadnieniem)
4. Po wszystkich ćwiczeniach: `git checkout main` (zostaw branch do review)

## Czego NIE robić

- Nie testuj modułu 09 (MCP) ani mkdocs — chyba że użytkownik poprosi.
- Nie pushuj brancha testowego.
- Nie naprawiaj błędów w ćwiczeniach — tylko raportuj.
- Ćwiczenia subiektywne (np. "zapytaj Copilot o...") oznacz jako SKIP — nie da się ich automatycznie zweryfikować.

## Klasyfikacja ćwiczeń

- **Weryfikowalne** (tworzą pliki): ex_08, ex_09, ex_10, ex_11, ex_12, ex_19, ex_20, ex_21 → sprawdź czy plik powstaje i jest poprawny
- **Kompilowalne** (generują kod/testy): ex_02, ex_06, ex_07, ex_13, ex_14, ex_15 → wygeneruj, skompiluj, uruchom test
- **Subiektywne** (odpowiedzi tekstowe): ex_01, ex_05, ex_16 → SKIP z adnotacją
- **Konfiguracyjne** (ustawienia VS Code): ex_03b, ex_08b, ex_10b → SKIP (wymagają interakcji z UI)
- **Python SDK (moduł 10)** — wymagają osobnego `.venv` w katalogu modułu i zainstalowanego `github-copilot-sdk`:
  - ex_25 → **Konfiguracyjne** — sprawdź czy `pip install` przechodzi i `smoke_test.py` drukuje listę modeli (SKIP jeśli brak Pythona 3.11+)
  - ex_26, ex_27, ex_28, ex_29 → **Kompilowalne** — uruchom skrypt, sprawdź exit code 0 i obecność spodziewanych artefaktów (np. `petclinic_domain_report.md` po ex_27). SKIP jeśli brak autoryzacji Copilot.

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

Usuń lub przywróć wszelkie zmiany w plikach projektu: `git checkout main`
