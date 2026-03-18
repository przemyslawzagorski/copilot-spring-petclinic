# Ex 12b: Skill vs Prompt vs Hook vs Agent — kiedy co wybrać

> Faza 4 · ~10 min · Źródło: moduł 04
> Dokumentacja: https://code.visualstudio.com/docs/copilot/customization/agent-skills

**Po co:** Copilot oferuje 5 mechanizmów customizacji. Jeśli wybierzesz zły — albo nie zadziała, albo zadziała w złym momencie. To ćwiczenie buduje intuicję.

## Tabela referencyjna

| | **Instruction** | **Prompt File** | **Skill** | **Hook** | **Agent** |
|---|---|---|---|---|---|
| **Plik** | `*.instructions.md` | `*.prompt.md` | `SKILL.md` w folderze | `.json` + skrypt | `*.agent.md` |
| **Gdzie** | `.github/instructions/` | `.github/prompts/` | `.github/skills/*/` | `.github/hooks/` | `.github/agents/` |
| **Kiedy działa** | Zawsze (lub via `applyTo` glob) | Gdy jawnie wywołasz `/` | Auto-load LUB `/` | Na zdarzeniu agenta (PreToolUse, PostToolUse...) | Gdy przełączysz agenta |
| **Zasoby** | Nie | Nie | **Tak** (skrypty, szablony) | Tak (skrypt shell/python) | Nie |
| **Wykonuje kod** | Nie | Nie | Agent może użyć plików z folderu | **Tak** (deterministycznie) | Nie |
| **Portable** | Nie | Nie | **Tak** (agentskills.io) | Nie | Nie |
| **Analogia** | Tabliczka z regulaminem | Formularz do wypełnienia | Podręcznik procedury | Bramka bezpieczeństwa | Specjalista na telefon |

## Co zrobić

W Copilot Chat wpisz:

```
Dla każdego z 8 scenariuszy poniżej odpowiedz:
jaki mechanizm customizacji Copilota wybrałbyś i dlaczego?
Opcje: Instruction, Prompt File, Skill, Hook, Agent.
Odpowiedz w tabeli: # | scenariusz | wybór | dlaczego | co się stanie jeśli źle wybiorę

1. "Wszyscy w projekcie używają camelCase i JUnit 5"
2. "Chcę szablon do generowania serwisu Spring z testami"
3. "Blokada edycji plików .env i secrets/"
4. "Procedura debugowania problemów z bazą danych krok po kroku z checklistą"
5. "Automatyczny lint po każdej edycji pliku"
6. "Code review kontrolerów z ograniczonym scope — nie pisze kodu, tylko raportuje"
7. "Generowanie dokumentacji API z szablonami i przykładami"
8. "Wymuszenie conventional commits w każdym git commit"
```

## Prawidłowe odpowiedzi

| # | Scenariusz | Wybór | Dlaczego | Ryzyko złego wyboru |
|---|---|---|---|---|
| 1 | camelCase + JUnit 5 | **Instruction** | Reguła obowiązuje ZAWSZE, na WSZYSTKIE pliki Java | Prompt/Skill = model może zapomnieć |
| 2 | Szablon serwisu | **Prompt File** | Prosty szablon, bez zasobów, ręczne odpalenie | Skill = overengineering dla 1 pliku tekstu |
| 3 | Blokada .env | **Hook** (PreToolUse) | Musi deterministycznie blokować — model może "zapomnieć" | Instruction/Skill = brak gwarancji |
| 4 | Debugowanie bazy | **Skill** | Wielokrokowa procedura z checklistą, może mieć skrypty diagnostyczne | Prompt = za mało na procedurę wielokrokową |
| 5 | Auto-lint | **Hook** (PostToolUse) | Automatyzacja na zdarzeniu, niezależna od promptu | Prompt = trzeba ręcznie wołać za każdym razem |
| 6 | Code review | **Agent** | Ograniczony scope, jasne "czego NIE robi", persona | Skill = brak ograniczeń scope/tools |
| 7 | Dokumentacja API | **Skill** | Potrzebujesz szablonów + przykładów w folderze | Prompt = nie może mieć zasobów towarzyszących |
| 8 | Conventional commits | **Hook** (PreToolUse na git) | Format enforceable, model nie może go zignorować | Instruction = sugestia, nie enforcement |

## Zasada ogólna — zapamiętaj

```
"Obowiązuje ZAWSZE, bez wyjątków"         → Instruction
"Szablon do ręcznego użycia"              → Prompt File
"Procedura z zasobami/skryptami"          → Skill
"MUSI się wykonać, model nie może zignorować" → Hook
"Persona z ograniczonym scope i tools"     → Agent
```

## Dodatkowe pytanie (dla zaawansowanych)

```
Mam scenariusz: "Security review przed każdym mergem — skanuj kod,
zraportuj podatności, zablokuj jeśli krytyczne."

Czy to powinien być hook, skill, agent, czy kombinacja?
Zaproponuj architekturę.
```

**Prawidłowa odpowiedź:** Hook + Agent (lub Hook + Skill).
- **Hook** (PreToolUse) → uruchamia skan i blokuje przy krytycznych
- **Agent** (lub Skill) → analizuje wyniki i raportuje w formacie tabelarycznym
- Sam hook nie "myśli" — umie tylko blokować/przepuszczać
- Sam agent nie gwarantuje wykonania — może zapomnieć o skanie

**Spodziewany wynik:** Kursant potrafi przyporządkować scenariusz do mechanizmu i uzasadnić wybór. Rozumie dlaczego np. hook na lint jest lepszy od instrukcji, a skill na procedurę jest lepszy od prompt file.

**Więcej:** `05_skills/EXERCISES.md`
