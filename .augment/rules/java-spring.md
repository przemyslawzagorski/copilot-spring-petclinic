---
type: agent_requested
description: Zasady tworzenia i testowania kodu Java Spring Boot w katalogach src/main/java i src/test/java
---

# Java i Spring Boot

- Używaj Java 17+ oraz Spring Boot 4.0.3.
- Zachowuj istniejący styl i granice pakietów.
- Stosuj rekordy zamiast klas DTO, gdy model danych jest niemutowalny.
- Testy pisz w JUnit 5 z Mockito; nie używaj JUnit 4 ani `@MockBean`.
- Dla kontrolerów używaj `@WebMvcTest` i `@MockitoBean`.
- Waliduj dane wejściowe na granicach systemu i nigdy nie loguj sekretów.
- Przed przekazaniem zmiany uruchom najwęższy adekwatny test.