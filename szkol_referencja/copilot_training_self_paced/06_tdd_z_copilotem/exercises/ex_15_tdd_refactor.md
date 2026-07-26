# Ex 15: TDD Refactor — ulepszenie bez łamania testów

> Faza 4 · ~8 min · Moduł 06

**Po co:** Faza Refactor: Copilot poprawia strukturę kodu NIE zmieniając zachowania. Testy muszą dalej przechodzić.

## Co zrobić

1. W Copilot Chat wpisz:

```
Zrefaktoryzuj OwnerRepository i powiązane klasy: dodaj case-insensitive wyszukiwanie w findByCity (użyj @Query z LOWER). Nie zmieniaj sygnatury metody. Testy muszą dalej przechodzić.
```

2. Zaakceptuj zmiany.
3. Uruchom testy: `.\mvnw.cmd test -Dtest=OwnerRepositoryTest` (Windows) lub
	`./mvnw test -Dtest=OwnerRepositoryTest` (Linux/macOS)

**Spodziewany wynik:** Testy `@DataJpaTest` PRZECHODZĄ. Metoda używa
`@Query("... LOWER(o.city) = LOWER(:city)")`, a test z wartością o innej wielkości
liter potwierdza wykonanie zapytania na H2.

> Test z Mockito nie wystarcza w tym kroku: mock nie parsuje JPQL i przepuściłby
> błędne zapytanie. Dlatego cały cykl używa `@DataJpaTest`.

**Wniosek:** Cały cykl TDD: Red (ex 13) → Green (ex 14) → Refactor (ex 15). Copilot na każdym etapie robi co innego, bo ty mu to mówisz.

**Więcej:** `06_tdd_z_copilotem/EXERCISES.md`
