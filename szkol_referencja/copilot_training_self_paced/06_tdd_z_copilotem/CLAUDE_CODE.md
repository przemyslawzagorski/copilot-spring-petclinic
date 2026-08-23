# Moduł 06 — TDD: adaptacja dla Claude Code

> Oryginalne ćwiczenia (`exercises/`) są dla GitHub Copilot w VS Code.
> Ten plik zawiera ich odpowiedniki dla Claude Code.

Sam cykl Red → Green → Refactor jest identyczny — to metoda, nie funkcja
narzędzia. Różnice są dwie i obie wychodzą dopiero w praktyce: Claude Code
**sam uruchamia testy**, więc pętla domyka się bez Ciebie, i ma `/rewind`,
który zmienia koszt nieudanej próby.

---

## Kluczowe różnice

| GitHub Copilot | Claude Code |
|---|---|
| `#file:OwnerRepository.java` | Podaj ścieżkę w prompcie |
| Ty uruchamiasz `mvnw test` i wklejasz wynik | Claude uruchamia i czyta wynik sam |
| Nieudana próba = ręczne sprzątanie | `/rewind` cofa do stanu przed promptem |
| Subagent: brak odpowiednika | `.claude/agents/tdd-expert.md` prowadzi cały cykl |

---

## Ex 13 (CC): Red — test, który pada

**Odpowiednik ex_13_tdd_red.md**

```
Napisz test repozytorium JUnit 5 z @DataJpaTest dla nowej metody
findByCity(String city) w OwnerRepository. Metoda jeszcze NIE ISTNIEJE — test
ma failować na etapie kompilacji. Prawdziwe repozytorium i H2, bez Mockito.
Scenariusze: znalezione wyniki, pusta lista, null jako argument.

Zapisz do src/test/java/.../owner/OwnerRepositoryTest.java i uruchom testy.
NIE dodawaj implementacji metody.
```

**Różnica:** ostatnie zdanie jest tu ważniejsze niż w Copilocie. Claude Code ma
narzędzia do edycji **i** do uruchamiania testów, więc widząc czerwony build
chętnie „pomoże" i dopisze brakującą metodę. To zabiłoby fazę Red.

**Spodziewany wynik:** Claude uruchomi `./mvnw test -Dtest=OwnerRepositoryTest`,
zobaczy błąd kompilacji i **zatrzyma się**, raportując że to oczekiwane.

**Nie działa?** Jeśli mimo wszystko dopisał implementację — `/rewind`, wybierz
punkt sprzed promptu, **Restore code and conversation**, i spróbuj z mocniejszym
sformułowaniem: „Zatrzymaj się na czerwonym buildzie. Nie implementuj."

---

## Ex 14 (CC): Green — minimalna implementacja

**Odpowiednik ex_14_tdd_green.md**

```
Dodaj metodę findByCity(String city) do OwnerRepository. MINIMALNA
implementacja — tylko tyle, żeby testy przeszły. Spring Data JPA derived query.
Uruchom testy i pokaż wynik.
```

**Spodziewany wynik:** jedna linia w interfejsie repozytorium, testy zielone.

**Ćwiczenie z `/rewind`:** poproś celowo o za dużo —

```
Dodaj findByCity razem z obsługą stronicowania, sortowania i cache'owaniem.
```

— zobacz rozrost, potem `/rewind` → **Restore code and conversation** → wróć do
minimalnej wersji. Koszt nieudanej próby spada do zera, więc możesz sobie
pozwolić na eksperyment, którego w Copilocie byś nie zaczął.

> ⚠️ Jeśli Claude uruchomił coś w terminalu (np. `mvn clean`), tamte skutki
> **nie wrócą** przez `/rewind`. Szczegóły w ex_11b.

---

## Ex 15 (CC): Refactor — bez łamania testów

**Odpowiednik ex_15_tdd_refactor.md**

```
Zrefaktoryzuj findByCity na wyszukiwanie case-insensitive: @Query z LOWER.
Nie zmieniaj sygnatury metody. Dopisz test z inną wielkością liter.
Uruchom testy — muszą przechodzić.
```

Uwaga z oryginału obowiązuje: mock nie parsuje JPQL i przepuściłby błędne
zapytanie, dlatego cały cykl stoi na `@DataJpaTest`.

---

## Ex 15b (CC): Pętla samokorekty

**Odpowiednik ex_15b_self_correction_loop.md**

Tu różnica jest największa. W Copilocie pętla „uruchom → przeczytaj błąd →
popraw" wymaga Ciebie w każdym obrocie. Claude Code zamyka ją sam:

```
Uruchom testy. Jeśli któryś pada, przeanalizuj przyczynę, popraw i uruchom
ponownie. Powtarzaj aż wszystkie przejdą albo aż stwierdzisz, że problem
wymaga mojej decyzji. Po każdej iteracji napisz jednym zdaniem, co zmieniłeś.
```

**Spodziewany wynik:** Claude wykonuje kilka obrotów bez pytania i raportuje
przebieg. Ostatnie zdanie promptu jest istotne — bez niego pętla potrafi
kręcić się długo, próbując obejść problem, który wymaga decyzji projektowej.

**Obserwacja do zapisania:** ile obrotów zajęło? Gdzie pętla zaczęła kręcić się
w miejscu? To ten sam mechanizm, który moduł 11 opisuje jako pętlę agenta.

---

## Subagent `tdd-expert`

Repo zawiera gotowego subagenta prowadzącego cały cykl:

```
Użyj subagenta tdd-expert: przeprowadź mnie przez Red-Green-Refactor dla
metody findByCity w OwnerRepository.
```

Zobacz `.claude/agents/tdd-expert.md` — zwróć uwagę, jak zdefiniowano tam
granice („nie implementuj w fazie Red"). To ten sam problem, który wyżej
rozwiązywałeś zdaniem w prompcie, tylko zapisany raz na stałe.

---

## Żywe przykłady w tym repo

| Plik | Czego uczy |
|---|---|
| `.claude/agents/tdd-expert.md` | Subagent prowadzący Red-Green-Refactor |
| `.claude/skills/controller-testing/SKILL.md` | Skill generujący testy MockMvc |
| `CLAUDE.md` | Reguła „JUnit 5 + Mockito, nigdy JUnit 4" |
