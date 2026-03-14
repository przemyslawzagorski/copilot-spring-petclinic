# Ex 21c: Feature Builder — agent koordynujący subagentów

> Bonus · ~12 min · Między ex_21 a ex_22

**Po co:** To praktyczny wzorzec z dokumentacji VS Code: jeden agent nadrzędny (`Feature Builder`) uruchamia wyspecjalizowanych subagentów (`Researcher`, `Implementer`) w workflow research -> implement.

## Co zrobić

1. Utwórz `.github/agents/feature-builder.agent.md`:

```markdown
---
name: Feature Builder
description: "Buduje feature przez research, a potem implementację"
tools: [agent]
agents: [Researcher, Implementer]
---
Jesteś agentem koordynującym.

Dla każdego zadania:
1. Najpierw użyj subagenta `Researcher`, aby zebrać kontekst i wzorce z kodu.
2. Potem użyj subagenta `Implementer`, aby wdrożyć zmiany zgodnie z wynikami researchu.
3. Na końcu zwróć krótkie podsumowanie: co zbadano, co zmieniono, jakie ryzyka zostały.
```

2. Utwórz `.github/agents/researcher.agent.md` (wersja read-only):

```markdown
---
name: Researcher
description: "Research codebase patterns and gather context"
tools: [read, search]
---
Analizujesz kod read-only. Nie modyfikujesz plików.
Zwracasz: kontekst, pliki do zmian, rekomendowany plan.
```

3. Utwórz `.github/agents/implementer.agent.md`:

```markdown
---
name: Implementer
description: "Implement code changes based on provided context"
tools: [read, search, edit, execute, todo]
---
Implementujesz zmiany na podstawie planu i kontekstu od Researcher.
Wprowadzaj minimalne, precyzyjne modyfikacje.
```

4. Testuj orchestrację:

```text
Wybierz agenta `Feature Builder` i wpisz:
Dodaj walidację email w Owner + testy kontrolera.
Najpierw zrób research, potem implementację.
```

## Spodziewany wynik

- Agent nadrzędny deleguje pracę do subagentów zgodnie z kolejnością research -> implement.
- `Researcher` nie edytuje plików.
- `Implementer` wykonuje tylko zakres wynikający z researchu.

## Checklist walidacji

- W `feature-builder.agent.md` jest `tools: [agent]`.
- W `feature-builder.agent.md` jest `agents: [Researcher, Implementer]`.
- Nazwy w `agents:` są zgodne z polami `name` w plikach subagentów.
- Odpowiedź końcowa zawiera podsumowanie: findings -> changes -> risks.

**Więcej:** `13_module_13_agents_advanced_examples/EXERCISES.md`
