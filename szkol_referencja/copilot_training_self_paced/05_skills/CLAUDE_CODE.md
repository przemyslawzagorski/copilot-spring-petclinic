# Moduł 05 — Skills: adaptacja dla Claude Code

> Skills w Claude Code i Copilot używają **tego samego otwartego standardu** [Agent Skills](https://agentskills.io).
> Migracja z `.github/skills/` do `.claude/skills/` jest prawie bezpośrednia!

---

## Porównanie lokalizacji

| GitHub Copilot | Claude Code |
|---|---|
| `.github/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| `~/.copilot/skills/` (user) | `~/.claude/skills/` (user) |
| Wywołanie: picker w UI | Wywołanie: `/nazwa-komendy` |

Możesz też użyć `.claude/commands/<name>.md` — działa tak samo jak skill.

---

## Frontmatter: Copilot vs Claude Code

| Pole | Copilot | Claude Code | Uwagi |
|---|---|---|---|
| `name` | ✅ | ✅ | Display name |
| `description` | ✅ | ✅ | Kiedy Claude używa skill |
| `argument-hint` | ✅ | ✅ | Podpowiedź w autocomplete |
| `user-invocable` | ✅ | ✅ | Czy widoczny w `/` menu |
| `disable-model-invocation` | ✅ | ✅ | Tylko ręczne wywołanie |
| `when_to_use` | ✅ | ✅ | Dodatkowy kontekst dla Claude |
| `allowed-tools` | ❌ | ✅ **Nowe** | Narzędzia dozwolone podczas skill |
| `disallowed-tools` | ❌ | ✅ **Nowe** | Narzędzia zablokowane |
| `context: fork` | ❌ | ✅ **Nowe** | Uruchom w subagent |
| `agent` | ❌ | ✅ **Nowe** | Który subagent (przy context: fork) |
| `paths` | ❌ | ✅ **Nowe** | Glob pattern — kiedy auto-load |
| `effort` | ❌ | ✅ **Nowe** | Poziom wysiłku modelu |
| `shell` | ❌ | ✅ **Nowe** | `bash` lub `powershell` |

---

## Dynamic context injection — unikalne w Claude Code

W SKILL.md możesz wstrzyknąć wynik polecenia shell:

```markdown
## Aktualne zmiany w projekcie

!`git diff HEAD`

## Twoje zadanie

Przeanalizuj powyższe zmiany i zaproponuj commit message.
```

Backtick z wykrzyknikiem `` !`polecenie` `` wykonuje się **przed** wysłaniem do Claude — model widzi wynik, nie polecenie.

---

## Ex 12 (CC): Twój pierwszy skill w Claude Code

**Odpowiednik ex_12_skill_wersje.md**

Ten projekt już ma skill `/project-versions` w `.claude/skills/project-versions/SKILL.md` — otwórz go i przejrzyj.

**Ćwiczenie:** Stwórz własny skill z dynamic injection:

```bash
mkdir .claude/skills/git-summary
```

Utwórz `.claude/skills/git-summary/SKILL.md`:
```markdown
---
name: git-summary
description: Podsumowuje ostatnie zmiany git i sugeruje commit message. Używaj gdy pytasz o zmiany lub chcesz zrobić commit.
argument-hint: "[liczba commitów — domyślnie 5]"
allowed-tools: Bash
---

## Ostatnie zmiany w projekcie

### Status repozytorium
!`git status --short`

### Ostatnie commity
!`git log --oneline -${0:-5}`

### Zmiany w plikach
!`git diff HEAD --stat`

## Twoje zadanie

1. Podsumuj co się zmieniło w 3-5 punktach
2. Zaproponuj commit message w formacie: `typ: krótki opis`
   - typ: feat, fix, docs, refactor, test, chore
3. Wskaż jeśli widzisz coś niepokojącego (np. przypadkowo dodane pliki, zbyt duże zmiany)
```

Wywołaj: `/git-summary` lub `/git-summary 10`

---

## Ex 12b (CC): Skill vs Prompt vs Hook — matryca decyzyjna

**Odpowiednik ex_12b_skill_vs_prompt_vs_hook.md**

| Sytuacja | Claude Code rozwiązanie |
|---|---|
| Zawsze formatuj po edycji | **Hook** PostToolUse |
| Procedura do uruchamiania ręcznie | **Skill** z `disable-model-invocation: true` |
| Wiedza tła (konwencje projektu) | **CLAUDE.md** |
| Wielokrotnie używana procedura analizy | **Skill** (bez `disable-model-invocation`) |
| Specjalistyczny asystent na czas sesji | **Subagent** (`.claude/agents/`) |
| Automatyczna weryfikacja po każdej edycji | **Hook** PostToolUse (`type: agent`) |

**Unikalne w Claude Code:** Skill może działać w subagent (`context: fork`) — wtedy izoluje kontekst i zwraca tylko podsumowanie.

---

## Widoczność skills — tabela Claude Code

| `user-invocable` | `disable-model-invocation` | W `/` menu | Auto-load Claude |
|---|---|---|---|
| `true` (domyślne) | `false` (domyślne) | ✅ Tak | ✅ Tak |
| `false` | `false` | ❌ Nie | ✅ Tak (background) |
| `true` | `true` | ✅ Tak | ❌ Nie (tylko ręcznie) |
| `false` | `true` | ❌ Nie | ❌ Nie (ukryta) |

To mapuje się prawie 1:1 na matrycę Copilot skills!
