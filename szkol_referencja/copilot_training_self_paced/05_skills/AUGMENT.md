# Moduł 05 - Skills: adaptacja dla Augmenta

> Augment używa standardu Agent Skills i potrafi czytać także skille z
> `.claude/skills/`. Nie trzeba kopiować istniejących materiałów.

## Lokalizacje i pierwszeństwo

Skille mogą być przechowywane w `.augment/skills/`, `.claude/skills/` i
`.agents/skills/`. Repozytorium dodaje natywny przykład:

```text
.augment/skills/augment-workspace-check/SKILL.md
```

Nazwa w frontmatterze musi odpowiadać nazwie katalogu. Wbudowana slash command
ma pierwszeństwo nad skillem o tej samej nazwie.

## Ex 12 (Auggie): pierwszy skill

1. Uruchom `/skills` i znajdź współdzielone oraz natywne skille.
2. Uruchom `/augment-workspace-check`.
3. Utwórz `.augment/skills/git-summary/SKILL.md`:

```markdown
---
name: git-summary
description: Read-only podsumowanie zmian Git. Użyj przed przygotowaniem commita.
---

Sprawdź git status, git diff --stat i ostatnie pięć commitów.
Nie zmieniaj plików. Zaproponuj conventional commit.
```

4. Rozpocznij nową sesję i wywołaj `/git-summary`.

## Ex 12b (Auggie): matryca decyzji

| Sytuacja | Augment |
|---|---|
| Wiedza i konwencje | rule albo `CLAUDE.md` |
| Wielokrotna procedura | skill |
| Jawny skrót z argumentami | custom command |
| Izolowana rola i kontekst | subagent |
| Deterministyczne zdarzenie | hook |

Skill opisuje procedurę i wiedzę. Uprawnienia egzekwuj na poziomie subagenta,
permissions lub hooków, a nie samą instrukcją tekstową skilla.