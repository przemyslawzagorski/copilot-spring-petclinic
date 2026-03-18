# Ex 13: TDD Red — napisz failujący test

> Faza 4 · ~10 min · Źródło: moduł 08

**Po co:** Test-Driven Development z Copilotem: najpierw test który PADA, potem implementacja. Copilot musi pisać test, NIE implementację.

## Co zrobić

1. W Copilot Chat wpisz:

```
Napisz test jednostkowy (JUnit 5 + Mockito) dla nowej metody w OwnerRepository: findByCity(String city). Metoda jeszcze NIE ISTNIEJE — test ma FAILOWAĆ. Przetestuj scenariusze: znalezione wyniki, pusta lista, null jako argument.
```

2. Skopiuj wygenerowany test do `src/test/java/.../owner/OwnerRepositoryTest.java`
3. Uruchom: `.\mvnw.cmd test -pl . -Dtest=OwnerRepositoryTest`

**Spodziewany wynik:** Test PADA — `findByCity` nie istnieje. TO DOBRZE. To jest "Red" w TDD.

**Nie działa?** Upewnij się, że Copilot NIE dodał implementacji metody. Jeśli dodał, powiedz: "Usuń implementację, zostaw tylko test."

**Następny krok:** Ex 14 (Green)
