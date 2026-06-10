# Ex 33: Recepta na pętlę agentic — zbadaj → zaplanuj → deleguj → zweryfikuj

> Moduł 11 (bonus) · Filar 1 · ~25 min · Źródło: Anthropic / Cognition (2026)

**Po co:** Agent kręci pętlę *plan → akcja → obserwacja → korekta*. Jeśli wrzucisz mu „zrób funkcję X" bez ramy — dostaniesz ładny kod, który nie pasuje do projektu. Tu ćwiczysz **sterowanie pętlą** na realnym, małym zadaniu w PetClinic.

**Zadanie referencyjne:** dodać walidację pola `telephone` w encji `Owner` (dokładnie 9 cyfr) + test. Małe, ale dotyka encji, kontrolera i testów — idealne do pętli.

---

## Co zrobić

### Krok 1 — ZBADAJ (nie pozwól pisać od razu)

Agenty spędzają ~60% czasu na szukaniu kontekstu. Skróć to — każ *najpierw przeczytać*, dopiero potem działać:

```
Zanim cokolwiek zmienisz: przeczytaj Owner.java i OwnerController.java.
Pokaż, gdzie dziś jest walidacja telephone i jakiej biblioteki walidacji
używa projekt. NIE pisz jeszcze kodu.
```

✅ Dobrze, jeśli agent wskaże konkretne pliki/adnotacje (`@Pattern`, `jakarta.validation`) zanim zaproponuje zmianę.

### Krok 2 — ZAPLANUJ (plan-before-build)

Wymuś tryb planu — w Claude Code `Shift+Tab` (plan mode) lub agent `Plan`; w Copilot agent `@plan`:

```
Tryb plan: zaproponuj plan dodania walidacji telephone = dokładnie 9 cyfr.
Chcę: listę plików do zmiany, kryteria sukcesu, warunek rollback, ryzyka.
Bez kodu — najpierw zatwierdzę plan.
```

Przeczytaj plan. Plan jest **tani** (mało tokenów) i łatwy do poprawienia. Zły kod jest **drogi** do cofnięcia. Popraw plan słowem, np. „test ma sprawdzać też przypadek 10 cyfr → odrzucony".

### Krok 3 — DELEGUJ (rozdziel kontekst)

Nie każ jednemu agentowi robić wszystkiego — „przepala własny kontekst". Rozdziel na subagentów z osobnym kontekstem (multi-agent z dedykowanym kontekstem: +90% jakości w badaniach Anthropic):

```
1) Implementację oddaj feature-builderowi:
   @"feature-builder (agent)" zaimplementuj plan walidacji telephone (9 cyfr)
   w Owner. Trzymaj się WYŁĄCZNIE listy plików z planu.

2) Test oddaj ekspertowi TDD:
   @"tdd-expert (agent)" napisz test JUnit 5 sprawdzający, że telephone
   z 9 cyframi przechodzi, a 8 i 10 cyfr jest odrzucane.
```

> Repo ma tych agentów gotowych — patrz `.github/agents/` i `.claude/agents/`.

### Krok 4 — ZWERYFIKUJ (zamknij pętlę)

Nie ufaj „na słowo". Każ agentowi *pokazać dowód* i przejść niezależnym review:

```
1) Uruchom testy i wklej wynik:
   ./mvnw -Dtest=OwnerValidationTest test

2) Niezależne review:
   @"reviewer (agent)" oceń zmianę walidacji telephone.
   Raport w kategoriach Critical/Major/Minor.
```

To jest **self-correction loop**: review łapie rzeczy, których implementer nie przewidział (np. komunikat błędu po polsku, brak `@NotBlank`, regex dopuszczający spacje).

### Krok 5 — Refleksja nad pętlą

Zapisz w 3 zdaniach: gdzie agent chciał „przeskoczyć" badanie/plan i od razu pisać kod? Co złapał reviewer? Ile iteracji korekty było potrzebne?

---

## Spodziewany wynik

- Walidacja `telephone` (9 cyfr) działa, test przechodzi, review czysty.
- Co ważniejsze: masz **trzy różne perspektywy** na jedno zadanie (implementer ≠ tester ≠ reviewer), każda z osobnym kontekstem.
- Widzisz na żywo, że plan-before-build oszczędza cofanie złego kodu.

## Checklist walidacji

- [ ] Agent NAJPIERW przeczytał `Owner.java` / `OwnerController.java`, zanim zaproponował zmianę.
- [ ] Powstał plan (lista plików + kryteria + rollback) i zatwierdziłeś go *przed* kodem.
- [ ] Implementacja i testy poszły do **różnych** subagentów (osobny kontekst).
- [ ] Testy uruchomione, wynik widoczny (nie „powinno działać").
- [ ] Niezależny reviewer dał raport Critical/Major/Minor.
- [ ] Masz notatkę z refleksji o przebiegu pętli.

**Więcej:** [README — Filar 1](../README.md) · moduł 08 (Custom Agenty) · moduł 06 (TDD self-correction)
