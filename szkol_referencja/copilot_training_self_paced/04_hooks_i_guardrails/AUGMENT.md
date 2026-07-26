# Moduł 04 - Hooki i guardrails: adaptacja dla Augmenta

> Repo zawiera aktywne hooki Auggie CLI w `.augment/settings.json`. Na Windows
> wykonuj ćwiczenia w WSL.

## Format

Hooki Augmenta są zdefiniowane w sekcji `hooks` ustawień. Skrypty dostają JSON
na stdin i zwracają JSON na stdout. Skrypt sukcesu powinien pozostać cichy.

| Zdarzenie | Zastosowanie w repo |
|---|---|
| `SessionStart` | minimalny kontekst projektu |
| `PreToolUse` | blokada komend i plików wrażliwych |
| `Stop` | nieblokujące przypomnienie o testach |

## Ex 11 (Auggie): deterministyczna blokada

Przejrzyj `.augment/hooks/block-sensitive.sh` oraz
`scripts/hooks/block-sensitive.py`. Matcher używa nazw narzędzi Auggie, np.
`str-replace-editor|save-file|remove-files`.

Bezpieczny test bez edycji sekretu:

```bash
printf '%s' '{"hook_event_name":"PreToolUse","tool_name":"save-file","tool_input":{"path":".env"}}' \
  | .augment/hooks/block-sensitive.sh
```

Oczekuj `permissionDecision: deny`. Nigdy nie twórz prawdziwego sekretu do testu.

## Ex 18 (Auggie): hook, rule czy command

| Potrzeba | Mechanizm |
|---|---|
| Deterministycznie blokuj operację | `PreToolUse` lub `toolPermissions` |
| Konwencja kodu | `CLAUDE.md` albo rule |
| Procedura ręczna | skill lub custom command |
| Przypomnienie na koniec | `Stop` z `systemMessage` |

`PostToolUse` nie może cofnąć wykonanej operacji. Hooki nie obsługują obecnie
modyfikowania wejścia narzędzia.

## Ex 21d (Auggie): zakres agenta

Auggie nie definiuje hooków w frontmatterze subagenta. Ogranicz zakres przez
`tools`/`disabled_tools` agenta, a globalne zabezpieczenie zostaw w ustawieniach.

Sprawdź konfigurację przez `/hooks` i `/permissions`.