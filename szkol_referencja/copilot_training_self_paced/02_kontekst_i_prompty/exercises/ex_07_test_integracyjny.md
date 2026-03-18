# Ex 07: Test integracyjny z kontrolowanym kontekstem

> Faza 2 · ~10 min · Źródło: moduł 05

**Po co:** Generowanie testów to killer feature Copilota. Ale musisz wskazać co testować i jak.

## Co zrobić

1. Otwórz `OwnerController.java`
2. W Copilot Chat wpisz:

```
#file:OwnerController.java Wygeneruj test integracyjny dla metody processFindForm używając MockMvc. Test powinien sprawdzić 3 scenariusze: brak wyników, jeden wynik (redirect), wiele wyników (lista). Użyj JUnit 5 i @WebMvcTest.
```

3. Przejrzyj wygenerowany test.
4. Skopiuj do `src/test/java/` i uruchom: `.\mvnw.cmd test`

**Spodziewany wynik:** Klasa testowa z 3 metodami `@Test`, mockowanym `OwnerRepository`, i asercjami na status HTTP i model.

**Nie działa?** Jeśli import się nie zgadza, dodaj w promptcie: "Użyj importów z org.springframework.test.web.servlet."

**Więcej:** `02_kontekst_i_prompty/EXERCISES.md`
