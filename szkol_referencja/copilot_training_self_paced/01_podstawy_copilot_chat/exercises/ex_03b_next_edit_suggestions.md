# Ex 03b: Next Edit Suggestions — predykcja następnej zmiany

> Bonus · ~5 min · Między ex_03 a ex_04

**Po co:** Po dokonaniu jednej zmiany Copilot próbuje **przewidzieć, co zrobisz dalej** i podświetla sugestię. Wystarczy nacisnąć Tab.

## Co zrobić

1. Otwórz `Owner.java`
2. Znajdź pole `firstName` i zmień nazwe getter z `getFirstName` na `retrieveFirstName` (ręcznie)
3. **Nie rób nic** — poczekaj 1-2 sekundy
4. Copilot powinien podświetlić kolejną edycję: zmianę `getLastName` → `retrieveLastName` (spójny wzorzec)
5. Naciśnij **Tab** aby zaakceptować, lub **Esc** aby odrzucić

## Drugi scenariusz

1. Otwórz `OwnerController.java`
2. Dodaj adnotację `@Valid` przed parametrem `Owner owner` w jednej metodzie
3. Copilot zasugeruje dodanie `@Valid` w kolejnych metodach z tym samym parametrem
4. Tab → Tab → Tab — kolejne sugestie w łańcuchu

**Spodziewany wynik:** Copilot przewiduje powtarzalne edycje na podstawie wzorca Twojej ostatniej zmiany.

**Nie widzisz sugestii?** Upewnij się, że masz włączone: Settings → `editor.inlineSuggest.enabled: true` i `github.copilot.nextEditSuggestions.enabled: true`.

**Kiedy NES się sprawdza?** Mechaniczne, powtarzalne zmiany: rename, dodanie adnotacji, zmiana typu w wielu miejscach. NIE sprawdza się przy zmianach logiki.
