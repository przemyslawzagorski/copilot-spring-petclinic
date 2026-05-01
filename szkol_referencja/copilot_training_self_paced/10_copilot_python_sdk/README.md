# Copilot Python SDK

> **Public Preview.** API może się zmienić w niekompatybilny sposób. Materiał aktualny na grudzień 2025 (`github-copilot-sdk` ~0.3.x, `@github/copilot` 1.0.40-3).

## 🎯 Cele modułu

- Zrozumieć czym różni się **Copilot SDK** od Copilot w VS Code i Copilot CLI.
- Zainstalować i autoryzować SDK w środowisku Python (3.11+).
- Napisać pierwszą sesję `CopilotClient` z odpowiedzią asynchroniczną.
- Wykorzystać SDK do automatyzacji zadań w repozytorium PetClinic.
- Włączyć **streaming** odpowiedzi.
- Zarejestrować **własne narzędzie** (custom tool) z walidacją Pydantic.

---

## 📚 Teoria

### Czym jest Copilot SDK?

**GitHub Copilot SDK** to programistyczny interfejs do tego samego silnika agentowego, na którym działa Copilot CLI. Zamiast pracować w czacie VS Code lub w terminalu, wywołujesz Copilota **z własnego kodu Python** i obsługujesz odpowiedzi w pętli `async/await`.

```
┌──────────────────┐                       ┌────────────────────┐
│  Twoja aplikacja │ ── JSON-RPC (stdio) ─▶│ Copilot CLI server │ ──▶ Modele LLM
│   (Python)       │ ◀──── eventy ──────── │  (proces dziecko)  │
└──────────────────┘                       └────────────────────┘
```

- SDK uruchamia w tle proces `copilot` (CLI jest **bundled** z pakietem PyPI — nie trzeba instalować osobno).
- Komunikacja przez **JSON-RPC** po stdio.
- Wszystkie zdarzenia (`AssistantMessageData`, `SessionIdleData`, `AssistantMessageDeltaData`, ...) dostajesz w handlerze `session.on(...)`.

### Kiedy używać SDK?

| Scenariusz | Narzędzie |
|------------|-----------|
| Praca interaktywna w edytorze | VS Code Copilot Chat |
| Skrypty ad-hoc w terminalu | Copilot CLI |
| **Batch/automatyzacja, własne UI, integracje, CI/CD** | **Copilot SDK** |
| Złożone narzędzia z walidacją typów | SDK + `@define_tool` |

Typowe zastosowania:
- Generowanie raportów z code review na PR (CI).
- Bot do triażu issue w GitHub Actions.
- Interaktywne CLI nad własną domeną biznesową.
- Pipeline do migracji kodu między wersjami frameworków.
- Integracja z własnym narzędziem przez tool calling.

### Architektura SDK (skrót)

| Komponent | Rola |
|-----------|------|
| `CopilotClient` | Manager procesu CLI; tworzy sesje. Async context manager. |
| `Session` | Pojedynczy „wątek" rozmowy. Wysyłasz `await session.send(...)`. |
| `PermissionHandler` | Decyzja przed każdym wywołaniem narzędzia. `approve_all` w nauce, custom w produkcji. |
| `@define_tool` + Pydantic | Definicja własnego narzędzia z auto-generowanym JSON schema. |
| `streaming=True` | Odpowiedź przychodzi po kawałku w `AssistantMessageDeltaData`. |
| `hooks={...}` | Wpięcie się w lifecycle (`on_pre_tool_use`, `on_session_start`, ...). |

### Autentykacja

SDK próbuje kolejno:

1. `github_token` jawnie podany w `SubprocessConfig`.
2. Zmienne środowiskowe: `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN`.
3. Zalogowany użytkownik z `copilot` CLI (token zapisany lokalnie).
4. **BYOK** (Bring Your Own Key) — dowolny endpoint OpenAI-compatible (Azure OpenAI, Ollama, Anthropic).

**Wymagana subskrypcja Copilot** (plan free wystarczy do nauki) chyba że używasz BYOK.

### Modele

Najczęściej używane: `gpt-5`, `claude-sonnet-4.5`. Pełną listę dostarczy `await client.list_models()`.

---

## 🛠 Wymagania techniczne

- **Python 3.11+** (sprawdź `python --version`).
- **Konto GitHub z aktywnym Copilot** (free tier OK do ćwiczeń).
- Dostęp do internetu (CLI nawiązuje połączenie z serwerem modeli).
- (Opcjonalnie) Wirtualne środowisko `.venv` w workspace — w tym repo już istnieje.

---

## 📝 Ćwiczenia

| # | Ćwiczenie | Czas |
|---|-----------|------|
| ex_25 | Setup SDK i autoryzacja | ~15 min |
| ex_26 | Pierwsza sesja: hello chat | ~15 min |
| ex_27 | PetClinic assistant — automatyzacja w repo | ~25 min |
| 🅱️ ex_28 | Bonus: streaming odpowiedzi | ~15 min |
| 🅱️ ex_29 | Bonus: własne narzędzie (custom tool) | ~25 min |

Pliki: [exercises/](exercises/). Index: [EXERCISES.md](EXERCISES.md).

**Kolejność:** ex_25 → ex_26 → ex_27 → (ex_28) → (ex_29).

---

## 🔗 Materiały dodatkowe

- **Repo SDK:** <https://github.com/github/copilot-sdk>
- **README pakietu Python:** <https://github.com/github/copilot-sdk/tree/main/python>
- **Sample chat.py:** <https://github.com/github/copilot-sdk/blob/main/python/samples/chat.py>
- **Testy e2e (wzorcowe użycia):** <https://github.com/github/copilot-sdk/tree/main/python/e2e>
- **Custom instructions dla Copilota o SDK:** <https://github.com/github/awesome-copilot/blob/main/instructions/copilot-sdk-python.instructions.md>
- **Cookbook recipes:** <https://github.com/github/awesome-copilot/blob/main/cookbook/copilot-sdk>

---

## ⚠️ Uwaga o stanie API

Pakiet jest w **public preview**. Sprawdź `pip show github-copilot-sdk`. Jeśli przykłady przestają działać — najpierw porównaj wersję z README repo SDK i ewentualnie odśwież ćwiczenia.
