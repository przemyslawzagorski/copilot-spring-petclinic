---
name: project-versions
description: >
  Sprawdza i raportuje wersje technologii w projekcie Spring PetClinic:
  Java, Spring Boot, Maven/Gradle, zależności. Pomaga przy upgrade'ach
  i audytach bezpieczeństwa.
argument-hint: "Podaj co sprawdzić: java, spring, all, dependencies"
---

# Procedura sprawdzania wersji projektu

## Krok 1 — Java
Sprawdź wersję Java w `pom.xml` lub `build.gradle`:
- Szukaj `<java.version>` lub `sourceCompatibility`
- Zweryfikuj zgodność z `JAVA_HOME`

## Krok 2 — Spring Boot
Sprawdź parent POM:
- `<parent>` → `spring-boot-starter-parent` → `<version>`
- Porównaj z najnowszą wersją na https://spring.io/projects/spring-boot

## Krok 3 — Zależności
Dla każdej zależności w `<dependencies>`:
- Wypisz groupId:artifactId:version
- Oznacz te, które mają jawną wersję (nie dziedziczoną z BOM)

## Krok 4 — Raport
Wygeneruj tabelę:

| Technologia | Wersja w projekcie | Najnowsza stabilna | Status |
|---|---|---|---|
| Java | ? | 21 | ✅/⚠️ |
| Spring Boot | ? | 3.4.x | ✅/⚠️ |
| ... | ... | ... | ... |
