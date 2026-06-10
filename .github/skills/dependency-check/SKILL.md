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
