# Moduł 03 — Konfiguracja zespołowa: adaptacja dla Claude Code

> Ten plik zastępuje ćwiczenia ex_08–ex_10b dla użytkowników Claude Code.

---

## Hierarchia konfiguracji w Claude Code

```
1. Managed settings (IT/admin — nadrzędne)
2. ~/.claude/settings.json (user — wszystkie projekty)
3. .claude/settings.json (project — ten repo)
4. .claude/settings.local.json (local — tylko Ty, gitignored)
```

Odpowiednik Copilot:
```
1. copilot-instructions.md (global)
2. instructions/*.instructions.md (scoped)
3. prompts/*.prompt.md (manual)
4. skills/*/SKILL.md (auto-load/manual)
```

---

## Ex 08 (CC): CLAUDE.md — instrukcje projektu

**Odpowiednik ex_08_copilot_instructions.md**

Zamiast `.github/copilot-instructions.md` tworzysz `CLAUDE.md` w root projektu.

**Ten projekt już ma `CLAUDE.md`** — otwórz go i przejrzyj.

**Ćwiczenie:** Dodaj do `CLAUDE.md` sekcję z zasadami dla testów:
```markdown
## Zasady testów

- Zawsze uruchamiaj `./mvnw test` przed commitem
- Pokrycie testami minimum 70% dla kontrolerów
- Nazwy testów: `shouldDoXWhenY`
```

**Różnica:** CLAUDE.md jest zawsze wczytywany automatycznie. Nie ma opcji "wyłącz" dla konkretnego pliku jak w Copilot.

---

## Ex 08b (CC): Pamięć Claude Code

**Odpowiednik ex_08b_copilot_memory.md**

Claude Code ma wbudowany system auto-memory. Zamiast ręcznie konfigurować Copilot Memory:

1. Auto memory jest domyślnie włączone
2. Claude Code sam zapisuje ważne informacje w `~/.claude/projects/*/memory/`
3. Możesz powiedzieć: `Zapamiętaj, że w tym projekcie używamy Javadoc po polsku`
4. Sprawdź pliki pamięci: `ls ~/.claude/projects/`

---

## Ex 09 (CC): Scoped instructions (applyTo → paths)

**Odpowiednik ex_09_instrukcje_applyto.md**

Copilot używa `applyTo:` glob w frontmatterze `.instructions.md`. Claude Code ma dwie opcje:

**Opcja A — pole `paths:` w CLAUDE.md** (nie wszystkie wersje):
Stwórz `src/main/java/CLAUDE.md`:
```markdown
Reguły dla kodu Java w tym projekcie:
- Używaj Java records zamiast POJO
- Javadoc po polsku dla każdej publicznej klasy
```

**Opcja B — oddzielne CLAUDE.md w podfolderach:**
Claude Code automatycznie wczytuje `CLAUDE.md` z każdego katalogu podczas pracy.

**Ćwiczenie:** Stwórz `src/test/java/CLAUDE.md`:
```markdown
Zasady dla testów:
- JUnit 5, nigdy JUnit 4
- @WebMvcTest dla kontrolerów
- @DataJpaTest dla repozytoriów
```

---

## Ex 09b (CC): Wykluczanie plików

**Odpowiednik ex_09b_exclude_files.md**

> ⚠️ **Uwaga — to NIE jest odpowiednik 1:1.** Claude Code **nie wspiera**
> `.claudeignore`. Plik o tej nazwie nie blokuje odczytu — Claude przeczyta
> wskazany plik, jeśli go o to poprosisz. Traktowanie go jako zabezpieczenia
> to fałszywe poczucie bezpieczeństwa.

**Co działa naprawdę:** reguły `permissions.deny` w `.claude/settings.json`:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./credentials/**)"
    ]
  }
}
```

Dodatkowo Claude Code respektuje `.gitignore` przy automatycznym wyszukiwaniu
plików — ale to też nie jest twarda blokada odczytu.

**Ten projekt ma plik `.claudeignore`** — otwórz go. To celowy przykład
**nieskutecznego** zabezpieczenia: wygląda solidnie, wymienia `.env`,
`secrets/`, `credentials/`, i nie robi nic.

**Ćwiczenie** (odpowiada krokom z `ex_09b_exclude_files.md`):

1. Utwórz testowy plik `secrets/api-keys.txt` z treścią `FAKE_KEY=abc123`.
   Wzorzec `secrets/` **jest już** w `.claudeignore`.
2. Poproś Claude Code: `Pokaż zawartość pliku secrets/api-keys.txt`.
   Plik zostanie przeczytany mimo wpisu w `.claudeignore`.
3. Dodaj `"Read(./secrets/**)"` do `permissions.deny`
   w `.claude/settings.json`.
4. Uruchom Claude Code ponownie i powtórz prośbę z kroku 2. Teraz odczyt
   zostaje zablokowany.
5. Posprzątaj: usuń `secrets/api-keys.txt`.

**Wniosek:** różnica między „narzędzie tego nie zaindeksuje samo z siebie"
a „narzędzie nie może tego przeczytać" jest różnicą między wygodą a kontrolą.

---

## Ex 10 (CC): Slash commands (zamiast prompt files)

**Odpowiednik ex_10_prompt_file.md**

Zamiast `.github/prompts/*.prompt.md` używasz `.claude/skills/<name>/SKILL.md` lub `.claude/commands/<name>.md`.

**Ten projekt ma już 6 skills** — wywołaj przykładowe:
```
/project-versions
/method-deep-dive OwnerController#processCreationForm
```

**Ćwiczenie:** Stwórz własny skill:
```bash
mkdir .claude/skills/moj-skill
```

Utwórz `.claude/skills/moj-skill/SKILL.md`:
```markdown
---
name: moj-skill
description: Mój pierwszy skill w Claude Code
argument-hint: "[temat do analizy]"
---

Przeanalizuj $ARGUMENTS w projekcie Spring PetClinic.

1. Znajdź powiązany kod
2. Wyjaśnij jak działa
3. Zaproponuj ulepszenia
```

Wywołaj: `/moj-skill encja Owner`

---

## Ex 10b (CC): Wybór modelu

**Odpowiednik ex_10b_model_selection.md**

W Claude Code masz tylko modele Claude (nie GPT ani Gemini):

| Model | Kiedy używać |
|---|---|
| `claude-opus-4-8` | Złożone zadania, architektura, analiza |
| `claude-sonnet-4-6` | Domyślny — balans szybkości i jakości |
| `claude-haiku-4-5` | Szybkie pytania, proste zmiany |

Zmiana modelu:
```
/model
```
Lub w `settings.json`:
```json
{"model": "claude-opus-4-8"}
```

**Kluczowa różnica:** W Copilot możesz wybrać GPT-4o, Claude, Gemini. W Claude Code tylko modele Claude.
