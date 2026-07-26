# Augment i Auggie CLI - przewodnik po szkoleniu

> Szkolenie powstało dla GitHub Copilot, ale repozytorium zawiera również
> działające przykłady dla Augmenta. Ten plik jest punktem startowym dla
> uczestników używających Auggie CLI.

## Co działa wspólnie

Augment obsługuje kilka otwartych lub kompatybilnych formatów:

- automatycznie czyta `CLAUDE.md` i `AGENTS.md`,
- odkrywa Agent Skills z `.augment/skills/`, `.claude/skills/` i `.agents/skills/`,
- odkrywa custom commands z `.augment/commands/`, `.claude/commands/` i `.agents/commands/`,
- używa natywnych subagentów z `.augment/agents/`,
- używa natywnych rules z `.augment/rules/`,
- konfiguruje permissions, hooki i MCP w `.augment/settings.json`.

Repo stosuje podejście hybrydowe: współdzieli wiedzę, która ma zgodny format,
oraz dodaje natywne przykłady tam, gdzie semantyka Augmenta jest inna.

## Instalacja na Windows

Oficjalny Auggie CLI wspiera macOS, Linux oraz **Windows przez WSL**. Nie
uruchamiaj części CLI tego szkolenia w natywnym Windows PowerShell.

### 1. Uruchom WSL

W PowerShell jako administrator zainstaluj WSL, jeśli nie jest dostępny:

```powershell
wsl --install
```

Po restarcie otwórz dystrybucję WSL i przejdź do repozytorium. Dysk `C:` jest
zwykle dostępny pod `/mnt/c`:

```bash
cd /mnt/c/Users/USER/copilot/copilot-spring-petclinic
```

### 2. Zainstaluj Node.js 20+

Sprawdź wersję:

```bash
node --version
npm --version
```

Auggie wymaga Node.js 20 lub nowszego. Instaluj Node zgodnie z zasadami swojej
organizacji, najlepiej przez manager wersji dostępny w dystrybucji WSL.

### 3. Zainstaluj i uwierzytelnij Auggie

```bash
npm install -g @augmentcode/auggie
auggie --version
auggie login
```

Token uwierzytelniający jest sekretem użytkownika. Nigdy nie zapisuj wyniku
`auggie token print` w repozytorium, logach szkoleniowych ani zrzutach ekranu.

## Szybki start

W katalogu głównym repozytorium uruchom:

```bash
auggie
```

Przy pierwszym uruchomieniu Auggie indeksuje bieżący katalog Git. Pliki pasujące
do `.gitignore` i `.augmentignore` nie trafiają do indeksu.

W trybie interaktywnym wykonaj:

```text
/status
/rules
/skills
/agents
/hooks
/permissions
```

Następnie rozpocznij szkolenie:

```text
/training:exercise 1
```

Możesz też uruchomić kontrolę konfiguracji:

```text
/augment-workspace-check
```

## Najważniejsze skróty i komendy

| Akcja | Auggie |
|---|---|
| Ulepsz bieżący prompt kontekstem repo | `Ctrl+P` |
| Nowa linia w terminalu | `Ctrl+J` |
| Przerwij aktywnego agenta | `Esc` lub `Ctrl+C` |
| Tryb tylko do analizy | `/ask` |
| Plan przed implementacją | `/plan` |
| Zadania wieloetapowe | `/task` |
| Pytanie poboczne bez zmiany głównego wątku | `/btw <pytanie>` |
| Nowa czysta rozmowa | `/new` |
| Rozgałęzienie bieżącej rozmowy | `/fork` |
| Wznowienie sesji | `/sessions` |
| Użycie kontekstu | `/context` |
| Statystyki sesji | `/stats` |
| Zmiany plików | `/diffs` |
| Szczegóły narzędzi | `/verbose` |

Prompt Enhancer działa tylko w interactive mode i tylko wtedy, gdy pole wejścia
zawiera tekst. Po `Ctrl+P` zawsze przeczytaj i popraw wygenerowany prompt przed
wysłaniem.

## Mapa pojęć

