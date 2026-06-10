# Ex 31: Copilot Coding Agent — autonomiczny agent na issue

> Bonus · ~20 min · Wymaga: GitHub repo z dostępem do Copilot Coding Agent (Enterprise/Team plan)

**Po co:** Copilot Coding Agent to nowy tryb (2025) gdzie Copilot **samodzielnie pracuje nad issue** w tle — bez Twojego nadzoru każdego kroku. Tworzysz issue, przypisujesz do Copilot, przychodzisz na gotowy PR.

---

## Teoria: Copilot Agent vs Copilot Chat

| | Copilot Chat | Copilot Coding Agent |
|---|---|---|
| Tryb | Interaktywny (ty prowadzisz) | Autonomiczny (Copilot pracuje sam) |
| Zakres | Jeden krok na raz | Pełne zadanie (plan → kod → testy → PR) |
| Gdy używać | Eksploracja, szybkie zmiany | Dobrze zdefiniowane zadania, praca w tle |
| Output | Odpowiedź w chacie | Pull Request z opisem |
| Review | Ty widzisz każdy krok | Ty reviewujesz PR jak od kolegi |

---

## Krok 1: Przygotuj issue

W repozytorium GitHub stwórz issue z jasno zdefiniowanym zadaniem:

```markdown
**Tytuł:** Add email field to Owner entity with validation

**Opis:**
Add an `email` field to the `Owner` class with the following requirements:

1. Field: `private String email` in `Owner.java`
2. Validation: `@Email` annotation (jakarta.validation)
3. Not null, not blank
4. Update `OwnerController.java` to include email in create/edit forms
5. Update Thymeleaf templates: `createOrUpdateOwnerForm.html`
6. Add integration test in `OwnerControllerTests.java`

**Acceptance criteria:**
- [ ] `./mvnw test` passes without errors
- [ ] Email field visible in owner form
- [ ] Invalid email rejected with validation message
```

**Zasada dobrych issue dla Coding Agent:** im bardziej precyzyjne kryteria sukcesu, tym lepszy PR.

---

## Krok 2: Przypisz do Copilot

1. W issue kliknij **Assignee** → **Copilot** (musi być widoczny na liście)
2. Lub wpisz w komentarzu: `@copilot please implement this`
3. Copilot zaczyna pracę — widać status w issue lub w zakładce **Copilot Sessions**

**Copilot robi:**
- Analizuje repozytorium (kod, testy, styl)
- Tworzy plan
- Implementuje zmiany krok po kroku
- Uruchamia testy (jeśli skonfigurowane)
- Otwiera Pull Request

---

## Krok 3: Review PR

Po kilku minutach Copilot otworzy PR. Przejrzyj:

**Co ocenić:**
- Czy zmiany są w scope issue?
- Czy testy są sensowne i przechodzą?
- Czy Copilot dodał coś niepotrzebnego?
- Czy kod jest spójny ze stylem projektu?

**Daj feedback przez komentarz w PR:**
```
The email validation works but the error message is in English.
Please use Polish: "Nieprawidłowy adres email"
```

Copilot wróci do pracy i zaktualizuje PR!

---

## Krok 4: Ocena jakości

Po przyjęciu/odrzuceniu PR odpowiedz sobie:

1. Ile % kodu Copilot napisał sam (bez Twojej poprawki)?
2. Czy testy faktycznie testują wymagania z issue?
3. Jak precyzyjne było Twoje issue? Co byś zmienił?

**Zasada:** Jakość outputu Coding Agent to w dużej mierze jakość Twojego issue. AI są dobre w "co robić", ale muszą wiedzieć "co oznacza sukces".

---

## Kiedy używać Coding Agent vs Chat

| Użyj Coding Agent gdy | Użyj Copilot Chat gdy |
|---|---|
| Zadanie jest dobrze zdefiniowane | Eksploracja, "nie wiem od czego zacząć" |
| Masz inne rzeczy do roboty | Chcesz rozumieć każdy krok |
| Feature z jasnymi kryteriami | Debugging (kontekst zmienia się dynamicznie) |
| Dodajesz testy do istniejącego kodu | Refaktoryzacja z wieloma decyzjami |
| Issue z checklist'ą akceptacji | Pytania architektoniczne |

---

## Checklist walidacji

- [ ] Issue zawiera precyzyjne acceptance criteria
- [ ] Copilot otworzył PR w rozsądnym czasie (~5-15 min)
- [ ] PR zawiera testy (nie tylko implementację)
- [ ] Dałeś feedback przez komentarz i Copilot go uwzględnił
- [ ] `./mvnw test` przechodzi w PR
