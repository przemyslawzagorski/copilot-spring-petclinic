# Dry-run: Moduł 05 (Skills)

> Branch: `test/dry-run-module-05` · Data: 2026-05-04

## Wyniki

| # | Ćwiczenie | Status | Uwagi |
|---|-----------|--------|-------|
| ex_12 | project-versions SKILL.md | PASS | Plik istnieje, `name`=`folder`=`project-versions`, frontmatter poprawny |
| ex_12 cz.2 | controller-testing SKILL.md + zasoby | PASS | 4 pliki: SKILL.md, test-template.java, examples/get-endpoint.java, examples/post-with-validation.java — wszystkie istnieją |
| ex_12 cz.3 | java-conventions (user-invocable: false) | PASS | Plik istnieje, `user-invocable: false` w frontmatter |
| ex_12 cz.3 | dependency-check (disable-model-invocation: true) | PASS | Plik istnieje, `disable-model-invocation: true` w frontmatter |
| ex_12b | Skill vs Prompt vs Hook — tabela decyzyjna | SKIP | Ćwiczenie subiektywne — wymaga oceny odpowiedzi tekstowej kursanta |
| ex_12 cz.4 | `/create-skill` — generowanie skilla przez AI | SKIP | Wymaga interakcji z VS Code UI / Copilot Chat |
| ex_12 cz.5 | Skill vs Prompt — porównanie na tym samym zadaniu | SKIP | Subiektywne, wymaga ręcznej oceny wyników Copilota |

### Walidacja struktury

```
controller-testing | user-invocable=true(default) | disable-model-invocation=false(default)  ✅
dependency-check   | user-invocable=true(default) | disable-model-invocation=true             ✅
java-conventions   | user-invocable=false          | disable-model-invocation=false(default)   ✅
project-versions   | user-invocable=true(default)  | disable-model-invocation=false(default)   ✅
```

Wszystkie: `name` == `nazwa folderu` ✅

### Podsumowanie
- PASS: 4
- FAIL: 0
- SKIP: 3
- Czas: ~5 min
