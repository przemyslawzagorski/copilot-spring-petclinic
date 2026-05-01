# START HERE — Ścieżka krok po kroku

## Szybki start

1. Otwórz folder `copilot-spring-petclinic` w VS Code.
2. W Copilot Chat wybierz agenta **mentor** i wpisz: `ćwiczenie 1`.
3. Rób ćwiczenia po kolei — każde ćwiczenie jest w folderze swojego modułu.

---

## 10 modułów

Każdy moduł ma README (teoria), EXERCISES.md (index ćwiczeń) i folder `exercises/` z plikami ćwiczeń.

| # | Moduł | Ćwiczenia | Czas |
|---|-------|-----------|------|
| 01 | [Podstawy Copilot Chat](01_podstawy_copilot_chat/) | ex_01 – ex_04 | ~45 min |
| 02 | [Kontekst i Prompty](02_kontekst_i_prompty/) | ex_05 – ex_07 | ~65 min |
| 03 | [Konfiguracja zespołowa](03_konfiguracja_zespolowa/) | ex_08 – ex_10b | ~50 min |
| 04 | [Hooks i Guardrails](04_hooks_i_guardrails/) | ex_11, ex_18, ex_21d | ~40 min |
| 05 | [Skills](05_skills/) | ex_12, ex_12b | ~35 min |
| 06 | [TDD z Copilotem](06_tdd_z_copilotem/) | ex_13 – ex_15b | ~40 min |
| 07 | [Bezpieczeństwo](07_bezpieczenstwo/) | ex_16 – ex_21b | ~50 min |
| 08 | [Custom Agenty](08_custom_agenty/) | ex_18b – ex_21c | ~95 min |
| 09 | [MCP Server](09_mcp_server/) | ex_22 – ex_24b | ~80 min |
| 10 | [Copilot Python SDK](10_copilot_python_sdk/) | ex_25 – ex_29 | ~95 min |

**Łącznie:** 46 ćwiczeń (~595 min, w tym bonusy).

---

## Ćwiczenia bonusowe (🅱️)

Ćwiczenia z literką „b", „c" lub „d" w nazwie są bonusowe. Rób je jeśli masz czas lub chcesz pogłębić temat. Nie są wymagane do przejścia modułu.

---

## Agent mentor

W Copilot Chat wybierz agenta `mentor` i wpisz np. `ćwiczenie 5` — poprowadzi Cię krok po kroku.

---

## Żywe przykłady w repozytorium

Repo zawiera działające przykłady konfiguracji Copilot w `.github/`:

| Plik | Czego uczy |
|------|-----------|
| `.github/copilot-instructions.md` | Globalne instrukcje repo (moduł 03) |
| `.github/instructions/java-spring.instructions.md` | Scoped instructions z applyTo (moduł 03) |
| `.github/prompts/*.prompt.md` | Prompt files z frontmatter (moduł 03) |
| `.github/hooks/*.json` | Lifecycle hooks (moduł 04) |
| `.github/agents/*.agent.md` | Custom agenty (moduł 08) |

---

## Materiały MCP

Gotowe implementacje MCP server do nauki (moduł 09):
- `mcp_ex_api/` — wzorcowa implementacja FastAPI
- `mcp_jira_wiki/` — integracja z Jira/Wiki
- `mcp_for_databases/` — MCP do baz danych