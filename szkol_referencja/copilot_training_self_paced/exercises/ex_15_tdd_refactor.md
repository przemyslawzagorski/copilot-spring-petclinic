# Ex 15: TDD Refactor — ulepszenie bez łamania testów

> Faza 4 · ~8 min · Źródło: moduł 08

**Po co:** Faza Refactor: Copilot poprawia strukturę kodu NIE zmieniając zachowania. Testy muszą dalej przechodzić.

## Co zrobić

1. W Copilot Chat wpisz:

```
Zrefaktoryzuj OwnerRepository i powiązane klasy: dodaj case-insensitive wyszukiwanie w findByCity (użyj @Query z LOWER). Nie zmieniaj sygnatury metody. Testy muszą dalej przechodzić.
```

2. Zaakceptuj zmiany.
3. Uruchom testy: `.\mvnw.cmd test -pl . -Dtest=OwnerRepositoryTest`

**Spodziewany wynik:** Testy PRZECHODZĄ. Metoda teraz używa `@Query("... LOWER(o.city) = LOWER(:city)")`.

**Wniosek:** Cały cykl TDD: Red (ex 13) → Green (ex 14) → Refactor (ex 15). Copilot na każdym etapie robi co innego, bo ty mu to mówisz.

**Więcej:** `08_module_08/EXERCISES.md`
