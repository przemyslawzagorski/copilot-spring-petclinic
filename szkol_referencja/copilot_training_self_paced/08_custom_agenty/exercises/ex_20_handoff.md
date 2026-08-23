# Ex 20: Handoff między agentami

> Faza 6 · ~12 min · Moduł 08

**Po co:** Agenty mogą przekazywać sobie zadania przez **`handoffs:` w frontmatter**. Jeden badacz, drugi implementator — jak w realnym zespole.

> 📁 **Obaj agenci już istnieją w repo** — `.github/agents/researcher.agent.md`
> i `implementer.agent.md`. Listingi poniżej są do **porównania**, nie do
> przepisania. Otwórz oba pliki obok siebie i zwróć uwagę na jedno: `handoffs:`
> jest zadeklarowane **tylko u Researchera**. Przekazanie jest jednokierunkowe
> i to autor agenta decyduje, dokąd prowadzi.

## Co zrobić

1. Otwórz `.github/agents/researcher.agent.md` i porównaj z listingiem:

```markdown
---
name: Researcher
description: "Agent badawczy — analizuje, nie implementuje"
tools: [read, search, todo, agent]
handoffs:
  - label: Przekaż do Implementera
    agent: Implementer
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

Na końcu odpowiedzi dodaj zdanie: "Plan gotowy. Użyj przycisku handoff: Przekaż do Implementera."
```

2. Otwórz `.github/agents/implementer.agent.md` i porównaj:

```markdown
---
name: Implementer
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
Kliknij przycisk handoff `Przekaż do Implementera`.

(Fallback: ręcznie przełącz agenta na `implementer` i wklej prompt z planem.)
```

**Spodziewany wynik:** Researcher daje plan (pliki, kroki, ryzyka). Implementer pisze kod zgodnie z planem.

## Checklist walidacji

- W `researcher.agent.md` istnieje sekcja `handoffs:` z `label`, `agent`, `prompt`.
- Wartość `agent: Implementer` jest identyczna z polem `name` agenta docelowego.
- Po odpowiedzi `researcher` pojawia się przycisk handoff.
- `implementer` dostaje kontekst planu i nie rozszerza zakresu.

## 5. Zepsuj handoff — tu jest właściwa nauka

W `researcher.agent.md` zmień `agent: Implementer` na `agent: implementer`
(mała litera) i powtórz krok 3.

**Spodziewany wynik:** przycisk handoff przestaje działać albo znika. Wartość
`agent:` musi być **dokładnie** równa polu `name` agenta docelowego — to
najczęstsza przyczyna „handoff mi nie działa" i jedyna rzecz z tego ćwiczenia,
którą naprawdę warto zapamiętać.

> 🧹 **Posprzątaj:** `git checkout -- .github/agents/researcher.agent.md`

**Więcej:** `08_custom_agenty/EXERCISES.md`
