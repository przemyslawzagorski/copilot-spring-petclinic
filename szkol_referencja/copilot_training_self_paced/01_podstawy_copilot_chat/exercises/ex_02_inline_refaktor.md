# Ex 02: Inline edit — refaktor metody

> Faza 1 · ~5 min · Moduł 01

**Po co:** Nauczyć się edytować kod bezpośrednio w pliku, bez przełączania do chatu.

## Co zrobić

1. Otwórz `src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java`
2. Zaznacz całą metodę `processFindForm` (~linia 97)
3. Naciśnij **Ctrl+I** (inline chat)
4. Wpisz:

```
Wydziel z tej metody osobną metodę prywatną odpowiedzialną za ustalenie
lastName (obsługa null → pusty string). Zachowaj zachowanie i komentarze.
```

5. Przejrzyj propozycję i kliknij Accept/Discard.

**Spodziewany wynik:** nowa metoda prywatna (np. `resolveLastName`) i wywołanie
w miejscu dotychczasowego `if (lastName == null)`. Reszta metody bez zmian.

> **Dlaczego nie „użyj Stream API"?** Bo `processFindForm` nie iteruje po
> kolekcji — to ciąg guard clause'ów zwracających różne widoki
> (`findOwners`, `redirect:`, paginacja). Nie ma tu czego zamienić na
> `.stream().filter()`. Jeśli o to poprosisz, Copilot albo odmówi, albo
> wymyśli coś sztucznego — i to jest **dobry pierwszy test** na to, czy model
> potrafi powiedzieć „to nie ma sensu". Spróbuj, jeśli chcesz zobaczyć różnicę.

**Nie działa?** Zaznacz DOKŁADNIE ciało metody (od `{` do `}`). Ctrl+I działa na zaznaczeniu.

> 🧹 **Posprzątaj:** `git checkout -- src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java`
> — kolejne ćwiczenia zakładają oryginalną treść pliku.

## Bonus: Identyfikacja code smells

Zaznacz cały `OwnerController.java` i w inline chat (Ctrl+I) wpisz:

```
Zidentyfikuj code smells w tym pliku. Format: linia | smell | severity. Top 5.
```

Zobacz, czy Copilot wskaże: God Class, Long Method, Feature Envy. Porównaj z własną oceną.

**Więcej teorii:** `01_podstawy_copilot_chat/README.md`