| GitHub Copilot | Claude Code | Augment/Auggie |
|---|---|---|
| `.github/copilot-instructions.md` | `CLAUDE.md` | `CLAUDE.md`, `AGENTS.md`, `.augment/rules/*.md` |
| `.github/instructions/*.instructions.md` | hierarchiczne `CLAUDE.md` | `.augment/rules/*.md` lub hierarchiczne `CLAUDE.md`/`AGENTS.md` |
| `.github/prompts/*.prompt.md` | `.claude/commands/*.md` | `.augment/commands/*.md` |
| `.github/skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` | `.augment/skills/*/SKILL.md` oraz kompatybilne lokalizacje |
| `.github/agents/*.agent.md` | `.claude/agents/*.md` | `.augment/agents/*.md` |
| `.github/hooks/*.json` | `.claude/settings.json` | `hooks` w `.augment/settings.json` |
| ustawienia narzędzi agenta | `permissions` | `toolPermissions` i ograniczenia subagenta |
| `.copilotignore` | `.claudeignore` | `.augmentignore` oraz `.gitignore` |
| `.vscode/mcp.json` | `.mcp.json` | `mcpServers` w ustawieniach lub `auggie mcp` |

## Rules

Auggie ładuje reguły w następującej kolejności pierwszeństwa:

1. plik przekazany przez `--rules`,
2. `CLAUDE.md`,
3. `AGENTS.md`,
4. `.augment-guidelines`,
5. `.augment/rules/**/*.md`,
6. `~/.augment/rules/**/*.md`.

Reguły workspace w `.augment/rules/` obsługują dwa typy:

- `always_apply` - dołączane do każdego promptu,
- `agent_requested` - dołączane, gdy opis pasuje do zadania.

Typ `manual` jest obsługiwany przez rozszerzenia IDE, ale **pomijany przez CLI**.
W tym repo specjalistyczne reguły są `agent_requested`, aby nie obciążać każdej
rozmowy.

## Skills

Auggie implementuje standard Agent Skills. Skill musi znajdować się w osobnym
katalogu i zawierać `SKILL.md`:

```text
.augment/skills/nazwa-skilla/SKILL.md
```

Wymagany frontmatter:

```yaml
---
name: nazwa-skilla
description: Co robi skill i kiedy go używać
---
```

`name` musi odpowiadać nazwie katalogu, używać małych liter, cyfr i myślników.
Wywołanie `/<nazwa-skilla>` uruchamia skill bezpośrednio, a `/skills` pokazuje
wszystkie wykryte skille i ich koszt kontekstu.

Kolejność pierwszeństwa zaczyna się od `~/.augment/skills/`, potem
`.augment/skills/`, a następnie kompatybilnych lokalizacji `.claude/skills/` i
`.agents/skills/`. Wbudowane slash commands mają pierwszeństwo nad skillem o tej
samej nazwie.

## Subagenci

Subagenci znajdują się w `.augment/agents/*.md`. Każdy ma niezależne okno
kontekstu, własny prompt i opcjonalne ograniczenia narzędzi.

```yaml
---
name: reviewer
description: Read-only code reviewer
tools: view, codebase-retrieval
---
```

- `tools` jest allowlistą,
- `disabled_tools` jest denylistą,
- nie ustawiaj obu pól jednocześnie,
- brak obu pól daje dostęp do wszystkich narzędzi.

Subagenta można wskazać wprost w prompcie albo wybrać przez `/agents`. Auggie
może zaproponować delegację, gdy opis agenta pasuje do zadania. Format Augmenta
nie ma deklaratywnego pola `handoffs:` znanego z agentów Copilota; orkiestrację
prowadzi agent główny.

## Custom commands

Plik:

```text
.augment/commands/training/exercise.md
```

tworzy komendę:

```text
/training:exercise
```

Komendy mogą mieć `description`, `argument-hint` i opcjonalny `model`.
Wbudowane komendy mają pierwszeństwo, dlatego nazwy własne nie powinny używać
np. `help`, `model`, `rules`, `skills` ani `agents`.

Poza interactive mode możesz użyć:

```bash
auggie command list
auggie command training:validate all
```

## Hooki i permissions

Repo zawiera aktywne hooki WSL w `.augment/settings.json`:

- `SessionStart` - przekazuje minimalny kontekst workspace,
- `PreToolUse` - blokuje destrukcyjne komendy i zapis plików wrażliwych,
- `Stop` - przypomina o testach, ale nie blokuje zakończenia.

Hooki są synchroniczne. `PreToolUse` może zablokować narzędzie przez kod wyjścia
2 lub `permissionDecision: deny`. `PostToolUse` nie może cofnąć wykonanej operacji.
Modyfikowanie wejścia narzędzia przez hook nie jest obecnie obsługiwane.

