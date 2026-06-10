---
name: build-red-i18n-test
description: Test suite is RED on main — I18nPropertiesSyncTest fails on hardcoded strings in ai/assistant.html
metadata:
  type: project
---

Na 2026-06-07 pełny `./mvnw test` jest CZERWONY na `main`: 69 testów, 1 failure (0 errors, 2 skipped). Failuje `org.springframework.samples.petclinic.system.I18nPropertiesSyncTest` — wykrywa zahardkodowane (nieumiędzynarodowione) stringi w `src/main/resources/templates/ai/assistant.html` (i jedną w `templates/fragments/layout.html` "AI Asystent"). Plik assistant.html pochodzi z live demo AI (commit 0fb6152), reszta UI używa `#{...}` z `messages/messages*.properties`.

**Why:** Ćwiczenia szkoleniowe (moduł 06 TDD, ex_07) każą uruchamiać `mvnw test` — trainee zobaczy ten niezwiązany failure i może się pogubić.
**How to apply:** Albo umiędzynarodowić teksty w assistant.html (dodać klucze do messages.properties), albo wyłączyć/oznaczyć ten plik w I18nPropertiesSyncTest. Środowisko sandbox nie pobiera Mavena 3.9.12 przez `mvnw` (bash/wget) — buduj przez `.\mvnw.cmd` w PowerShell.
