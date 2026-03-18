# Ćwiczenia: Moduł 04 (Agent Skills)

> Źródło: https://code.visualstudio.com/docs/copilot/customization/agent-skills

Format każdego ćwiczenia:
- Cel
- Prompt kursanta (bazowy)
- Oczekiwany rezultat
- Jak zweryfikować
- Typowe błędy i korekta
- Prompt trenerski (solution)

---

## Ćwiczenie 1: Twój pierwszy skill — raport wersji projektu

### Cel
Stworzyć folder `.github/skills/project-versions/` z plikiem `SKILL.md` i przetestować auto-load oraz wywołanie przez `/`.

### Krok po kroku

1. Utwórz folder i plik:

```
.github/skills/project-versions/SKILL.md
```

2. Zawartość `SKILL.md`:

```markdown
---
name: project-versions
description: "Raportuje wersje Java, Spring Boot i główne zależności z pom.xml. Użyj gdy ktoś pyta o wersje, stack technologiczny, zależności lub kompatybilność."
argument-hint: "[opcjonalnie: nazwa konkretnej zależności]"
---

# Raport wersji projektu

## Procedura

1. Otwórz `pom.xml` w katalogu głównym projektu.
2. Odczytaj:
   - Wersję Java z `<java.version>` w `<properties>`
   - Wersję Spring Boot z `<parent><version>`
   - Wszystkie zależności z `<dependencies>` — podaj groupId, artifactId i wersję
3. Sprawdź datę ostatniego commita: `git log -1 --format="%cd" --date=short`
4. Zwróć wynik w tabeli Markdown.

## Format wyjścia

| Komponent | Wersja |
|---|---|
| Java | (z pom.xml) |
| Spring Boot | (z parent) |
| (zależność 1) | (wersja) |
| ... | ... |
| Ostatni commit | (data) |

## Kiedy NIE używać
- Gdy pytanie dotyczy wersji runtime (zainstalowane JDK) — to inne pytanie.
- Gdy chcesz zmienić wersje — ten skill tylko raportuje.
```

### Prompt kursanta (bazowy)
```text
Jakie wersje Java i Spring Boot używa ten projekt?
```

### Oczekiwany rezultat
- Copilot auto-loaduje skill `project-versions` (bo description pasuje do pytania).
- Wynik: tabela Markdown z Java 17, Spring Boot 3.x i zależnościami.

### Jak zweryfikować
1. **Auto-load:** Zadaj pytanie naturalnym językiem (bez `/`). Copilot powinien sam znaleźć skill.
2. **Slash command:** Wpisz `/project-versions` w chat — skill musi pojawić się w liście.
3. **Porównaj wynik z `pom.xml`** — wersje muszą się zgadzać.

### Typowe błędy i korekta
| Błąd | Objaw | Korekta |
|---|---|---|
| Nazwa folderu ≠ `name` w frontmatter | Skill nie pojawia się w `/` | Zmień nazwę folderu LUB pole `name` — muszą być identyczne |
| Brak pola `description` | Copilot nie wie kiedy użyć skilla | Dodaj description z frazą "Użyj gdy..." |
| Plik nie w `.github/skills/` | Skill nie wykryty | Sprawdź ścieżkę: `.github/skills/project-versions/SKILL.md` |
| Zbyt ogólny description | Skill ładuje się na każde pytanie | Bądź konkretny: "wersje Java, Spring Boot, zależności z pom.xml" |

### Prompt trenerski (solution)
```text
Smoke test skilla project-versions:
1) Wpisz /project-versions — widać w liście? ✅/❌
2) Zapytaj "jakie wersje Java używa projekt?" — auto-load zadziałał? ✅/❌
3) Porównaj wynik z pom.xml — wersje się zgadzają? ✅/❌
Jeśli skill nie działa — diagnostyka: nazwa folderu vs name, ścieżka, description.
```

---

## Ćwiczenie 2: Skill z zasobami — testowanie kontrolerów

### Cel
Stworzyć skill który zawiera **towarzyszące zasoby** (szablon testu + przykład) — to główna przewaga skilla nad prompt file.

### Krok po kroku

1. Utwórz strukturę folderu:

```
.github/skills/controller-testing/
├── SKILL.md
├── test-template.java
└── examples/
    └── owner-controller-test.java
```

2. `SKILL.md`:

