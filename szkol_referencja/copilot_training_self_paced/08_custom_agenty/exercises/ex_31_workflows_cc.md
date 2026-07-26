# Ex 31: Dynamic Workflows — autonomiczny agent w Claude Code

> Bonus · ~20 min · Odpowiednik ex_31_coding_agent.md dla Claude Code

**Po co:** Claude Code Workflows (2025) to orkiestracja dziesiątek równoległych subagentów realizujących jedno złożone zadanie. Tam gdzie Copilot Coding Agent przypisuje się do issue, Claude Code uruchamia całą flotę agentów.


## Teoria: subagent vs workflow vs /goal

| Mechanizm | Kiedy | Jak |
|---|---|---|
| Subagent | Jedno specjalistyczne podzadanie | `@"agent-name (agent)"` |
| `/goal` | Długotrwały cel przez wiele tur | `/goal [cel]` — Claude nie odpuszcza |
| Workflow (ultracode) | Równoległe zadania na dużą skalę | Słowo `ultracode` w prompcie |


## Krok 1: /goal — agent nie odpuszcza

Uruchom Claude Code i wpisz:

```
/goal Dodaj pole email do encji Owner z pełną walidacją, formularzami i testami.
Nie kończ dopóki ./mvnw test nie przechodzi.
```

`/goal` sprawia, że Claude Code:

Możesz na bieżąco obserwować co robi — albo zająć się czymś innym i wrócić za 10 minut.

**Różnica vs zwykły prompt:** `claude` bez `/goal` pyta Cię o potwierdzenie po każdym bloku zmian. `/goal` działa aż skończy.


## Krok 2: ultracode — orkiestracja równoległa

Dla bardziej złożonego zadania:

```
ultracode Przejrzyj cały projekt pod kątem bezpieczeństwa OWASP Top 10.
Sprawdź każdy pakiet osobno, zidentyfikuj problemy, zaproponuj fixes.
```

Co się dzieje:

Możesz śledzić postęp: `/workflows`

**Kiedy ultracode jest wart kosztu:**


## Krok 3: Porównanie z Copilot Coding Agent

| Aspekt | Copilot Coding Agent | Claude Code Workflows |
|---|---|---|
| Trigger | GitHub issue | Prompt w sesji (`ultracode`) |
| Output | Pull Request | Raport + edycje plików w sesji |
| Tracking | GitHub issue/PR UI | `/workflows` dashboard |
| Feedback loop | Komentarz w PR | Kontynuacja sesji |
| Skala | Jedno zadanie | Dziesiątki równoległych agentów |
| Dobra analogia | Senior dev working on a ticket | Engineering team sprint |


## Ćwiczenie: własny workflow

Stwórz plik `.claude/workflows/tdd-sprint.js` który:
1. Czyta wszystkie klasy w `src/main/java/`
2. Dla każdej bez testów — generuje szkielet JUnit 5
3. Dla każdej z testami — uruchamia i raportuje coverage

```javascript
export const meta = {
  name: 'tdd-sprint',
  description: 'Generuje brakujące testy JUnit 5 dla wszystkich klas',
  phases: [
    { title: 'Discover', detail: 'Znajdź klasy bez testów' },
    { title: 'Generate', detail: 'Generuj szkielety testów' },
  ]
}

phase('Discover')
const classes = await agent(
  'Znajdź wszystkie klasy Java w src/main/java/ które NIE mają odpowiadającego pliku testowego. Zwróć listę ścieżek.',
  { schema: { type: 'object', properties: { classes: { type: 'array', items: { type: 'string' } } }, required: ['classes'] } }
)

phase('Generate')
const results = await pipeline(
  classes.classes,
  (path) => agent(
    `Wygeneruj pełny szkielet testów JUnit 5 + Mockito dla klasy ${path}. Uwzględnij najważniejsze metody publiczne.`,
    { label: `test:${path.split('/').pop()}` }
  )
)
```

Wywołaj: `ultracode /workflows tdd-sprint`


## /claude agents — dashboard

Gdy uruchomisz /goal lub workflow:
```
claude agents
```
Widzisz wszystkie aktywne i zakończone sesje agentów — jak GitHub Actions dla Twojego lokalnego AI.


## Checklist walidacji

- [ ] `/goal` z testem kompilacji zakończył się bez interwencji
- [ ] `ultracode` uruchomił równoległe agenty (widać w `/workflows`)
- [ ] Stworzyłeś własny workflow script (choćby jako ćwiczenie)
- [ ] Rozumiesz kiedy używać `/goal` vs `ultracode` vs zwykłego subagenta
