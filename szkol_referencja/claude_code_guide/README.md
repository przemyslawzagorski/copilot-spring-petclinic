# Claude Code — Przewodnik po szkoleniu Copilot

> Szkolenie zostało zaprojektowane dla GitHub Copilot, ale każdy użytkownik **Claude Code** też się tu odnajdzie. Ten plik jest Twoim punktem startowym.

---

## Instalacja Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
claude --version          # Weryfikacja
claude                    # Uruchom w katalogu projektu
```

W **VSCode** — Claude Code Extension jest już zainstalowane (używasz go teraz).

---

## Kluczowe odkrycie: ten sam standard!

GitHub Copilot Skills i Claude Code Skills używają **tego samego otwartego standardu** [Agent Skills](https://agentskills.io).

Oznacza to, że pliki `SKILL.md` z `.github/skills/` są prawie bezpośrednio kompatybilne z `.claude/skills/`.

---

## Mapa pojęć: Copilot → Claude Code

| GitHub Copilot | Claude Code | Uwagi |
|---|---|---|
| `copilot-instructions.md` | `CLAUDE.md` | Instrukcje projektu, zawsze wczytywane |
| `.github/agents/*.agent.md` | `.claude/agents/*.md` | Subagenci, podobny format |
| `.github/skills/*/SKILL.md` | `.claude/skills/<name>/SKILL.md` | **Ten sam standard!** |
| `.github/prompts/*.prompt.md` | `.claude/commands/*.md` lub skills | Slash commands |
| `.github/instructions/*.instructions.md` | `CLAUDE.md` z `paths:` | Scoped instructions |
| `.github/hooks/*.json` | `hooks:` w `.claude/settings.json` | Inny format, te same zdarzenia |
| `.copilotignore` | `.claudeignore` | Identyczny format |
| `@workspace` | Niepotrzebny | Claude Code widzi pliki bezpośrednio |
| `#file:nazwa` | Podaj ścieżkę w prompcie | Lub użyj @ w VSCode |
| Copilot Memory | Auto memory (wbudowane) | Zapisuje w `~/.claude/projects/*/memory/` |
| Copilot Chat (Ctrl+Alt+I) | `claude` w terminalu / VSCode | Różne interfejsy |
| Tryby Agent/Ask/Plan | `/plan` do planowania | Domyślnie działa autonomicznie |
| `.vscode/mcp.json` | `.mcp.json` (root projektu) | MCP konfiguracja |

---

## Co jest skonfigurowane w tym projekcie dla Claude Code

### Subagenci (`.claude/agents/`)

Wywołuj: `@"nazwa (agent)"` lub opisz co chcesz zrobić

| Agent | Do czego | Narzędzia |
|---|---|---|
| `mentor` | Pomoc z ćwiczeniami (ma mapę wszystkich ex_01–ex_35) | Read-only |
| `reviewer` | Code review kontrolerów | Read-only |
| `tdd-expert` | TDD Red-Green-Refactor | Pełne narzędzia |
| `security-expert` | Audyt bezpieczeństwa | Read-only |
| `feature-builder` | Budowanie funkcjonalności | Pełne narzędzia |
| `mkdocs-documentation` | Generuj/aktualizuj docs MkDocs + C4 Mermaid | Pełne narzędzia |
| `exercise-validator` | Smoke test materiałów szkoleniowych | Read + Bash |

### Skills (`.claude/skills/`)

Wywołuj: `/nazwa-komendy`

| Skill | Wywołanie | Do czego |
|---|---|---|
| project-versions | `/project-versions` | Raport wersji Java/Spring/deps |
| method-deep-dive | `/method-deep-dive OwnerController#method` | Analiza metody + Mermaid |
| controller-testing | `/controller-testing OwnerController` | Generuj testy MockMvc |
| dependency-check | `/dependency-check` | Audyt CVE (tylko ręcznie) |
| exercise-dry-run | `/exercise-dry-run 01` | Dry-run ćwiczeń z modułu (PASS/FAIL/SKIP) |

