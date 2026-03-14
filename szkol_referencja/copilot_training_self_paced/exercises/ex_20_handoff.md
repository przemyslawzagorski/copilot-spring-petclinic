# Ex 20: Handoff między agentami

> Faza 6 · ~12 min · Źródło: moduł 07

**Po co:** Agenty mogą przekazywać sobie zadania przez **`handoffs:` w frontmatter**. Jeden badacz, drugi implementator — jak w realnym zespole.

## Co zrobić

1. Utwórz `.github/agents/researcher.agent.md`:

```markdown
---
name: researcher
description: "Agent badawczy — analizuje, nie implementuje"
tools: [read, search, todo, agent]
handoffs:
  - label: Przekaż do implementera
    agent: implementer
    prompt: |-
      Zrealizuj plan badawczy z poprzedniej odpowiedzi.
      Trzymaj się wskazanych plików, ograniczeń i kryteriów sukcesu.
    send: false
---

Analizujesz problem i tworzysz plan implementacji.

## Zakres
- Analiza istniejącego kodu
- Identyfikacja plików do zmian
- Lista kroków implementacji
- Ryzyka i ograniczenia

## Czego NIE robisz
- Nie piszesz kodu
- Nie modyfikujesz plików

## Kontrakt wyjścia (obowiązkowy)
- task goal
- affected files
- constraints
- success criteria
- open risks

Na końcu odpowiedzi dodaj zdanie: "Plan gotowy. Użyj przycisku handoff: Przekaż do implementera."
```

2. Utwórz `.github/agents/implementer.agent.md`:

```markdown
---
name: implementer
description: "Agent implementujący — realizuje plan"
tools: [read, search, edit, execute, todo]
---

Implementujesz KOD na podstawie przekazanego planu. Nic więcej.

## Zakres
- Kodowanie zgodne z planem
- Trzymanie się wyznaczonych plików

## Czego NIE robisz
- Nie planujesz
- Nie zmieniasz zakresu planu
```

3. Testuj:

```
Wybierz agenta `researcher` w pickerze i wpisz:
Chcę dodać pole email do encji Owner z walidacją. Zbadaj co trzeba zmienić.
```

4. Po otrzymaniu planu:

```
Kliknij przycisk handoff `Przekaż do implementera`.

(Fallback: ręcznie przełącz agenta na `implementer` i wklej prompt z planem.)
```

**Spodziewany wynik:** Researcher daje plan (pliki, kroki, ryzyka). Implementer pisze kod zgodnie z planem.

## Checklist walidacji

- W `researcher.agent.md` istnieje sekcja `handoffs:` z `label`, `agent`, `prompt`.
- Po odpowiedzi `researcher` pojawia się przycisk handoff.
- `implementer` dostaje kontekst planu i nie rozszerza zakresu.

**Więcej:** `07_module_07/EXERCISES.md` — ćwiczenie 2
