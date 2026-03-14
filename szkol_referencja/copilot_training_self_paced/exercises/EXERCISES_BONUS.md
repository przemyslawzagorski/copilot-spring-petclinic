# Ćwiczenia bonusowe — index

Bonusy uzupełniają luki w stosunku do programu szkolenia. Nazwane `ex_XXb_` / `ex_XXc_` — rób je **między** ćwiczeniami głównymi, w których się znajdują.

## Mapa: kiedy które bonusy

```
ex_01  Chat o projekcie
ex_02  Inline refaktor          ← + bonus krok: code smells
  └─ ex_02b  Panel Edits + Working Set     🆕 (Moduł 2 programu)
ex_03  Javadoc inline
  └─ ex_03b  Next Edit Suggestions         🆕 (Moduł 1 programu)
ex_04  Terminal przez chat
ex_05  @workspace vs #file
ex_06  Iteracja promptu         ← + bonus krok: SOLID refaktor
  ├─ ex_06b  Few-shot / CoT / Role         🆕 (Moduł 1 programu)
  └─ ex_06c  Characterization Test         🆕 (Moduł 3 programu)
ex_07  Test integracyjny
ex_08  copilot-instructions.md
  └─ ex_08b  Copilot Memory               🆕 (Moduł 4 programu)
ex_09  Instrukcje applyTo
  └─ ex_09b  Exclude files / .copilotignore 🆕 (Moduł 4 programu)
ex_10  Prompt file
  └─ ex_10b  Wybór modelu AI               🆕 (Moduł 4 programu)
ex_11  Pre-run hook
ex_12  Skill wersje
ex_13  TDD Red
ex_14  TDD Green
ex_15  TDD Refactor
  └─ ex_15b  Self-Correction Loop          🆕 (Moduł 5 programu)
ex_16  Security review
  └─ ex_16b  Mermaid diagramy              🆕 (Moduł 5 programu)
ex_17  Anti-injection
ex_18  Hook vs Prompt
  ├─ ex_18b  Migracja języka (Java→Python) 🆕 (Moduł 6 programu)
  └─ ex_18c  Migracja architektury         🆕 (Moduł 6 programu)
ex_19  Custom agent
ex_20  Handoff
ex_21  Triada agentów
  └─ ex_21b  Copilot Code Review           🆕 (Moduł 5 programu)
  └─ ex_21c  Feature Builder orchestration 🆕 (Moduł 13 programu)
  └─ ex_21d  Scoped Hooks (Preview)        🆕 (Moduł 13 programu)
ex_22  MCP Bootstrap
ex_23  MCP Endpoint
ex_24  MCP Hardening
  └─ ex_24b  Projekt końcowy               🆕 (Moduł 8 programu)
```

## Pokrycie programu szkolenia po dodaniu bonusów

| Moduł z programu | Główne ćwiczenia | Bonusy |
|---|---|---|
| M1: Komunikacja z AI | ex_01–06 | ex_03b (NES), ex_06b (techniki promptowania) |
| M2: Refaktoring z Edits | ex_02 | **ex_02b** (Panel Edits + Working Set) + bonus krok w ex_02 (code smells) |
| M3: Testowanie | ex_07, ex_13–15 | **ex_06c** (Characterization Tests) |
| M4: Konfiguracja zespołowa | ex_08–11 | **ex_08b** (Memory), **ex_09b** (exclude files), **ex_10b** (model selection) |
| M5: Agent Mode | ex_19–21, ex_16 | **ex_15b** (Self-Correction), **ex_16b** (Mermaid), **ex_21b** (Code Review), **ex_21d** (Scoped Hooks) |
| M6: Migracje z AI | — | **ex_18b** (język), **ex_18c** (architektura) |
| M7: MCP | ex_22–24 | (komplet w głównych) |
| M8: Projekt końcowy | — | **ex_24b** (łączy wszystko) |

## Czas bonusów

| Bonus | Czas |
|---|---|
| ex_02b Panel Edits | ~10 min |
| ex_03b NES | ~5 min |
| ex_06b Techniki promptowania | ~10 min |
| ex_06c Characterization Test | ~10 min |
| ex_08b Copilot Memory | ~5 min |
| ex_09b Exclude files | ~5 min |
| ex_10b Model selection | ~8 min |
| ex_15b Self-Correction Loop | ~10 min |
| ex_16b Mermaid diagramy | ~5 min |
| ex_18b Migracja języka | ~15 min |
| ex_18c Migracja architektury | ~12 min |
| ex_21b Copilot Code Review | ~8 min |
| ex_21c Feature Builder orchestration | ~12 min |
| ex_21d Scoped Hooks (Preview) | ~8 min |
| ex_24b Projekt końcowy | ~30 min |
| Bonus kroki w ex_02, ex_06 | ~10 min |
| **RAZEM bonusy** | **~163 min** |