```markdown
---
name: controller-testing
description: "Generuje testy integracyjne MockMvc dla kontrolerów Spring MVC. Użyj gdy chcesz przetestować endpoint HTTP, formularz lub REST API w PetClinic."
argument-hint: "[nazwa kontrolera] [opcjonalnie: metoda]"
---

# Testowanie kontrolerów Spring MVC

## Kiedy użyć
- Testujesz endpoint HTTP (GET/POST/PUT/DELETE)
- Chcesz sprawdzić walidację formularzy
- Potrzebujesz test integracyjny z MockMvc

## Kiedy NIE użyć
- Test jednostkowy serwisu/repozytorium — to nie ten skill
- Test E2E z prawdziwą bazą — użyj @SpringBootTest zamiast @WebMvcTest

## Procedura
1. Zidentyfikuj kontroler i endpointy do przetestowania
2. Użyj szablonu z [test-template.java](./test-template.java)
3. Dla każdego endpointu utwórz testy:
   - Happy path (HTTP 200/302)
   - Walidacja (HTTP 400)
   - Not found (HTTP 404)
4. Uruchom: `./mvnw test -Dtest=NazwaTestu`

## Konwencje projektu
- Klasa: `{Controller}MockMvcTest`
- Metoda: `test{Endpoint}_{scenariusz}`
- Adnotacje: `@WebMvcTest` + `@MockBean`
- Asercje: AssertJ + MockMvc matchers

## Przykład
Zobacz [owner-controller-test.java](./examples/owner-controller-test.java)
```

3. `test-template.java`:

```java
package org.springframework.samples.petclinic.PAKIET;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.bean.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

@WebMvcTest(KONTROLER.class)
class KONTROLERMockMvcTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SERWIS serwis;

    @Test
    void testEndpoint_happyPath() throws Exception {
        mockMvc.perform(get("/SCIEZKA"))
            .andExpect(status().isOk())
            .andExpect(view().name("WIDOK"));
    }
}
```

4. `examples/owner-controller-test.java`:

```java
package org.springframework.samples.petclinic.owner;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.bean.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(OwnerController.class)
class OwnerControllerMockMvcTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private OwnerRepository owners;

    @Test
    void testShowOwnerList_happyPath() throws Exception {
        mockMvc.perform(get("/owners"))
            .andExpect(status().isOk())
            .andExpect(view().name("owners/ownersList"));
    }

    @Test
    void testNewOwnerForm_returnsForm() throws Exception {
        mockMvc.perform(get("/owners/new"))
            .andExpect(status().isOk())
            .andExpect(view().name("owners/createOrUpdateOwnerForm"));
    }
}
```

### Prompt kursanta (bazowy)
```text
/controller-testing VetController
```

lub naturalnie:
```text
Pomóż mi napisać testy MockMvc dla VetController.
```

### Oczekiwany rezultat
- Copilot wczytuje SKILL.md, sięga po szablon i przykład.
- Generuje testy MockMvc dla VetController z poprawnymi adnotacjami.
- Używa konwencji z SKILL.md (nazewnictwo klasy, metod).

### Jak zweryfikować
1. Wygenerowana klasa kompiluje się: `./mvnw compile -pl . -Dtest=VetControllerMockMvcTest`
2. Używa `@WebMvcTest` (nie `@SpringBootTest`)
3. Zawiera minimum 2 metody testowe (happy path + edge case)
4. Copilot odwołuje się do szablonu lub przykładu z folderu skilla

### Typowe błędy i korekta
| Błąd | Korekta |
|---|---|
| Copilot ignoruje szablon i pisze od zera | Dodaj w SKILL.md: "ZAWSZE użyj szablonu z [test-template.java](./test-template.java)" |
| Test używa @SpringBootTest | Skill mówi @WebMvcTest — wzmocnij instrukcję w body |
| Brak MockBean | Dodaj do procedury: "Krok 0: zidentyfikuj zależności kontrolera → MockBean" |

### Prompt trenerski (solution)
```text
Używając /controller-testing wygeneruj testy dla VetController.
Sprawdź: czy Copilot użył szablonu? Czy konwencje nazewnicze się zgadzają?
Porównaj z examples/owner-controller-test.java.
```

---

## Ćwiczenie 3: Widoczność — user-invocable i disable-model-invocation

### Cel
Zrozumieć i przetestować 4 kombinacje widoczności skilla.

### Krok po kroku

1. Utwórz skill „wiedzy tła" (background knowledge):

```
.github/skills/java-conventions/SKILL.md
```

