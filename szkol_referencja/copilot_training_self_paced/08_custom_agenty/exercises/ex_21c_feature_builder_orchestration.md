# Ex 21c: Feature Builder — agent koordynujący subagentów

> Bonus · ~12 min · Między ex_21 a ex_22

**Po co:** To praktyczny wzorzec z dokumentacji VS Code: jeden agent nadrzędny (`Feature Builder`) uruchamia wyspecjalizowanych subagentów (`Researcher`, `Implementer`) w workflow research -> implement.

> 📁 **Wszyscy trzej agenci są już w repo** — `feature-builder.agent.md`,
> `researcher.agent.md` i `implementer.agent.md`. **Nie nadpisuj dwóch
> ostatnich**: to te same pliki, których używałeś w ex_20, razem z działającym
> `handoffs:`. Tutaj oglądasz je w drugiej roli — jako **subagentów**
> wołanych przez agenta nadrzędnego.

## Dwa sposoby na to samo

To ćwiczenie ma sens tylko w zestawieniu z ex_20. Ci sami dwaj agenci,
dwa różne mechanizmy łączenia:

| | ex_20 — handoff | ex_21c — orkiestracja |
|---|---|---|
| Kto decyduje o przejściu | **Ty**, klikając przycisk | **Agent nadrzędny**, sam |
| Gdzie zapisany związek | `handoffs:` u źródła | `agents:` u koordynatora |
| Kontrola nad krokiem | pełna — widzisz plan przed implementacją | żadna — dowiadujesz się na końcu |
| Kiedy lepsze | zmiany ryzykowne, chcesz zatwierdzić plan | zadania powtarzalne, ufasz przebiegowi |

## Co zrobić

1. Otwórz `.github/agents/feature-builder.agent.md` — to jedyny nowy element:

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

Zwróć uwagę na `tools: [agent]` — koordynator **nie ma** narzędzi do czytania
ani edycji plików. Nie potrafi zrobić roboty sam; jedyne, co umie, to
delegować. To celowe ograniczenie.

2. Sprawdź, że `agents: [Researcher, Implementer]` zgadza się co do znaku
   z polami `name:` w obu plikach subagentów. Ta sama pułapka co przy
   `handoffs:` w ex_20.

3. Testuj orkiestrację:

```text
Wybierz agenta `Feature Builder` i wpisz:
Dodaj walidację email w Owner + testy kontrolera.
Najpierw zrób research, potem implementację.
```

4. **Porównaj z ex_20.** To samo zadanie (pole email w `Owner`) przeszło już
   przez handoff. Zwróć uwagę na jedną rzecz: w ex_20 **widziałeś plan przed**
   napisaniem kodu i mogłeś go odrzucić. Tutaj dostajesz gotowy wynik
   i podsumowanie po fakcie.

## Spodziewany wynik

- Agent nadrzędny deleguje pracę do subagentów zgodnie z kolejnością research -> implement.
- `Researcher` nie edytuje plików.
- `Implementer` wykonuje tylko zakres wynikający z researchu.

## Checklist walidacji

- W `feature-builder.agent.md` jest `tools: [agent]`.
- W `feature-builder.agent.md` jest `agents: [Researcher, Implementer]`.
- Nazwy w `agents:` są zgodne z polami `name` w plikach subagentów.
- Odpowiedź końcowa zawiera podsumowanie: findings -> changes -> risks.
- `researcher.agent.md` **nadal ma** sekcję `handoffs:` z ex_20 — nie
  nadpisałeś go po drodze.

**Więcej:** `08_custom_agenty/EXERCISES.md`
