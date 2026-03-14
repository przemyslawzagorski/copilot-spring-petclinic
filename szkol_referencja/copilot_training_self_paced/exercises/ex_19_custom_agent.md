# Ex 19: Twój pierwszy custom agent

> Faza 6 · ~10 min · Źródło: moduł 07

**Po co:** Agent to "persona" Copilota z jasnym zakresem i ograniczeniami. Zamiast ogólnego asystenta — specjalista.

## Co zrobić

1. Utwórz plik `.github/agents/reviewer.agent.md`:

```markdown
---
name: reviewer
description: "Agent do code review kontrolerów Spring"
tools: [read, search]
---

Jesteś surowym recenzentem kodu kontrolerów Spring MVC.

## Zakres
- Analizujesz WYŁĄCZNIE pliki *Controller.java
- Sprawdzasz: walidację danych, obsługę błędów, nazewnictwo, separation of concerns

## Czego NIE robisz
- Nie piszesz kodu
- Nie zmieniasz plików
- Nie analizujesz testów ani konfiguracji

## Format odpowiedzi
Tabela: plik | problem | severity (Critical/Major/Minor) | sugestia
```

2. W Copilot Chat wybierz agenta `reviewer` w pickerze i wpisz:

```
Zrób review OwnerController.java
```

**Spodziewany wynik:** Tabela z uwagami dotyczącymi kontrolera — np. brak `@Valid`, za duża odpowiedzialność metody.

**Więcej:** `07_module_07/EXERCISES.md` — ćwiczenie 1
