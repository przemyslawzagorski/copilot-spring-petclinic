# Ex 09: Instrukcje per ścieżka (applyTo)

> Faza 3 · ~8 min · Źródło: moduł 06

**Po co:** Różne pliki potrzebują różnych reguł. Testy inne niż kontrolery. To się robi przez `applyTo`.

## Co zrobić

1. Utwórz plik `java.instructions.md` w katalogu głównym spring-petclinic:

```markdown
---
applyTo: "**/*.java"
---
- Formatuj kod zgodnie z Google Java Style Guide.
- Używaj `Optional` zamiast `null` w typach zwracanych.
- Każda metoda publiczna musi mieć Javadoc.
```

2. Utwórz plik `test.instructions.md`:

```markdown
---
applyTo: "**/test/**/*.java"
---
- Używaj JUnit 5 (@Test, @BeforeEach, @DisplayName).
- Nazwy testów: should_OczekiwanyWynik_when_Warunek.
- Każdy test ma sekcje: // given, // when, // then.
- Mockuj zależności przez @MockitoBean (Spring Boot 4.x; pakiet `org.springframework.test.context.bean.override.mockito`).
```

3. Przetestuj — otwórz plik testowy i w inline chat (Ctrl+I) wpisz:

```
Wygeneruj test dla metody findByLastName w OwnerRepository.
```

**Spodziewany wynik:** Test z `@DisplayName`, `should_...when_...`, sekcjami given/when/then.

**Więcej:** `03_konfiguracja_zespolowa/EXERCISES.md`
