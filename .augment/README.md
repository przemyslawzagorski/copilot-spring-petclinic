# Augment workspace configuration

Ten katalog zawiera natywne przykłady konfiguracji Auggie CLI dla szkolenia.

## Źródła konfiguracji

| Element | Źródło w tym repo | Strategia |
|---|---|---|
| Zasady projektu | `CLAUDE.md` | Współdzielone z Claude Code, automatycznie czytane przez Auggie |
| Reguły kontekstowe | `.augment/rules/` | Natywne dla Augmenta |
| Skills | `.claude/skills/` i `.augment/skills/` | Wspólny standard Agent Skills |
| Subagenci | `.augment/agents/` | Natywne przykłady Augmenta |
| Komendy | `.augment/commands/` | Natywne slash commands |
| Hooki i permissions | `.augment/settings.json` | Egzekwowane przez Auggie CLI |

Nie kopiujemy całej konfiguracji Copilota i Claude Code. Duplikat powstaje tylko
tam, gdzie format albo zachowanie Augmenta jest inne.

## Ważne ograniczenia

- Auggie CLI na Windows uruchamiaj w WSL.
- `toolPermissions` są egzekwowane przez CLI i Cosmos, ale nie przez rozszerzenie IDE.
- Hooki używają nazw narzędzi takich jak `launch-process`, a permissions aktualnych
  nazw `terminal`, `read`, `edit` i `write`.
- MCP nie jest aktywowany w ustawieniach repo. Każdy uczestnik konfiguruje serwery lokalnie.
- Lokalne nadpisania zapisuj w `.augment/settings.local.json`; plik jest ignorowany przez Git.

Przewodnik uczestnika znajduje się w
`szkol_referencja/augment_guide/README.md`.