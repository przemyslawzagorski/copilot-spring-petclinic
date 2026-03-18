# TDD z Copilotem

## 🎯 Cele modułu

- Przeprowadzić pełny cykl Red-Green-Refactor z aktywnym wsparciem Copilota.
- Generować testy jednostkowe z użyciem JUnit 5 + Mockito.
- Debugować z Copilotem: analiza stack trace, sugestie poprawek.
- Poznać self-correction loop — agent naprawia własne błędy.

---

## 📚 Teoria

### Cykl TDD z Copilotem

```
RED   → Napisz failujący test (Copilot generuje szkielet)
GREEN → Minimalna implementacja (Copilot sugeruje kod pod test)
REFACTOR → Ulepszenie bez łamania testów (Copilot refaktoryzuje)
```

### RED — generowanie testów

Copilot doskonale generuje testy z kontekstu. Wystarczy:
- komentarz z intencją: `// test: should return empty list when no visits found`
- albo prompt w Chat: `Napisz test jednostkowy JUnit 5 dla metody findByLastName w OwnerRepository`

**Zasada:** Test powinien failować — jeśli przechodzi od razu, albo jest za prosty, albo metoda już istnieje.

### GREEN — minimalna implementacja

Po dodaniu sygnatury metody otwórz klamrę `{` — Copilot zaproponuje implementację na bazie:
- nazwy metody i parametrów,
- istniejącego testu,
- konwencji w projekcie (z `copilot-instructions.md`).

**Zasada:** Implementuj minimum potrzebne do przejścia testu. Nie optymalizuj w fazie GREEN.

### REFACTOR — ulepszanie z Copilotem

Zaznacz kod → `Ctrl+I` → „Zrefaktoryzuj tę metodę — uprość, usuń duplikaty, zachowaj zachowanie."

Copilot może:
- wyciągnąć private method,
- zastąpić pętlę Stream API,
- uprościć warunki logiczne,
- poprawić nazewnictwo.

**Po każdej zmianie:** uruchom testy. Testy muszą przechodzić — inaczej cofnij.

### Debugowanie z Copilotem

1. **Stack trace:** Wklej cały stack trace do Chat → „Zanalizuj ten stack trace i zaproponuj przyczynę."
2. **Zmienna:** Zaznacz fragment → `Ctrl+I` → „Dlaczego ta zmienna może być null?"
3. **Git diff:** „Porównaj moje zmiany i powiedz, co mogło wprowadzić ten błąd."

### Self-correction loop (bonus)

Agent w trybie autonomicznym potrafi:
1. Wygenerować kod
2. Uruchomić testy
3. Zobaczyć błędy
4. Naprawić je sam
5. Powtarzać aż testy przejdą

To wymaga trybu **Agent** z dostępem do terminala.

---

## 📝 Ćwiczenia

| # | Ćwiczenie | Czas |
|---|-----------|------|
| ex_13 | TDD Red — napisz failujący test | ~10 min |
| ex_14 | TDD Green — minimalna implementacja | ~10 min |
| ex_15 | TDD Refactor — ulepszenie bez łamania testów | ~10 min |
| 🅱️ ex_15b | Self-Correction Loop — agent naprawia własne błędy | ~10 min |

Pliki ćwiczeń: `exercises/`
