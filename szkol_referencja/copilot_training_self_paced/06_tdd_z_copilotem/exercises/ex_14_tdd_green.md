# Ex 14: TDD Green — minimalna implementacja

> Faza 4 · ~8 min · Moduł 06

**Po co:** Faza Green: Copilot pisze MINIMALNY kod, żeby test przeszedł. Nic więcej.

## Co zrobić

1. Otwórz `OwnerRepository.java`
2. W Copilot Chat wpisz:

```
#file:OwnerRepository.java Dodaj metodę findByCity(String city) do tego repozytorium. Napisz MINIMALNĄ implementację — tylko tyle, żeby testy przeszły. Spring Data JPA derived query.
```

3. Zaakceptuj zmianę.
4. Uruchom test ponownie: `.\mvnw.cmd test -Dtest=OwnerRepositoryTest` (Windows)
	lub `./mvnw test -Dtest=OwnerRepositoryTest` (Linux/macOS)

**Spodziewany wynik:** Testy `@DataJpaTest` PRZECHODZĄ i wykonują derived query na
H2. Metoda `findByCity` to jedna linia: sygnatura metody w interfejsie repozytorium.

**Nie działa?** Jeśli Copilot dodał za dużo, powiedz: "Za dużo kodu. Zostaw TYLKO sygnaturę metody w interfejsie."

**Zweryfikowane na tym repo:** minimalna wersja to dosłownie
`List<Owner> findByCity(String city);` plus `import java.util.List;`. Trzy testy
z ex_13 przechodzą — łącznie z tym dla `null`, bo derived query z `null`
zwraca pustą listę bez rzucania wyjątku.

**Następny krok:** Ex 15 (Refactor)
