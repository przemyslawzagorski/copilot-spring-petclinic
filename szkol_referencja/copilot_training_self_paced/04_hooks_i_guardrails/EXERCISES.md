# Ćwiczenia: Moduł 04 (Hooks i Guardrails)

| # | Ćwiczenie | Plik | Czas |
|---|-----------|------|------|
| 11 | PreToolUse hook — strażnik sekretów | [ex_11](exercises/ex_11_prerun_hook.md) | ~15 min |
| 11b | Checkpointy — co naprawdę da się cofnąć (bonus) | [ex_11b](exercises/ex_11b_checkpointy_i_rewind.md) | ~12 min |
| 18 | Hook vs Prompt — kiedy co | [ex_18](exercises/ex_18_hook_vs_prompt.md) | ~10 min |
| 21d | Scoped Hooks (Preview) — Strict Formatter Agent | [ex_21d](exercises/ex_21d_scoped_hooks_preview.md) | ~8 min |

## Kolejność

ex_11 → ex_11b → ex_18 → ex_21d (wymagane: `chat.useCustomAgentHooks`)

## Żywe przykłady hooków w repo

- `.github/hooks/06-motivator.json` — PostToolUse hook z filtrowaniem narzędzi
- `.github/hooks/07-precompact.json` — PreCompact hook logujący do pliku
- `scripts/hooks/motivator.py` — skrypt Python dla hooka
- `scripts/hooks/precompact-save.py` — skrypt Python dla PreCompact

Dodatkowe przykłady w `examples/hooks/` — 10 hooków z różnymi lifecycle events.
