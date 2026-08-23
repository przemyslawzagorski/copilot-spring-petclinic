# Reguły dla Copilot w tym projekcie

- Język kodu: Java 17+, używaj rekordów zamiast POJO gdzie to możliwe.
- Framework: Spring Boot 4.0.3, Spring Data JPA.
- Testy: JUnit 5 + Mockito. Nigdy JUnit 4.
- Nazewnictwo: camelCase, klasy z dużej litery, pakiety lowercase.
- Komentarze: Javadoc po polsku dla klas publicznych.
- Bezpieczeństwo: zawsze waliduj dane wejściowe. Nigdy nie loguj haseł.
- Złożone zadania realizuj w kolejności: analiza i doprecyzowanie wymagań -> specyfikacja -> plan -> implementacja.
- Jeśli zadanie dotyczy kilku plików, większej zmiany architektury albo niejasnego zakresu, najpierw przygotuj spec i plan, a dopiero potem pisz kod.
- Trzymaj specyfikację opisową i bez implementacji; szczegóły wykonawcze przenieś do planu.
- Inspiruj się workflow w stylu Shotgun: najpierw uporządkowanie problemu, potem rozbicie na etapy, na końcu realizacja.
