# Ex 21d: Scoped Hooks (Preview) — Strict Formatter Agent

> Bonus · ~8 min · Między ex_21 a ex_22

**Po co:** Agent może mieć własne hooki w frontmatter. Hook działa tylko, gdy ten agent jest aktywny.

## Co zrobić

1. Włącz ustawienie VS Code:

```text
chat.useCustomAgentHooks = true
```

2. Utwórz `.github/agents/strict-formatter.agent.md`:

```markdown
---
name: Strict Formatter
description: Agent that auto-formats code after every edit
tools: [edit, read, search]
hooks:
  PostToolUse:
    - type: command
      command: "echo formatting-after-edit"
---

You are a code editing agent.
After making changes, ensure formatting command runs via hook.
```

3. Przetestuj:

```text
Wybierz agenta `Strict Formatter` i poproś o małą zmianę w pliku Java.
Sprawdź, czy po edycji uruchomił się hook PostToolUse.
```

## Spodziewany wynik

- Hook `PostToolUse` uruchamia się tylko dla agenta `Strict Formatter`.
- Inne agenty nie uruchamiają tego hooka.

## Checklist walidacji

- Ustawienie `chat.useCustomAgentHooks` jest włączone.
- W `.agent.md` istnieje sekcja `hooks`.
- Hook działa po narzędziu edycji (`edit`) i nie działa poza tym agentem.

**Uwaga:** To funkcja Preview. Zachowanie może się różnić między wersjami VS Code/Copilot Chat.

**Więcej:** `04_hooks_i_guardrails/EXERCISES.md`
