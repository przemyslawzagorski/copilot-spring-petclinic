# Moduł 11 (BONUS) - Agentic AI: adaptacja dla Augmenta

> Pętla agentowa, zarządzanie kontekstem i routing między narzędziami pozostają
> uniwersalne. Poniżej są odpowiedniki komend Auggie.

## Mapa komend

| Potrzeba | Auggie |
|---|---|
| Diagnoza kontekstu | `/context` i `/stats` |
| Czysta rozmowa | `/new` |
| Rozgałęzienie rozmowy | `/fork` |
| Wznowienie | `/sessions` |
| Plan przed kodem | `/plan` |
| Wieloetapowe zadanie | `/task` |
| Pytanie poboczne | `/btw` |
| Zmiany | `/diffs` |
| Szczegóły narzędzi | `/verbose` |

## Ex 32: kontekst i koszt

Uruchom `/context`, sprawdź udział rules, historii, wyników narzędzi i MCP.
Specjalistyczną wiedzę trzymaj w `agent_requested` rules i skills zamiast w
regule dołączanej zawsze. Przy wielu narzędziach MCP włącz Tool Search.

Subagent ma osobne okno kontekstu, ale nie jest darmowy. Deleguj duży,
samodzielny skan lub review; prostą odpowiedź wykonuj w głównym wątku.

## Ex 33: pętla agentowa

Auggie nie używa deklaratywnych `handoffs:`. Zleć agentowi głównemu kolejność:

```text
1. Zbadaj Owner i zaproponuj plan walidacji telefonu.
2. Poczekaj na akceptację planu.
3. Deleguj cykl Red-Green-Refactor do tdd-expert.
4. Deleguj read-only review do reviewer.
5. Uruchom testy i podsumuj różnice.
```

## Ex 34: prompt i routing

Użyj `Ctrl+P`, aby rozszerzyć krótki prompt kontekstem repo, ale przed wysłaniem
usuń zbędne wymagania. Wybieraj model przez `/model` stosownie do ryzyka i
złożoności, nie według stałej nazwy z materiału.

## Ex 35: multi-tool

Wspólne artefakty (`CLAUDE.md`, Agent Skills, serwery MCP) ograniczają duplikację,
ale każde narzędzie ma własne permissions i format agentów. Cross-check wykonuj
na osobnym worktree lub gałęzi i porównuj `git diff`; nie pozwalaj dwóm agentom
edytować tych samych plików jednocześnie.

Więcej: `../../augment_guide/README.md`.