```markdown
---
name: java-conventions
description: "Konwencje Java używane w tym projekcie: nazewnictwo, formatowanie, wzorce. Użyj gdy piszesz lub reviewujesz kod Java."
user-invocable: false
---

# Konwencje Java w PetClinic

- Pakiety: lowercase, bez underscore
- Klasy: PascalCase
- Metody/pola: camelCase
- Testy: `{Klasa}Test` lub `{Klasa}IntegrationTest`
- Spring: constructor injection (nie @Autowired na polach)
- Walidacja: @Valid na kontrolerze, nie w serwisie
- Records zamiast POJO tam gdzie brak mutacji
```

2. Utwórz skill „na żądanie":

```
.github/skills/dependency-check/SKILL.md
```

```markdown
---
name: dependency-check
description: "Sprawdza zależności Maven pod kątem znanych CVE i przestarzałych wersji."
disable-model-invocation: true
argument-hint: "[opcjonalnie: groupId:artifactId do sprawdzenia]"
---

# Sprawdzanie zależności

## Procedura
1. Przeczytaj pom.xml
2. Dla każdej zależności sprawdź stabilność wersji
3. Zwróć tabelę: zależność | wersja | najnowsza | status (OK/OUTDATED/CVE)

## Kiedy uruchomić
- Przed release
- Po dodaniu nowej zależności
- Periodic review (co miesiąc)
```

### Prompt kursanta (bazowy)
```text
Test 1 — auto-load background skill:
Zapytaj Copilota: "Napisz nową klasę serwisu w tym projekcie"
Czy Copilot sam zastosował konwencje z java-conventions? (np. constructor injection)

Test 2 — menu /:
Wpisz / w chat. Czy widzisz java-conventions w liście? (NIE powinno być)
Czy widzisz dependency-check? (TAK powinno być)

Test 3 — auto-load disabled:
Zapytaj: "Czy moje zależności Maven są aktualne?"
Czy Copilot załadował dependency-check? (NIE powinien — disable-model-invocation: true)

Test 4 — jawne wywołanie:
Wpisz: /dependency-check
Czy teraz działa? (TAK)
```

### Oczekiwany rezultat

| Test | Skill | user-invocable | disable-model-invocation | Widoczny w `/`? | Auto-load? |
|---|---|---|---|---|---|
| 1 | java-conventions | `false` | `false` (domyślne) | Nie | **Tak** |
| 2 | dependency-check | `true` (domyślne) | `true` | **Tak** | Nie |
| 3 | dependency-check | — | `true` | — | **Nie** |
| 4 | dependency-check | — | — | — | — (jawne `/`) |

### Jak zweryfikować
- Test 1: Sprawdź czy wygenerowany kod używa constructor injection (nie @Autowired na polach) — to dowód auto-load.
- Test 2: Zrzut ekranu menu `/` — java-conventions nie powinno być widoczne.
- Test 3 vs 4: Ten sam skill, różne zachowanie zależnie od sposobu wywołania.

### Typowe błędy i korekta
| Błąd | Korekta |
|---|---|
| java-conventions widoczny w `/` menu | Sprawdź: `user-invocable: false` musi być w frontmatter |
| dependency-check auto-loaduje | Sprawdź: `disable-model-invocation: true` — pisownia! |
| Żaden skill nie działa | Sprawdź nazwy folderów vs `name` — muszą być identyczne |

### Prompt trenerski (solution)
```text
Przetestuj macierz widoczności:
1) Skill z user-invocable: false → nie widać w /, ale auto-load działa
2) Skill z disable-model-invocation: true → widać w /, ale auto-load nie działa
3) Wyciągnij wnioski: kiedy który wariant ma sens w praktyce?
```

---

## Ćwiczenie 4: Generowanie skilla przez AI — /create-skill

### Cel
Użyć wbudowanej komendy `/create-skill` do wygenerowania kompletnego skilla bez ręcznego pisania.

### Prompt kursanta (bazowy)
```text
/create-skill Skill do code review kontrolerów Spring MVC.
Powinien sprawdzać: walidację danych wejściowych, obsługę błędów,
separation of concerns, nazewnictwo metod.
Output w tabeli: plik | problem | severity | sugestia naprawy.
```

