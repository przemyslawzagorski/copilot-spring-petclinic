# Ex 35: Capstone — jedno zadanie, wszystkie trzy filary naraz 🅱️

> Moduł 11 (bonus) · Wszystkie filary · ~30 min · Bonus

**Po co:** Recepty z ex_32–34 nie działają osobno — działają **razem**. Tu przeprowadzasz jedno realne zadanie end-to-end, świadomie stosując pętlę agentic (Filar 1), pilnując budżetu tokenów (Filar 2) i dobierając narzędzia do warstw (Filar 3). To Twój „egzamin praktyczny" z całego modułu.

**Zadanie referencyjne:** dodać do PetClinic endpoint **wyszukiwania weterynarzy po specjalności** (`GET /vets?specialty=radiology`) — kontroler, prosta logika filtrująca, test, review bezpieczeństwa. Jeśli wolisz, wybierz inną funkcję o podobnej wielkości.

---

## Co zrobić — przebieg z jawną kontrolą wszystkich 3 filarów

### Faza 0 — Higiena startu (Filar 2)

```
/clear          # czysty kontekst na nowe zadanie
/context        # zapamiętaj punkt startowy budżetu
/model sonnet   # rutynowa robota → tańszy model na start
```

### Faza 1 — Zbadaj (Filar 1 + 2)

Celowany prompt (nie „przejrzyj projekt"):

```
Przeczytaj TYLKO vet/VetController.java i vet/VetRepository.java.
Pokaż, jak dziś pobierane są weterynarze i czy Specialty jest już mapowane.
Bez kodu.
```

> Filar 2 w akcji: wskazujesz dokładne pliki → mniej tokenów, mniej context rot.

### Faza 2 — Zaplanuj (Filar 1)

```
Tryb plan: endpoint GET /vets?specialty=. Daj listę plików, kryteria sukcesu,
walidację parametru (whitelista specjalności? sanityzacja?), ryzyka, rollback.
Najpierw zatwierdzę.
```

Popraw plan słowem, jeśli pomija walidację wejścia (to projekt szkoleniowy — `CLAUDE.md` wymaga: „zawsze waliduj dane wejściowe").

### Faza 3 — Deleguj wg warstw (Filar 1 + 3)

| Warstwa | Komu | Prompt (skrót) |
|---------|------|----------------|
| Implementacja | `feature-builder` | „zaimplementuj plan endpointu /vets?specialty=, trzymaj się listy plików" |
| Testy | `tdd-expert` | „test: znana specjalność zwraca wyniki; nieznana/pusta → pusty wynik, nie 500" |
| Gadatliwy skan | `security-expert` | „TYLKO lista plik:linia + ryzyko dla parametru specialty (injection?)" — streszczenie, nie kod (Filar 2) |

### Faza 4 — Zweryfikuj + cross-check krytycznej części (Filar 1 + 3)

```
1) Testy:
   ./mvnw -Dtest=VetSearchTest test

2) Cross-check walidacji parametru (zmiana wrażliwa → 2 niezależne oceny):
   @"reviewer (agent)" oceń obsługę parametru specialty: poprawność + edge-case.
   @"security-expert (agent)" oceń ten sam parametr: injection / niedozwolone wartości.

   Zgodne → merge. Rozbieżne → tam skup uwagę.
```

### Faza 5 — Domknięcie budżetu (Filar 2)

```
/context        # porównaj z punktem startowym z Fazy 0 — ile zjadło zadanie?
/compact        # jeśli sesja ma iść dalej
```

---

## Spodziewany wynik

Działający, przetestowany i zreviewowany endpoint — ale prawdziwym produktem jest **świadomy przebieg**: w każdej fazie wiesz, którego filaru używasz i dlaczego.

Wypełnij krótką retrospektywę:

| Filar | Gdzie zadziałał | Co bym poprawił następnym razem |
|-------|-----------------|----------------------------------|
| 1 · Pętla agentic | | |
| 2 · Tokeny | | |
| 3 · Multinarzędziowość | | |

## Checklist walidacji

- [ ] Start od `/clear` + `/context` (znasz punkt odniesienia budżetu).
- [ ] Badanie celowane (konkretne pliki), nie „przejrzyj projekt".
- [ ] Plan zatwierdzony przed kodem; uwzględnia walidację wejścia.
- [ ] Praca rozdzielona na min. 3 subagentów wg warstw.
- [ ] Testy uruchomione z widocznym wynikiem.
- [ ] Cross-check walidacji parametru dwoma niezależnymi agentami.
- [ ] `/context` na końcu — wiesz, ile tokenów kosztowało zadanie.
- [ ] Retrospektywa 3 filarów wypełniona.

## Gratulacje 🎉

Przeszedłeś moduł 11. Masz trzy recepty, które stosujesz od następnego zadania:
1. **Pętla:** zbadaj → zaplanuj → deleguj → zweryfikuj.
2. **Tokeny:** diagnozuj (`/context`), tnij (lean instrukcje, celowane pliki), kompaktuj (`/compact` @ ~70%).
3. **Multi-tool:** narzędzie do warstwy, cross-check dla krytycznych, wspólny MCP, osobne gałęzie.

**Więcej:** [README modułu 11](../README.md) · [START_HERE](../../START_HERE.md)
