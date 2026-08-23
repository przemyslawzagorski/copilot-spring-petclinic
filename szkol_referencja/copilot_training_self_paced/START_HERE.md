# START HERE — Ścieżka krok po kroku

## Szybki start

1. Otwórz folder `copilot-spring-petclinic` w VS Code.
2. Wybierz ścieżkę narzędzia:
	- **GitHub Copilot:** wybierz agenta `mentor` i wpisz `ćwiczenie 1`.
	- **Claude Code:** przeczytaj [przewodnik Claude Code](../claude_code_guide/README.md).
	- **Augment/Auggie:** przeczytaj [przewodnik Augment](../augment_guide/README.md), uruchom `auggie` w WSL i wpisz `/training:exercise 1`.
3. Rób ćwiczenia po kolei — każde ćwiczenie jest w folderze swojego modułu.

---

## 11 modułów

Każdy moduł ma README (teoria), EXERCISES.md (index ćwiczeń) i folder `exercises/` z plikami ćwiczeń.

| # | Moduł | Ćwiczenia | Czas |
|---|-------|-----------|------|
| 01 | [Podstawy Copilot Chat](01_podstawy_copilot_chat/) | ex_01 – ex_04 | ~33 min |
| 02 | [Kontekst i Prompty](02_kontekst_i_prompty/) | ex_05 – ex_07 | ~48 min |
| 03 | [Konfiguracja zespołowa](03_konfiguracja_zespolowa/) | ex_08 – ex_10b | ~42 min |
| 04 | [Hooks i Guardrails](04_hooks_i_guardrails/) | ex_11, ex_11b, ex_18, ex_21d | ~45 min |
| 05 | [Skills](05_skills/) | ex_12, ex_12b | ~20 min |
| 06 | [TDD z Copilotem](06_tdd_z_copilotem/) | ex_13 – ex_15b | ~36 min |
| 07 | [Bezpieczeństwo](07_bezpieczenstwo/) | ex_16, ex_16b, ex_17, ex_21b | ~26 min |
| 08 | [Custom Agenty](08_custom_agenty/) | ex_18b, ex_18c, ex_19, ex_20, ex_21, ex_21c, ex_31 | ~96 min |
| 09 | [MCP Server](09_mcp_server/) | ex_22 – ex_24b | ~80 min |
| 10 | [Copilot Python SDK](10_copilot_python_sdk/) | ex_25 – ex_30 | ~125 min |
| 🎁 11 | [BONUS — Agentic AI: tokeny, pętla, multi-tool](11_bonus_agentic_ai/) | ex_32 – ex_35 | ~95 min |

**Łącznie:** 52 ćwiczenia (~646 min, w tym bonusy).

> 🎁 **Moduł 11** jest przekrojowy — rób go po przejściu modułów 01–10. Spina całość w 3 recepty: na pętlę agenta, na tokeny i na multinarzędziowość (stan: maj/czerwiec 2026).

---

## Ćwiczenia bonusowe (🅱️)

Ćwiczenia z literką „b", „c" lub „d" w nazwie są bonusowe. Rób je jeśli masz czas lub chcesz pogłębić temat. Nie są wymagane do przejścia modułu.

---

## Agent mentor

W Copilot Chat wybierz agenta `mentor` i wpisz np. `ćwiczenie 5` — poprowadzi Cię krok po kroku.

W Auggie użyj `/training:exercise 5` albo poproś o delegację do subagenta
`mentor`. Adaptacje narzędziowe znajdują się w plikach `CLAUDE_CODE.md` i
`AUGMENT.md` w odpowiednich modułach.

---

## Żywe przykłady w repozytorium

Repo zawiera działające przykłady konfiguracji Copilot w `.github/`, Claude Code
w `.claude/` i Augmenta w `.augment/`:

| Plik | Czego uczy |
|------|-----------|
| `.github/copilot-instructions.md` | Globalne instrukcje repo (moduł 03) |
| `.github/instructions/java-spring.instructions.md` | Scoped instructions z applyTo (moduł 03) |
| `.github/prompts/*.prompt.md` | Prompt files z frontmatter (moduł 03) |
| `.github/hooks/*.json` | Lifecycle hooks (moduł 04) |
| `.github/agents/*.agent.md` | Custom agenty (moduł 08) |
| `CLAUDE.md`, `.claude/skills/` | Współdzielone zasady i Agent Skills |
| `.augment/rules/*.md` | Kontekstowe rules Augmenta (moduł 03) |
| `.augment/hooks/*.sh` | Hooki Auggie CLI dla WSL (moduł 04) |
| `.augment/skills/*/SKILL.md` | Natywne Agent Skills (moduł 05) |
| `.augment/agents/*.md` | Subagenty Augmenta (moduł 08) |
| `.augment/commands/**/*.md` | Custom commands Augmenta |

---

## Materiały MCP

Gotowe implementacje MCP server do nauki (moduł 09):
- `mcp_ex_api/` — wzorcowa implementacja FastAPI
- `mcp_jira_wiki/` — integracja z Jira/Wiki
- `mcp_for_databases/` — MCP do baz danych