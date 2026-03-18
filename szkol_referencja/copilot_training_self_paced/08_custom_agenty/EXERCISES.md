# Ćwiczenia: Moduł 08 (Custom Agenty)

| # | Ćwiczenie | Plik | Czas |
|---|-----------|------|------|
| 18b | Migracja między językami — Java → Python | [ex_18b](exercises/ex_18b_migracja_jezyka.md) | ~15 min |
| 18c | Refaktoring architektury z AI | [ex_18c](exercises/ex_18c_migracja_architektury.md) | ~15 min |
| 19 | Twój pierwszy custom agent | [ex_19](exercises/ex_19_custom_agent.md) | ~10 min |
| 20 | Handoff między agentami | [ex_20](exercises/ex_20_handoff.md) | ~15 min |
| 21 | Triada agentów — Planner / Executor / Reviewer | [ex_21](exercises/ex_21_triada_agentow.md) | ~20 min |
| 21c | Feature Builder — agent koordynujący subagentów | [ex_21c](exercises/ex_21c_feature_builder_orchestration.md) | ~20 min |

**ex_18b, ex_18c i ex_21c są bonusowe.**

## Kolejność

ex_19 → ex_20 → ex_21 → (bonusy w dowolnej kolejności)

## Żywe przykłady agentów w repo

- `.github/agents/mentor.agent.md` — prosty agent
- `.github/agents/ports-adapters-refactor.agent.md` — fazowy workflow z argument-hint
- `.github/agents/senior-security-code-review.agent.md` — read-only (tools: read, search, todo)
- `.github/agents/vet-crud-feature.agent.md` — pełny cykl: analiza → plan → implementacja

Dodatkowe przykłady w `examples/.github/agents/`.
