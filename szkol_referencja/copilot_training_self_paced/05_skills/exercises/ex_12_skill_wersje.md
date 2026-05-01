# Ex 12: Skill — raport wersji projektu (SKILL.md)

> Faza 4 · ~10 min · Źródło: moduł 04
> Dokumentacja: https://code.visualstudio.com/docs/copilot/customization/agent-skills

**Po co:** Skill to folder z plikiem `SKILL.md` — specjalistyczna umiejętność, którą Copilot ładuje automatycznie lub na żądanie (`/`). W odróżnieniu od prompt file, skill może zawierać zasoby (skrypty, szablony, przykłady) i jest zgodny z otwartym standardem [agentskills.io](https://agentskills.io/).

## Przypomnienie: czym NIE jest skill

| To NIE jest skill | To JEST skill |
|---|---|
| Plik `.github/prompts/*.prompt.md` | Folder `.github/skills/<nazwa>/SKILL.md` |
| Tekst w `copilot-instructions.md` | Folder z instrukcjami + opcjonalnymi zasobami |
| Sekcja w `package.json` | Plik SKILL.md z YAML frontmatter (`name`, `description`) |

## Co zrobić

### 1. Utwórz folder skilla

```
.github/skills/project-versions/SKILL.md
```

### 2. Wpisz zawartość SKILL.md

```markdown
---
name: project-versions
description: "Raportuje wersje Java, Spring Boot i główne zależności z pom.xml. Użyj gdy ktoś pyta o wersje, stack technologiczny, zależności lub kompatybilność."
argument-hint: "[opcjonalnie: nazwa konkretnej zależności]"
---

# Raport wersji projektu

## Procedura

1. Otwórz `pom.xml` w katalogu głównym projektu.
2. Odczytaj:
   - Wersję Java z `<java.version>` w `<properties>`
   - Wersję Spring Boot z `<parent><version>`
   - Wszystkie zależności z `<dependencies>` — podaj groupId, artifactId i wersję
3. Sprawdź datę ostatniego commita: `git log -1 --format="%cd" --date=short`
4. Zwróć wynik w tabeli Markdown.

## Format wyjścia

| Komponent | Wersja |
|---|---|
| Java | (z pom.xml) |
| Spring Boot | (z parent) |
| (zależność 1) | (wersja) |
| ... | ... |
| Ostatni commit | (data) |

## Kiedy NIE używać
- Gdy pytanie dotyczy wersji runtime (zainstalowane JDK) — to inne pytanie.
- Gdy chcesz zmienić wersje — ten skill tylko raportuje.
```

### 3. Przetestuj — 3 sposoby

**A) Auto-load (naturalny język):**
```
Jakie wersje Java i Spring Boot używa ten projekt?
```
Copilot powinien SAM znaleźć skill na podstawie `description`.

**B) Slash command:**
```
/project-versions
```
Skill musi pojawić się w menu `/`.

**C) Menu Configure Skills:**
Wpisz `/skills` w chat → otwiera się menu → skill `project-versions` powinien być na liście.

### 4. Zweryfikuj wynik

- Porównaj tabelę z zawartością `pom.xml`
- Java powinna być 17
- Spring Boot powinien być 3.x
- Zależności powinny mieć poprawne wersje

## Kluczowe zasady (zapamiętaj!)

1. **Nazwa folderu = `name` w frontmatter.** `project-versions/` → `name: project-versions`. Inaczej skill nie zadziała.
2. **`description` decyduje o auto-load.** Im lepszy opis, tym trafniejsze automatyczne ładowanie.
3. **Skill ≠ Prompt File.** Skill może mieć zasoby (skrypty, szablony). Prompt file to jeden plik z tekstem.

## Typowe błędy

| Objaw | Przyczyna | Fix |
|---|---|---|
| Skill nie widać w `/` menu | Nazwa folderu ≠ `name` | Wyrównaj nazwy |
| Skill nie auto-loaduje | Brak/zbyt ogólny `description` | Dodaj "Użyj gdy..." |
| Plik SKILL.md nie wykryty | Zła lokalizacja | Musi być w `.github/skills/<nazwa>/SKILL.md` |
| Frontmatter nie parsowany | Brak `---` na początku i końcu | Sprawdź delimitery YAML |

**Spodziewany wynik:** Tabela z Java 17, Spring Boot 4.0.3 i głównymi zależnościami — wygenerowana przez skill, nie przez prompt file.

**Więcej:** `05_skills/EXERCISES.md`
