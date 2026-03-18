# Kontekst i prompty

> Źródło: https://code.visualstudio.com/docs/copilot/chat/copilot-chat

## 🎯 Cele modułu

- Zrozumieć różnicę między `@workspace` a `#file` i wiedzieć kiedy co użyć.
- Opanować iteracyjne udoskonalanie promptów (v1 → v2 → v3).
- Poznać techniki promptowania: few-shot, chain-of-thought, persona.
- Napisać test integracyjny z kontrolowanym kontekstem.

---

## 📚 Teoria

### `@workspace` vs `#file`

| Modyfikator | Zakres | Kiedy? | Ryzyko |
|-------------|--------|--------|--------|
| `@workspace` | Cały projekt | Pytania o architekturę, zmiany w wielu plikach, dokumentacja | Token window — w dużym projekcie Copilot przycina kontekst |
| `#file:nazwa.java` | Jeden plik | Refaktor metody, testy jednostkowe, Javadoc | Nie widzi zależności z innych plików |
| Zaznaczenie + `Ctrl+I` | Fragment kodu | Szybka zmiana, wyjaśnienie bloku | Jeszcze węższy kontekst |

**Zasada:** Używaj najwęższego kontekstu, który wystarcza do zadania.

### Token window — co to i dlaczego to ważne

Model przetwarza ograniczoną liczbę tokenów. Gdy projekt jest duży i użyjesz `@workspace`, Copilot sam decyduje co obciąć. Skutki:
- pomija ważne klasy/interfejsy,
- daje ogólnikowe odpowiedzi,
- „halucynuje" nazwy metod.

**Optymalizacja:**
1. Używaj `#file` gdy wystarczy jeden plik.
2. Otwieraj w edytorze pliki, które mają być w kontekście.
3. `.copilotignore` — wyklucz foldery nieistotne (`build/`, `target/`, `node_modules/`).
4. Dziel duże klasy — mniejsze pliki = mniej szumu.

### Iteracyjne promptowanie

Rzadko idealny prompt powstaje za pierwszym razem. Schemat pracy:

```
Prompt v1 (ogólny) → Analiza wyniku → Prompt v2 (precyzyjniejszy) → ... → Prompt vN (idealny)
```

**Każda iteracja dodaje:** kontekst, ograniczenia, format wyjścia, przykłady.

### Techniki promptowania

| Technika | Opis | Przykład |
|----------|------|---------|
| **Persona / Rola** | Nadaj Copilotowi rolę eksperta | „Jako architekt Spring Boot..." |
| **Few-shot** | Podaj 1-2 przykłady wejścia → wyjścia | „Wzoruj się na `OwnerController` — zrób analogicznie dla Vet" |
| **Chain of Thought** | Proś o krok po kroku | „Krok 1: przeanalizuj zależności. Krok 2: zaproponuj interfejs. Krok 3: implementuj." |
| **Ograniczenia negatywne** | Powiedz czego NIE robić | „Nie używaj Lombok. Nie dodawaj nowych zależności." |
| **Format wyjścia** | Określ czego oczekujesz | „Zwróć tabelę Markdown z kolumnami: klasa, odpowiedzialność, zależności" |

### `.copilotignore`

Plik analogiczny do `.gitignore` — wyklucza pliki/foldery z kontekstu Copilota:

```
# .copilotignore
target/
build/
*.log
docs/
```

---

## 🔗 Żywy przykład z tego repo

W `.github/prompts/` masz 3 prompt files o różnym poziomie złożoności:
- `refiner.prompt.md` — prosty, bez YAML frontmatter
- `prompt-refiner.prompt.md` — z frontmatter: `agent: "ask"`, `argument-hint`
- `method-deep-dive.prompt.md` — rozbudowany: `agent: "agent"`, sekcje analizy, diagram Mermaid

Porównaj je — zobaczysz jak format i precyzja promptu wpływają na jakość wyniku.

---

## 📝 Ćwiczenia

| # | Ćwiczenie | Czas |
|---|-----------|------|
| ex_05 | `@workspace` vs `#file` — kiedy co | ~10 min |
| ex_06 | Iteracja promptu v1 → v2 → v3 | ~10 min |
| 🅱️ ex_06b | Few-shot / CoT / Role — techniki promptowania | ~10 min |
| 🅱️ ex_06c | Characterization Test — bezpieczny refaktor legacy | ~10 min |
| ex_07 | Test integracyjny z kontrolowanym kontekstem | ~10 min |

Pliki ćwiczeń: `exercises/`
