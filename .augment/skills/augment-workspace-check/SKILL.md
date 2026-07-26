---
name: augment-workspace-check
description: Sprawdza konfigurację Augment/Auggie w tym repozytorium: rules, agents, skills, commands, hooks, permissions i ignore. Użyj przy konfiguracji lub diagnostyce workspace.
---

# Kontrola workspace Augment

1. Sprawdź, czy istnieją `.augment/settings.json` i `.augmentignore`.
2. Zweryfikuj JSON ustawień oraz obecność `toolPermissions` i hooków.
3. Wypisz reguły z `.augment/rules/` i ich typy.
4. Wypisz subagentów z `.augment/agents/` wraz z ograniczeniami narzędzi.
5. Sprawdź natywne skille `.augment/skills/` i współdzielone `.claude/skills/`.
6. Sprawdź komendy `.augment/commands/` i kolizje z komendami wbudowanymi.
7. Potwierdź, że repozytoryjne ustawienia nie zawierają MCP ani sekretów.
8. Zwróć raport PASS/FAIL z rekomendacją dla każdego problemu.

Nie modyfikuj plików podczas tej kontroli.