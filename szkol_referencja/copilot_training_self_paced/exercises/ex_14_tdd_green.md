# Ex 14: TDD Green — minimalna implementacja

> Faza 4 · ~8 min · Źródło: moduł 08

**Po co:** Faza Green: Copilot pisze MINIMALNY kod, żeby test przeszedł. Nic więcej.

## Co zrobić

1. Otwórz `OwnerRepository.java`
2. W Copilot Chat wpisz:

```
#file:OwnerRepository.java Dodaj metodę findByCity(String city) do tego repozytorium. Napisz MINIMALNĄ implementację — tylko tyle, żeby testy przeszły. Spring Data JPA derived query.
```

3. Zaakceptuj zmianę.
4. Uruchom test ponownie: `.\mvnw.cmd test -pl . -Dtest=OwnerRepositoryTest`

**Spodziewany wynik:** Testy PRZECHODZĄ. Metoda `findByCity` to jedna linia: sygnatura metody w interfejsie repozytorium.

**Nie działa?** Jeśli Copilot dodał za dużo, powiedz: "Za dużo kodu. Zostaw TYLKO sygnaturę metody w interfejsie."

**Następny krok:** Ex 15 (Refactor)
