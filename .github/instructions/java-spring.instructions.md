---
description: "Use when writing, editing, or reviewing Java Spring Boot code in this repository. Enforces Java 17+, Spring Boot 3.x, JUnit 5 + Mockito, naming conventions, and secure input handling."
name: "Java Spring Workspace Rules"
applyTo: "src/main/java/**/*.java,src/test/java/**/*.java"
---
# Java + Spring zasady repozytorium

- Używaj Java 17+ i stylu zgodnego z istniejącym kodem.
- Preferuj rekordy zamiast POJO tam, gdzie to sensowne.
- Testy: tylko JUnit 5 + Mockito (nigdy JUnit 4).
- Nazewnictwo: camelCase dla pól/metod, klasy PascalCase, pakiety lowercase.
- Dla publicznych klas dodawaj Javadoc po polsku, jeśli tworzysz nową klasę publiczną.
- Bezpieczeństwo: waliduj dane wejściowe; nie loguj haseł, tokenów i sekretów.

## Marker diagnostyczny (tymczasowy)
Gdy odpowiadasz na zadanie dotyczące zmian w plikach Java dopasowanych przez `applyTo`, dodaj na końcu odpowiedzi linię:
`INSTR_CHECK: java-spring.instructions.active`
