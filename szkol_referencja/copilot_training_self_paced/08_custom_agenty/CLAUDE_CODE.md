# Moduł 08 — Custom Agenty: adaptacja dla Claude Code

> Subagenci w Claude Code i Copilot mają podobny format, ale kilka kluczowych różnic.

---

## Porównanie formatu

| GitHub Copilot | Claude Code |
|---|---|
| `.github/agents/*.agent.md` | `.claude/agents/*.md` |
| Narzędzia: `read`, `edit`, `search` (lowercase) | Narzędzia: `Read`, `Edit`, `Write`, `Bash`, `Grep`, `Glob` (CamelCase) |
| `@AgentName` w chacie | `@"agent-name (agent)"` w chacie |
| Agenty mogą handoff do innych agentów | Subagenty **nie mogą** wywoływać kolejnych subagentów |
| `model:` (Claude/GPT/Gemini) | `model:` (tylko Claude) |

---

## Frontmatter agenta w Claude Code

```markdown
---
name: moj-agent
description: "Krótki opis — Claude używa go do decyzji o delegacji. Im dokładniejszy, tym lepiej."
tools: Read, Grep, Glob, Bash, Edit, Write
model: claude-sonnet-4-6
---

System prompt agenta...
```

**Pola opcjonalne:**
```yaml
permissionMode: allowAll      # lub restricted
memory: project               # agent uczy się między sesjami
hooks:                        # hooki aktywne tylko gdy ten agent działa
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "echo 'edited' >> log.txt"
mcpServers:                   # MCP serwery dostępne tylko dla tego agenta
  - name: "moj-mcp"
```

---

## Ex 19 (CC): Twój pierwszy subagent

**Odpowiednik ex_19_custom_agent.md**

Ten projekt ma kilka subagentów w `.claude/agents/`, między innymi mentor,
reviewer, tdd-expert, security-expert, feature-builder, mkdocs-documentation i
exercise-validator. Przejrzyj aktualną zawartość katalogu jako źródło wzorców.

**Ćwiczenie:** Stwórz subagenta do analizy wydajności:

Utwórz `.claude/agents/performance-analyst.md`:
```markdown
---
name: performance-analyst
description: "Analizuje wydajność kodu Java — N+1 queries, missing indexes, eager loading. Deleguj do tego agenta gdy widzisz problemy z bazą danych lub wolne zapytania."
tools: Read, Grep, Glob
---

Jesteś ekspertem od wydajności aplikacji Spring Boot. Analizujesz kod szukając:

1. **Problemy N+1 query** — pętle z wywołaniami do bazy danych
2. **Brakujące @Transactional** — metody serwisowe bez transakcji
3. **Eager vs Lazy loading** — nieodpowiednie FetchType
4. **Brakujące indeksy** — kolumny JOIN bez @Index

## Format raportu

Dla każdego problemu:
- **Plik:** ścieżka:linia
- **Problem:** co jest nie tak
- **Wpływ:** szacowany wpływ na wydajność (Wysoki/Średni/Niski)
- **Rozwiązanie:** konkretna zmiana do wprowadzenia

Zawsze sprawdzaj klasy w `src/main/java/` i konfigurację JPA.
```

Wywołaj: `@"performance-analyst (agent)" przeanalizuj klasy Owner i Visit`

## Ex 18b (CC): Migracja Java → Python

**Odpowiednik ex_18b_migracja_jezyka.md**

Zamiast składni `#file` wskaż ścieżkę bezpośrednio:
```
Przeczytaj src/main/java/org/springframework/samples/petclinic/owner/Owner.java
i przekonwertuj encję na SQLAlchemy + Pydantic zgodnie z krokami ex_18b.
```

## Ex 18c (CC): Refaktoring architektury

**Odpowiednik ex_18c_migracja_architektury.md**

Claude Code automatycznie widzi workspace. Użyj promptu:
```
Przeanalizuj architekturę tego repo zgodnie z checklistą ex_18c. Najpierw zwróć
wyłącznie plan refaktoryzacji, bez edycji plików.
```

---

## Ex 20 (CC): Agenty read-only vs pełne uprawnienia

**Odpowiednik ex_20_handoff.md**

W Claude Code uprawnienia agenta ustawiasz przez pole `tools:`:

**Agent tylko do odczytu (bezpieczny, do analizy):**
```yaml
tools: Read, Grep, Glob
```

**Agent z pełnymi uprawnieniami (może edytować pliki):**
```yaml
tools: Read, Edit, Write, Bash, Grep, Glob
```

**Agent z dostępem do terminala (pomija pytania o uprawnienia):**
```yaml
tools: Read, Edit, Write, Bash, Grep, Glob
permissionMode: bypassPermissions
```

