# Ex 08: Twój pierwszy copilot-instructions.md

> Faza 3 · ~8 min · Źródło: moduł 03 + 06

**Po co:** Ten plik zmienia zachowanie Copilota dla CAŁEGO repozytorium. Jak firmowy styl promptowany raz, działa zawsze.

## Co zrobić

1. Utwórz plik `.github/copilot-instructions.md` w katalogu głównym spring-petclinic
2. Wklej do niego:

```markdown
# Reguły dla Copilot w tym projekcie

- Język kodu: Java 17+, używaj rekordów zamiast POJO gdzie to możliwe.
- Framework: Spring Boot 3.x, Spring Data JPA.
- Testy: JUnit 5 + Mockito. Nigdy JUnit 4.
- Nazewnictwo: camelCase, klasy z dużej litery, pakiety lowercase.
- Komentarze: Javadoc po polsku dla klas publicznych.
- Bezpieczeństwo: zawsze waliduj dane wejściowe. Nigdy nie loguj haseł.
```

3. Teraz przetestuj — w nowym chacie wpisz:

```
Wygeneruj nową encję Appointment z polami: date, description, pet. Dodaj repozytorium.
```

**Spodziewany wynik:** Copilot użyje Java 17+, Spring Data JPA, Javadoc po polsku — zgodnie z instrukcjami.

**Nie działa?** Zamknij i otwórz ponownie chat po zapisaniu pliku. Instructions ładują się przy starcie sesji.

**Więcej:** `03_konfiguracja_zespolowa/README.md` — sekcja Custom Instructions
