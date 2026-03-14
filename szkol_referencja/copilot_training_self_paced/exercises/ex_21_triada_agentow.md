# Ex 21: Triada agentów — Planner / Executor / Reviewer

> Faza 6 · ~15 min · Źródło: moduł 13

**Po co:** Pełny workflow wieloagentowy: planowanie → wykonanie → review z oceną jakości. Przejścia realizujesz przez `handoffs:` w frontmatter (przyciski handoff).

## Co zrobić

1. Masz już `reviewer` (ex 19). Utwórz brakujące:

`.github/agents/planner.agent.md`:
```markdown
---
name: planner
description: "Agent planujący — plan-before-build"
tools: [read, search, todo, agent]
handoffs:
  - label: Przekaż do executor
    agent: executor
    prompt: |-
      Zrealizuj plan z poprzedniej odpowiedzi.
      Trzymaj się scope, listy plików i kryteriów sukcesu.
    send: false
---
Tworzysz plan implementacji z: krokami, ryzykami, kryteriami done, warunkiem rollback.
NIE piszesz kodu. NIE modyfikujesz plików.
Format: numerowana lista kroków z checkboxami.

Output contract (obowiązkowo):
- task goal
- affected files
- constraints
- success criteria
- rollback condition
- open risks
```

`.github/agents/executor.agent.md`:
```markdown
---
name: executor
description: "Agent wykonawczy — minimalny scope"
tools: [read, search, edit, execute, todo, agent]
handoffs:
  - label: Przekaż do reviewer
    agent: reviewer
    prompt: |-
      Oceń wdrożenie względem planu i kontraktu handoff.
      Zwróć wynik w kategoriach Critical/Major/Minor.
    send: false
---
Implementujesz DOKŁADNIE plan przekazany przez Planner.
Nie dodajesz nic ponad plan. Nie zmieniasz plików spoza listy.
```

2. Pełny cykl:

```
Wybierz agenta `planner` w pickerze i wpisz:
Zaplanuj dodanie walidacji chipId (format: 15 cyfr) do encji Pet z testami.
```

```
Kliknij przycisk handoff `Przekaż do executor`.
```

```
Kliknij przycisk handoff `Przekaż do reviewer`.

(Fallback: ręcznie przełącz agenta na `reviewer` i użyj promptu audytowego.)
```

**Spodziewany wynik:** 3 różne odpowiedzi, 3 różne perspektywy na to samo zadanie. Review łapie rzeczy, których executor nie przewidział.

## Checklist walidacji

- W `planner.agent.md` i `executor.agent.md` istnieje `handoffs:` z `label`, `agent`, `prompt`.
- Po odpowiedzi plannera pojawia się przycisk do executora.
- Po odpowiedzi executora pojawia się przycisk do reviewera.
- Reviewer raportuje wynik w kategoriach Critical/Major/Minor.

**Więcej:** `13_module_13_agents_advanced_examples/EXERCISES.md`