> Dozwolone wartości `permissionMode`: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`.
> (Nie ma wartości `allowAll` ani `restricted` — ogranicz agenta zawężając pole `tools:`.)

**Reguła:** Zawsze daj agentowi minimum potrzebnych narzędzi. Agent do code review nie potrzebuje `Write`.

---

## Ex 21 (CC): Wielozadaniowość — Agent Teams (eksperymentalne)

**Odpowiednik ex_21_triada_agentow.md**

Copilot wspiera handoff między agentami (A → B → C). Claude Code ma dwa podejścia:

### Podejście 1: Opis zadania (Claude sam deleguje)

```
Wykonaj pełne TDD dla nowej funkcji dodawania wizyty:
1. Najpierw napisz testy (użyj @"tdd-expert (agent)")
2. Zaimplementuj kod
3. Wykonaj code review (użyj @"reviewer (agent)")
```

Claude sam zdecyduje kiedy delegować.

### Podejście 2: Agent Teams (eksperymentalne)

Wymaga ustawienia zmiennej środowiskowej:
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Windows PowerShell:
```powershell
$env:CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = "1"
```

Potem możesz pisać zadania z wieloma agentami działającymi równolegle — ale to funkcja eksperymentalna i API może się zmienić.

### Podejście 3: Workflows (dla złożonych orkiestracji)

Dla bardziej deterministycznych wieloagentowych zadań użyj Workflows:
```
ultracode przeanalizuj i napraw wszystkie problemy bezpieczeństwa w projekcie
```

Słowo `ultracode` uruchamia tryb wieloagentowy.

---

## Ex 21c (CC): Agenty z pamięcią

**Odpowiednik ex_21c_feature_builder_orchestration.md**

Claude Code subagenci mogą mieć pamięć między sesjami:

```markdown
---
name: project-historian
description: "Zna historię projektu — poprzednie decyzje, problemy, refaktoryzacje. Konsultuj przed dużymi zmianami."
tools: Read, Glob
memory: project
---

Jesteś historykiem projektu. Pamiętasz wszystkie ważne decyzje architektoniczne.

Przy każdym uruchomieniu sprawdź zapisane wspomnienia i uwzględnij je w odpowiedziach.
Gdy uczysz się czegoś ważnego, zaznacz to: "ZAPAMIĘTAJ: [co]"
```

Subagent z `memory: project` sam zapisuje i wczytuje notatki między sesjami.

---

## Ex 31 (CC): Dynamic Workflows i /goal

**Odpowiednik ex_31_coding_agent.md (Copilot Coding Agent)**

Ćwiczenie ma dedykowany plik: [ex_31_workflows_cc.md](exercises/ex_31_workflows_cc.md)

Skrót kluczowych konceptów:

| Concept | Copilot | Claude Code |
|---|---|---|
| Autonomiczny agent | Coding Agent (GitHub issue → PR) | `/goal [cel]` — nie odpuszcza aż skończy |
| Równoległe agenty | Brak | `ultracode` — dziesiątki agentów naraz |
| Dashboard | GitHub PR view | `/workflows` + `claude agents` |
| Tracking | Issue/PR status | Task notifications w sesji |

---

## Kluczowa różnica: brak handoff chain w Claude Code

W Copilot możesz zdefiniować:
```yaml
handoffs:
  - label: Przekaż do reviewera
    agent: reviewer
    prompt: "Przejrzyj wdrożenie z poprzedniego kroku."
    send: false
```

**W Claude Code tego nie ma.** Zamiast tego:
- Claude sam decyduje kiedy delegować na podstawie opisu agenta
- Możesz jawnie prosić o delegację w prompcie
- Dla deterministycznych workflow użyj Workflows (ultracode)

Ta różnica jest celowa — Claude Code preferuje elastyczne podejmowanie decyzji zamiast sztywnych reguł.

---

## Delegacja bez pisania agenta: `/subtask` i `/background`

Nie każde oddelegowanie wymaga pliku w `.claude/agents/`. Dwie komendy
załatwiają przypadki jednorazowe.

| Komenda | Co robi | Kiedy |
|---|---|---|
| `/subtask` | oddaje zadanie poboczne subagentowi, który wraca z raportem | Gadatliwe zadanie, którego wynik chcesz, a przebiegu nie |
| `/background` | odpina bieżącą sesję i puszcza ją w tle | Długie zadanie, przy którym nie chcesz czekać |

**Po co to w module o agentach:** `/subtask` rozwiązuje ten sam problem co
subagent z pliku — chroni Twoje okno kontekstu przed zalaniem — tylko bez
konfiguracji. Subagent dostaje **własne okno**, wykonuje robotę i oddaje
streszczenie.

**Ćwiczenie (~5 min), rozszerzenie ex_20:**

1. Najpierw bez delegacji — sprawdź `/context`, zapamiętaj zajętość:

```
Przeskanuj wszystkie kontrolery w projekcie i wypisz każdy endpoint HTTP
z jego metodą, ścieżką i tym, czy waliduje wejście.
```

2. Sprawdź `/context` ponownie. Skan wszedł do Twojej rozmowy w całości.
3. `/rewind` → **Restore conversation** (kod nietknięty, historia czysta).
4. To samo przez delegację:

```
/subtask Przeskanuj wszystkie kontrolery i wypisz każdy endpoint HTTP
z metodą, ścieżką i informacją o walidacji wejścia. Zwróć samą tabelę.
```

5. `/context` po raz trzeci.

**Spodziewany wynik:** wersja z `/subtask` zostawia w Twoim oknie samą tabelę,
zamiast całej ścieżki przeszukiwania. To jest ten sam mechanizm, który
w module 11 opisany jest jako filar oszczędzania kontekstu — tutaj widzisz go
na liczbach.

> **Uwaga z ex_11b:** edycje subagenta zwykle **nie cofają się** przez
> `/rewind`. Do delegowania zadań, które piszą po plikach, rób commit
> wcześniej.