`toolPermissions` stosują zasadę first match wins wewnątrz jednej polityki.
Między politykami wygrywa najbardziej restrykcyjna decyzja:

```text
deny > webhook-policy > script-policy > allow
```

Permissions są egzekwowane przez Auggie CLI i Cosmos. Nie traktuj ich jako
zabezpieczenia rozszerzenia Augment w VS Code lub JetBrains.

## MCP i integracje

Repo **nie aktywuje MCP automatycznie** w `.augment/settings.json`. Chroni to
uczestników przed przypadkowym uruchomieniem lokalnych serwerów, wysłaniem danych
do zewnętrznej usługi albo użyciem konfiguracji wymagającej sekretu.

Lokalne zarządzanie:

```bash
auggie mcp list
auggie mcp add publiczne-api -- python szkol_referencja/copilot_training_self_paced/mcp_ex_api/api_sever.py
auggie mcp remove publiczne-api
```

Auggie obsługuje transporty `stdio`, `http` i `sse`. Ustawienia MCP wspierają
`${workspaceFolder}` w `command`, `args` i `url`.

Sekrety zapisuj wyłącznie w ustawieniach użytkownika lub lokalnych ustawieniach
repo, nigdy w commitowanym `.augment/settings.json`. Przy wielu serwerach warto
włączyć MCP Tool Search:

```json
{
  "enableToolSearch": true
}
```

albo jednorazowo:

```bash
auggie --enable-tool-search
```

Tool Search ogranicza koszt schematów MCP w kontekście, udostępniając agentowi
narzędzia `find-tool` i `execute-tool`.

## Diagnostyka

### Reguła lub skill nie jest widoczny

1. Uruchom Auggie z katalogu głównego repo.
2. Sprawdź `/status`, `/rules` i `/skills`.
3. Zweryfikuj frontmatter oraz nazwę katalogu skilla.
4. Sprawdź kolizję z komendą wbudowaną.
5. Rozpocznij nową sesję, ponieważ reguły są cache'owane w rozmowie.

### Hook się nie uruchamia

1. Sprawdź `/hooks`.
2. Zweryfikuj matcher i nazwę narzędzia.
3. Upewnij się, że skrypt `.sh` ma prawa wykonania w WSL.
4. Uruchom hook ręcznie z fixture JSON.
5. Włącz logi: `auggie --log-level debug`.

### CLI nie działa w Windows

Uruchom polecenie w WSL, nie w natywnym PowerShell. Sprawdź `node --version` i
upewnij się, że Node 20+ oraz pakiet `@augmentcode/auggie` są zainstalowane
wewnątrz tej samej dystrybucji WSL.

## Adaptacje modułów

| Moduł | Adaptacja Augment |
|---|---|
| 01 - podstawy | `01_podstawy_copilot_chat/AUGMENT.md` |
| 02 - kontekst i prompty | Użyj oryginalnych ćwiczeń oraz Prompt Enhancer |
| 03 - konfiguracja | `03_konfiguracja_zespolowa/AUGMENT.md` |
| 04 - hooki | `04_hooks_i_guardrails/AUGMENT.md` |
| 05 - skills | `05_skills/AUGMENT.md` |
| 06 - TDD | Użyj oryginalnych ćwiczeń |
| 07 - bezpieczeństwo | Użyj oryginalnych ćwiczeń |
| 08 - custom agenty | `08_custom_agenty/AUGMENT.md` |
| 09 - MCP | `09_mcp_server/AUGMENT.md` |
| 10 - Copilot Python SDK | Specyficzny dla Copilota; brak odpowiednika w tej ścieżce |
| 11 - Agentic AI | `11_bonus_agentic_ai/AUGMENT.md` |

## Oficjalna dokumentacja

- CLI: https://docs.augmentcode.com/cli/overview
- Subagenci: https://docs.augmentcode.com/cli/subagents
- Rules: https://docs.augmentcode.com/cli/rules
- Skills: https://docs.augmentcode.com/cli/skills
- Permissions: https://docs.augmentcode.com/cli/permissions
- Integracje i MCP: https://docs.augmentcode.com/cli/integrations
- Hooki: https://docs.augmentcode.com/cli/hooks
- Custom commands: https://docs.augmentcode.com/cli/custom-commands
- Interactive mode: https://docs.augmentcode.com/cli/interactive
- Prompt Enhancer: https://docs.augmentcode.com/cli/interactive/prompt-enhancer