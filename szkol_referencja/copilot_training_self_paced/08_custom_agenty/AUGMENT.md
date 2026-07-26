# Moduł 08 - Custom agenty: adaptacja dla Augmenta

> Natywne subagenty Augmenta znajdują się w `.augment/agents/*.md`.

## Format i narzędzia

```yaml
---
name: performance-analyst
description: Analizuje wydajność JPA i wykrywa N+1 bez zmieniania kodu.
tools: view, codebase-retrieval
---
```

`tools` jest allowlistą, `disabled_tools` denylistą. Nie używaj obu pól naraz.
Brak obu pól oznacza dostęp do wszystkich narzędzi.

## Ex 18b i 18c: migracje

Wskaż źródłowy plik ścieżką. Dla refaktoryzacji architektury zacznij od `/ask`
albo `/plan`, aby najpierw otrzymać analizę bez edycji.

## Ex 19: własny subagent

Utwórz `.augment/agents/performance-analyst.md` według wzoru powyżej. Dodaj
format raportu: plik, problem, wpływ i rozwiązanie. Sprawdź przez `/agents`, a
następnie poproś głównego agenta o delegację analizy encji `Owner` i `Visit`.

## Ex 20: least privilege

Porównaj `.augment/agents/reviewer.md` z `tdd-expert.md`. Reviewer ma wyłącznie
narzędzia odczytu, a TDD Expert może edytować i uruchamiać procesy. Opis roli nie
zastępuje technicznego ograniczenia `tools`.

## Ex 21 i 21c: delegacja i kontekst

Auggie może zaproponować subagenta na podstawie jego `description`; możesz też
poprosić o delegację wprost. Format nie ma pola `handoffs:`. Agent główny
koordynuje kolejność i zbiera wyniki z izolowanych okien kontekstu.

Użyj promptu:

```text
Zaplanuj walidację telefonu Owner. Po akceptacji deleguj implementację do
tdd-expert, a końcowy przegląd do reviewer. Nie pomijaj testów.
```

## Ex 31: autonomiczna praca agenta

Zabezpieczenia globalne umieść w hookach i permissions. Dla długich zadań użyj
`/task`, kontroluj `/context`, oglądaj `/diffs` i zachowaj finalną walidację w
agencie głównym.