### Oczekiwany rezultat
- Copilot zadaje doprecyzowujące pytania (np. „Czy tylko kontrolery, czy też REST controllery?").
- Generuje folder `.github/skills/controller-review/` z `SKILL.md`.
- SKILL.md zawiera prawidłowy YAML frontmatter + procedurę review.

### Jak zweryfikować
1. Sprawdź wygenerowany plik — ma `name` i `description` w frontmatter?
2. `name` = nazwa folderu?
3. Wpisz `/controller-review` — pojawia się w liście?
4. Uruchom: `/controller-review` na OwnerController.java — dostarcza tabelę?

### Alternatywny scenariusz: skill z rozmowy
```text
(Po wielokrokowej sesji debugowania)
Stwórz skill z tego co właśnie debugowaliśmy — procedura diagnostyki
problemów z połączeniem do bazy danych w Spring Boot.
```

### Typowe błędy i korekta
| Błąd | Korekta |
|---|---|
| /create-skill nie rozpoznane | Upewnij się, że masz najnowszą wersję Copilot Chat |
| Wygenerowany skill za ogólny | Doprecyzuj w follow-up: "Skup się TYLKO na @Controller, nie @RestController" |
| Brak sekcji „kiedy NIE użyć" | Dodaj ręcznie — to best practice |

### Prompt trenerski (solution)
```text
Użyj /create-skill do wygenerowania skilla dla dowolnego scenariusza z Twojej pracy.
Ocena: czy wygenerowany SKILL.md spełnia kryteria jakości (name=folder, description, procedura, format wyjścia)?
```

---

## Ćwiczenie 5: Skill vs Prompt — porównanie na tym samym zadaniu

### Cel
Zobaczyć **różnicę w działaniu** między prompt file a skill na identycznym zadaniu. Zrozumieć kiedy co wybrać.

### Krok po kroku

1. Masz już skill `controller-testing` (ćw. 2).

2. Utwórz prompt file do tego samego zadania:

`.github/prompts/generate-controller-test.prompt.md`:

```markdown
---
description: "Wygeneruj test MockMvc dla kontrolera Spring"
---
Wygeneruj test integracyjny MockMvc dla wskazanego kontrolera.
Użyj @WebMvcTest, @MockBean, JUnit 5.
Klasa testowa: {Kontroler}MockMvcTest.
Przetestuj happy path i walidację.
```

3. Porównaj wyniki:

### Prompt kursanta (bazowy)
```text
Zrób 2 testy — raz z promptem, raz ze skillem:

A) Wywołaj: /generate-controller-test dla PetController
B) Wywołaj: /controller-testing PetController

Porównaj wyniki i odpowiedz:
- Który dał lepszy wynik?
- Który użył szablonu/przykładu?
- Który jest bardziej konsystentny przy wielokrotnym użyciu?
```

### Oczekiwany rezultat

| Aspekt | Prompt File | Skill |
|---|---|---|
| Ma szablon testu | ❌ | ✅ (test-template.java) |
| Ma przykład | ❌ | ✅ (examples/) |
| Konsystentny output | Zależny od modelu | Bardziej — ma procedurę i format |
| Portable (inne AI) | ❌ Tylko VS Code | ✅ agentskills.io |
| Prosty w tworzeniu | ✅ 1 plik | ❌ Folder + pliki |
| Auto-load | ❌ Tylko jawnie | ✅ Jeśli enabled |

### Kiedy co wybrać — reguła kciuka

```
Szybki szablon bez dodatkowych plików → Prompt File
Procedura wielokrokowa z zasobami     → Skill
Coś co miałoby działać poza VS Code  → Skill (agentskills.io)
```

### Prompt trenerski (solution)
```text
Porównaj wynik prompt file vs skill na PetController.
Który wygenerował test bliższy standardom projektu? Dlaczego?
Odpowiedz w tabeli porównawczej.
```

---

## Podsumowanie modułu — Mini-quiz

Po wykonaniu ćwiczeń kursant powinien odpowiedzieć na te pytania:

1. **Gdzie żyje skill?** → `.github/skills/<nazwa>/SKILL.md`
2. **Co MUSI się zgadzać?** → Nazwa folderu = pole `name` w frontmatter
3. **Czym skill różni się od prompt file?** → Może zawierać zasoby (skrypty, szablony), jest portable, ma auto-load
4. **Czym skill różni się od hooka?** → Hook wymusza (execute code), skill instruuje (guide AI)
5. **Czym skill różni się od agenta?** → Agent to persona z ograniczeniami i tools. Skill to wiedza/procedura.
6. **Kiedy `user-invocable: false`?** → Background knowledge — auto-load, ale nie w menu `/`
7. **Kiedy `disable-model-invocation: true`?** → Tylko na żądanie — heavy/risky operacje
8. **Jak szybko wygenerować skill?** → `/create-skill` + opis
