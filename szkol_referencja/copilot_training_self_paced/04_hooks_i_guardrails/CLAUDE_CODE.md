# Moduł 04 — Hooki i Guardrails: adaptacja dla Claude Code

> Ten plik zastępuje ćwiczenia ex_11, ex_18, ex_21d dla użytkowników Claude Code.

---

## Kluczowa różnica: format hooków

| GitHub Copilot | Claude Code |
|---|---|
| Osobne pliki `.github/hooks/*.json` | Sekcja `hooks:` w `.claude/settings.json` |
| `PostToolUse`, `PreCompact` (kilka zdarzeń) | 25+ zdarzeń cyklu życia |
| Skrypt wywoływany przez `command` | `command`, `http`, `mcp_tool`, `prompt`, `agent` |

---

## Zdarzenia hooków w Claude Code

| Zdarzenie | Kiedy odpala | Odpowiednik Copilot |
|---|---|---|
| `PostToolUse` | Po użyciu narzędzia (np. edycji pliku) | `PostToolUse` ✅ identyczny |
| `PreCompact` | Przed kompresją kontekstu | `PreCompact` ✅ identyczny |
| `PreToolUse` | Przed użyciem narzędzia — może zablokować | Brak bezpośredniego |
| `Stop` | Gdy Claude kończy odpowiedź | Brak bezpośredniego |
| `SessionStart` | Na początku sesji | Brak bezpośredniego |
| `Notification` | Gdy Claude czeka na input | Brak bezpośredniego |
| `SubagentStart/Stop` | Gdy subagent startuje/kończy | Brak bezpośredniego |
| `PermissionRequest` | Gdy Claude prosi o uprawnienie | Brak bezpośredniego |
| `ConfigChange` | Gdy zmienia się plik konfiguracji | Brak bezpośredniego |

---

## Format hooków w Claude Code

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/hooks/motivator.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "scripts/hooks/validate-command.sh"
          }
        ]
      }
    ]
  }
}
```

**Kody wyjścia:**
- `exit 0` — brak decyzji, akcja kontynuuje normalnie
- `exit 2` — zablokuj akcję, wyślij stderr do Claude jako feedback
- `exit 1` (inne) — błąd hooka, akcja kontynuuje

---

## Ex 11 (CC): Hook guardrail (PreToolUse)

**Odpowiednik ex_11_prerun_hook.md**

**Cel:** Zablokuj edycję pliku `.env` przez Claude.

**Krok 1** — Utwórz skrypt `.claude/hooks/protect-env.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))")

if [[ "$FILE_PATH" == *".env"* ]]; then
  echo "Zablokowano: plik .env jest chroniony" >&2
  exit 2
fi
exit 0
```

**Krok 2** — Dodaj do `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/protect-env.sh"
          }
        ]
      }
    ]
  }
}
```

**Test:** Poproś Claude o edycję pliku `.env` — powinien zobaczyć komunikat o blokadzie.

---

## Ex 18 (CC): Hook vs Prompt — kiedy co używać

**Odpowiednik ex_18_hook_vs_prompt.md**

| Sytuacja | Copilot | Claude Code |
|---|---|---|
| Zawsze formatuj po edycji | Hook PostToolUse | Hook PostToolUse |
| Waliduj polecenia terminala | Hook PreToolUse | Hook PreToolUse |
| Styl kodu i konwencje | copilot-instructions.md | CLAUDE.md |
| Procedura deploymentu | Prompt file | Skill z `disable-model-invocation: true` |
| Background knowledge | Skill (auto-load) | Skill (`user-invocable: false`) |
| Zawsze weryfikuj testy przed stopem | Brak | Hook Stop (`type: agent`) |

**Reguła Claude Code:** Hook = deterministyczna reguła. Skill = procedura/wiedza. CLAUDE.md = fakty i konwencje.

---

## Ex 21d (CC): Agent-scoped hooki

**Odpowiednik ex_21d_scoped_hooks_preview.md**

W Claude Code hooki można definiować bezpośrednio w frontmatterze subagenta:

```markdown
---
name: code-reviewer
description: Agent do code review
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "npx prettier --check $FILE_PATH"
  Stop:
    - hooks:
        - type: command
          command: "echo 'Review zakończony' >> review-log.txt"
---

Jesteś recenzentem kodu...
```

Hooki w frontmatterze agenta działają **tylko gdy ten agent jest aktywny** — nie wpływają na główną sesję.

---

## Typy hooków unikalne dla Claude Code

### Prompt-based hook (LLM ocenia)
```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Czy wszystkie zadania zostały wykonane? Jeśli nie, zwróć {\"ok\": false, \"reason\": \"co pozostało\"}."
      }]
    }]
  }
}
```

### Agent-based hook (subagent weryfikuje)
```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "agent",
        "prompt": "Uruchom testy i sprawdź czy przechodzą. Jeśli nie, zwróć {\"ok\": false}."
      }]
    }]
  }
}
```

To jest potężniejsze niż Copilot hooks — możesz użyć LLM do weryfikacji warunków!
