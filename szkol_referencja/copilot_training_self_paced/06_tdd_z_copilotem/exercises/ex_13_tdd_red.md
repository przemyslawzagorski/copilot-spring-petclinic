# Ex 13: TDD Red — napisz failujący test

> Faza 4 · ~10 min · Moduł 06

**Po co:** Test-Driven Development z Copilotem: najpierw test który PADA, potem implementacja. Copilot musi pisać test, NIE implementację.

## Co zrobić

1. W Copilot Chat wpisz:

```
Napisz test repozytorium JUnit 5 z `@DataJpaTest` dla nowej metody w OwnerRepository: findByCity(String city). Metoda jeszcze NIE ISTNIEJE — test ma FAILOWAĆ na etapie kompilacji. Użyj prawdziwego repozytorium i H2, bez Mockito. Przetestuj scenariusze: znalezione wyniki, pusta lista, null jako argument.
```

2. Skopiuj wygenerowany test do `src/test/java/.../owner/OwnerRepositoryTest.java`
3. Uruchom: `.\mvnw.cmd test -Dtest=OwnerRepositoryTest` (Windows) lub
	`./mvnw test -Dtest=OwnerRepositoryTest` (Linux/macOS)

**Spodziewany wynik:** Kompilacja testu PADA — `findByCity` nie istnieje. TO
DOBRZE. To jest „Red” w TDD.

**Nie działa?** Upewnij się, że Copilot NIE dodał implementacji metody i że test
używa wstrzykniętego `OwnerRepository`, a nie mocka. Jeśli dodał implementację,
powiedz: „Usuń implementację, zostaw tylko test.”

**Następny krok:** Ex 14 (Green)
