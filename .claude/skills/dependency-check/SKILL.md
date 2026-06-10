---
name: dependency-check
description: Sprawdza zależności Maven pod kątem znanych podatności CVE i przestarzałych wersji. Uruchamiaj ręcznie — nie jest wywoływana automatycznie.
argument-hint: "Opcjonalnie: podaj nazwę zależności do sprawdzenia (np. spring-boot, thymeleaf)"
disable-model-invocation: true
allowed-tools: Read Bash
---

# Audyt zależności projektu

## Krok 1 — Lista wszystkich zależności

!`grep -E '<artifactId>|<version>' pom.xml`

## Krok 2 — Sprawdzenie znanych problemów

Na podstawie listy zależności przeanalizuj:

1. **Przestarzałe wersje** — porównaj z najnowszymi stabilnymi wersjami (wiedza modelu)
2. **Znane CVE** — sprawdź czy znasz podatności dla podanych wersji
3. **EOL biblioteki** — czy biblioteka jest nadal rozwijana?

## Krok 3 — Raport

```
## Wyniki audytu zależności

| Biblioteka | Aktualna wersja | Najnowsza | CVE | Akcja |
|---|---|---|---|---|
| ... | ... | ... | Brak/CVE-xxx | Aktualizuj/OK |

## Priorytety
1. 🔴 Krytyczne (CVE CVSS >= 9.0): ...
2. 🟡 Ważne (CVE CVSS 7-8.9): ...
3. 🟢 Niskie (stare wersje bez CVE): ...

## Rekomendacja
...
```

> Uwaga: To jest analiza oparta na wiedzy modelu. Dla produkcyjnego audytu użyj OWASP Dependency-Check lub Snyk.
