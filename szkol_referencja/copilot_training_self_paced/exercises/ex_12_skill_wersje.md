# Ex 12: Skill — wersje i zależności projektu

> Faza 4 · ~5 min · Źródło: moduł 04

**Po co:** Skill to prompt file który robi jedno konkretne zadanie powtarzalnie. Zaczniemy od prostego: raport wersji.

## Co zrobić

1. Otwórz `.copilot/prompts/prompt_date_java_version.md` z modułu 04 (lub utwórz):

```markdown
---
description: "Raport: wersje Java, Spring Boot, zależności"
---
Sprawdź pom.xml tego projektu i podaj:
- Wersję Java
- Wersję Spring Boot (parent)
- Top 5 najważniejszych zależności z numerami wersji
- Datę ostatniego build (git log -1 lub build-info jeśli dostępne)
Format: tabela Markdown.
```

2. Wywołaj ten prompt w Copilot Chat.

**Spodziewany wynik:** Tabela z Java 17, Spring Boot 3.x i głównymi zależnościami.

**Więcej:** `04_module_04/EXERCISES.md` — ćwiczenie 1
