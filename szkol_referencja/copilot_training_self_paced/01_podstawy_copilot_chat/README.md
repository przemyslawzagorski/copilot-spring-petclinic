# Podstawy Copilot Chat

> Źródło: https://code.visualstudio.com/docs/copilot/chat/copilot-chat

## 🎯 Cele modułu

- Poznać 3 sposoby interakcji z Copilotem: Chat view, Inline Chat, Quick Chat.
- Zrozumieć różnicę między 3 wbudowanymi agentami: Agent, Ask, Plan.
- Użyć `@workspace` i Inline Chat do pracy z kodem projektu.
- Uruchamiać polecenia terminalowe przez Copilot Chat.

---

## 📚 Teoria

### Trzy interfejsy czatu

| Interfejs | Skrót | Do czego? |
|-----------|-------|-----------|
| **Chat view** | `Ctrl+Alt+I` | Główne okno — wieloturowe rozmowy, edycja plików, uruchamianie narzędzi |
| **Inline Chat** | `Ctrl+I` | Szybka zmiana w zaznaczonym fragmencie kodu |
| **Quick Chat** | `Ctrl+Shift+Alt+L` | Szybkie pytanie bez otwierania panelu bocznego |

### Trzy wbudowane agenty (tryby)

W Chat view u góry okna wybierasz tryb pracy:

| Agent | Co robi? | Kiedy używać? |
|-------|----------|---------------|
| **Agent** | Autonomicznie edytuje pliki, uruchamia terminal, używa narzędzi | Większość zadań — domyślny tryb |
| **Ask** | Tylko odpowiada, nie modyfikuje niczego | Pytania o kod, architekturę, wyjaśnienia |
| **Plan** | Tworzy plan krok po kroku, czeka na potwierdzenie | Złożone zmiany — chcesz zobaczyć plan przed wykonaniem |

> **Uwaga:** „Edit mode" / „Panel Edits" (Ctrl+Shift+I) **nie istnieje** od marca 2025. Cała funkcjonalność edycji wielu plików jest teraz w trybie **Agent**.

### Kontekst: co Copilot „widzi"

Copilot automatycznie korzysta z:
- otwartego pliku i zaznaczenia,
- plików w projekcie (gdy użyjesz `@workspace`),
- historii rozmowy w bieżącej sesji.

Ręcznie możesz dodać kontekst przez:
- `@workspace` — cały projekt (Copilot wybiera relevantne pliki),
- `#file:nazwa.java` — konkretny plik,
- zaznaczenie kodu + `Ctrl+I` — wybrany fragment.

### Przydatne komendy w Chat

- `/explain` — wyjaśnij zaznaczony kod
- `/fix` — napraw błąd
- `/tests` — wygeneruj testy
- `/doc` — dodaj dokumentację

---

## 🔗 Żywe przykłady w tym repo

W tym repozytorium masz już skonfigurowane elementy Copilota, które zobaczysz w kolejnych modułach:

| Plik | Co to? |
|------|--------|
| `.github/copilot-instructions.md` | Globalne reguły dla Copilota — 6 zasad projektu |
| `.github/agents/mentor.agent.md` | Prosty agent — mentor szkolenia |
| `.github/hooks/06-motivator.json` | Hook PostToolUse — losowa wiadomość po edycji pliku |

---

## 📝 Ćwiczenia

| # | Ćwiczenie | Czas |
|---|-----------|------|
| ex_01 | Chat o projekcie (`@workspace`) | ~5 min |
| ex_02 | Inline edit — refaktor metody (Ctrl+I) | ~5 min |
| 🅱️ ex_02b | Edycja wielu plików w trybie Agent | ~10 min |
| ex_03 | Generuj Javadoc inline | ~5 min |
| 🅱️ ex_03b | Next Edit Suggestions — Tab prediction | ~5 min |
| ex_04 | Terminal przez chat | ~5 min |

Pliki ćwiczeń: `exercises/`
