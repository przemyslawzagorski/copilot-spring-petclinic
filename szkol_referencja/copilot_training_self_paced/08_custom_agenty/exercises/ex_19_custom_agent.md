# Ex 19: Twój pierwszy custom agent

> Faza 6 · ~10 min · Moduł 08

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

---

## Krok 3: Zabierz agenta ze sobą (poziom użytkownika)

Agent w `.github/agents/` jedzie razem z repo — cały zespół go ma, ale znika,
gdy przejdziesz do innego projektu. Agenta **osobistego** trzymasz u siebie:

| Narzędzie | Ścieżka |
|---|---|
| VS Code / Copilot CLI | `~/.copilot/agents/` |
| Visual Studio (Windows) | `%USERPROFILE%\.github\agents\` |

W VS Code dodatkowe lokalizacje wskażesz ustawieniem `chat.agentFilesLocations`.

**Ćwiczenie:** skopiuj `reviewer.agent.md` do katalogu użytkownika, zmień w nim
`name` na `reviewer` (bez zmian) i otwórz **inny** projekt. Agent nadal jest na
liście.

> **Przy konflikcie nazw wygrywa agent użytkownika** — przesłania tego z repo.
> To wygodne, ale bywa mylące w zespole: kolega z tą samą nazwą agenta lokalnie
> dostanie inne wyniki niż Ty, mimo tego samego repo. Nazywaj osobiste agenty
> inaczej niż zespołowe.

## Podział, który warto zapamiętać

| Poziom | Do czego |
|---|---|
| Repo (`.github/agents/`) | Standard zespołu — review, konwencje, architektura projektu |
| Użytkownik | Twój sposób pracy — przenośny między projektami |

**Więcej:** `08_custom_agenty/EXERCISES.md` · odpowiednik dla Claude Code
w [CLAUDE_CODE.md](../CLAUDE_CODE.md)