### Hooki (`.claude/settings.json`)

- **PostToolUse (Edit/Write)** → `motivator.py` — losowa motywacja po edycji pliku
- **PreCompact** → `precompact-save.py` — zapisz notatkę przed kompresją kontekstu

### MCP (`.mcp.json`)

- `claude-code-docs` — pełnotekstowe przeszukiwanie dokumentacji Claude Code

---

## Mapa ćwiczeń — które moduły wymagają adaptacji

| Moduł | Temat | Identyczny? | Plik adaptacji |
|---|---|---|---|
| **01** | Podstawy chatu | ❌ Inny interfejs | `01_podstawy_copilot_chat/CLAUDE_CODE.md` |
| **02** | Kontekst i prompty | ✅ Identyczny | Użyj oryginalnych ćwiczeń |
| **03** | Konfiguracja zespołowa | ❌ Różne pliki konfiguracji | `03_konfiguracja_zespolowa/CLAUDE_CODE.md` |
| **04** | Hooki i guardrails | ❌ Inny format hooków | `04_hooks_i_guardrails/CLAUDE_CODE.md` |
| **05** | Skills | ⚠️ Prawie identyczny | `05_skills/CLAUDE_CODE.md` |
| **06** | TDD z Copilotem | ✅ Identyczny | Użyj oryginalnych ćwiczeń |
| **07** | Bezpieczeństwo | ✅ Identyczny | Użyj oryginalnych ćwiczeń |
| **08** | Custom Agenty | ❌ Różny format agentów | `08_custom_agenty/CLAUDE_CODE.md` |
| **09** | MCP Server | ⚠️ Prawie identyczny | `09_mcp_server/CLAUDE_CODE.md` |
| **10** | Python SDK | ❌ Inny SDK | `10_copilot_python_sdk/CLAUDE_CODE.md` |
| 🎁 **11** | BONUS — Agentic AI (tokeny, pętla, multi-tool) | ⚠️ Przekrojowy, komendy CC | `11_bonus_agentic_ai/CLAUDE_CODE.md` |

---

## Funkcje Claude Code bez odpowiednika w Copilot

| Funkcja | Opis | Jak użyć |
|---|---|---|
| **Dynamic context injection** | `` !`git diff HEAD` `` w SKILL.md wstrzykuje wynik polecenia | W plikach skills |
| **Workflows (ultracode)** | Orkiestracja dziesiątek subagentów | Dodaj `ultracode` do promptu |
| **Agent Teams** | Wiele agentów współpracujących z shared task list | Eksperymentalne, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
| **Forked subagents** | Subagent dziedziczy pełny kontekst rozmowy | `/fork zrób X` |
| **Memory dla agentów** | Subagenci uczą się między sesjami (`memory: project`) | W frontmatterze agenta |
| **Background agents** | Ctrl+B — przenieś zadanie w tło | Podczas działania subagenta |
| **`context: fork` w skills** | Skill uruchamia się w izolowanym subagent | W frontmatterze skill |

---

## Szybki start dla uczestnika Claude Code

1. Upewnij się że jesteś w root projektu: `ls CLAUDE.md`
2. Uruchom Claude Code: `claude` (CLI) lub użyj VSCode extension
3. Sprawdź wersje projektu: `/project-versions`
4. Porozmawiaj z mentorem: `@"mentor (agent)" pomóż mi z ćwiczeniem 1`
5. Otwórz `szkol_referencja/copilot_training_self_paced/` i zacznij od modułu 01

---

## Dokumentacja Claude Code

- Pełna dokumentacja: https://code.claude.com/docs
- MCP Quickstart: https://code.claude.com/docs/en/mcp-quickstart
- Subagenci: https://code.claude.com/docs/en/sub-agents
- Skills: https://code.claude.com/docs/en/skills
- Hooks: https://code.claude.com/docs/en/hooks-guide
