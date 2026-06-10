---
name: project-versions
description: Sprawdza i raportuje wersje technologii w projekcie Spring PetClinic — Java, Spring Boot, Maven/Gradle, zależności. Używaj przy pytaniach o wersje, upgrade'ach i audytach bezpieczeństwa.
argument-hint: "Podaj co sprawdzić: java, spring, all, dependencies"
allowed-tools: Read Bash
---

# Procedura sprawdzania wersji projektu

## Krok 1 — Java

Sprawdź wersję Java w `pom.xml`:

!`grep -A2 '<java.version>' pom.xml 2>/dev/null || grep 'sourceCompatibility' build.gradle 2>/dev/null`

## Krok 2 — Spring Boot

Sprawdź parent POM:

!`grep -A3 '<parent>' pom.xml | grep '<version>' 2>/dev/null`

## Krok 3 — Główne zależności

!`grep -E '<artifactId>|<version>' pom.xml | head -60`

## Krok 4 — Raport

Na podstawie powyższych danych wygeneruj tabelę:

| Technologia | Wersja w projekcie | Najnowsza stabilna | Status |
|---|---|---|---|
| Java | ? | 21 LTS (najnowszą sprawdź na adoptium.net) | ✅/⚠️ |
| Spring Boot | ? | najnowszą sprawdź na spring.io/projects/spring-boot | ✅/⚠️ |
| ... | ... | ... | ... |

Oznacz statusy: ✅ aktualne, ⚠️ dostępna nowsza wersja, ❌ EOL/podatność.
Sprawdź aktualne wersje na podstawie swojej wiedzy (data cutoff: sierpień 2025).
