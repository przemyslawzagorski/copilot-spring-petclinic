# Ex 03b: Next Edit Suggestions — predykcja następnej zmiany

> Bonus · ~5 min · Między ex_03 a ex_04

**Po co:** Po dokonaniu jednej zmiany Copilot próbuje **przewidzieć, co zrobisz dalej** i podświetla sugestię. Wystarczy nacisnąć Tab.

## Co zrobić

1. Otwórz `src/main/java/org/springframework/samples/petclinic/model/Person.java`

   > `firstName` i `lastName` są w klasie bazowej `Person`, **nie** w `Owner`.
   > `Owner` ma tylko `address`, `city`, `telephone` i `pets` — resztę
   > dziedziczy.

2. Zmień nazwę gettera `getFirstName` na `retrieveFirstName` (ręcznie)
3. **Nie rób nic** — poczekaj 1–2 sekundy
4. Copilot powinien podświetlić kolejną edycję: `getLastName` → `retrieveLastName` (spójny wzorzec)
5. Naciśnij **Tab** aby zaakceptować, lub **Esc** aby odrzucić

> 🧹 **Posprzątaj:** `git checkout -- src/main/java/org/springframework/samples/petclinic/model/Person.java`
> — zmieniona nazwa gettera zepsuje kompilację w innych miejscach.

## Drugi scenariusz

1. Otwórz `OwnerController.java`
2. Znajdź `processFindForm` (~linia 97) — jako jedyna z metod przyjmujących
   `Owner owner` **nie ma** adnotacji `@Valid`. Dodaj ją.
3. Copilot może zasugerować spójne zmiany w pozostałych metodach z tym samym parametrem
4. Tab → Tab — kolejne sugestie w łańcuchu

> Ten scenariusz bywa mniej wyrazisty niż pierwszy: `processCreationForm`
> i `processUpdateOwnerForm` **już mają** `@Valid`, więc wzorzec jest prawie
> domknięty. Jeśli nic nie zaproponuje — to poprawny wynik, nie błąd.

**Spodziewany wynik:** Copilot przewiduje powtarzalne edycje na podstawie wzorca Twojej ostatniej zmiany.

**Nie widzisz sugestii?** Upewnij się, że masz włączone: Settings → `editor.inlineSuggest.enabled: true` i `github.copilot.nextEditSuggestions.enabled: true`.

**Kiedy NES się sprawdza?** Mechaniczne, powtarzalne zmiany: rename, dodanie adnotacji, zmiana typu w wielu miejscach. NIE sprawdza się przy zmianach logiki.
