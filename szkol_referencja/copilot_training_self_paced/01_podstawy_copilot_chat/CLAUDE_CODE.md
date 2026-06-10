# Moduł 01 — Podstawy: adaptacja dla Claude Code

> Oryginalne ćwiczenia (`exercises/`) są dla GitHub Copilot w VS Code.
> Ten plik zawiera ich odpowiedniki dla Claude Code.

---

## Kluczowe różnice w interfejsie

| GitHub Copilot | Claude Code |
|---|---|
| Chat view (Ctrl+Alt+I) | Terminal: `claude` / VSCode Extension |
| Inline Chat (Ctrl+I) | Opisz zmianę w prompcie lub zaznacz kod w VSCode |
| Quick Chat (Ctrl+Shift+Alt+L) | `/btw pytanie` — szybkie pytanie bez dodawania do historii |
| Tryb Agent (edytuje pliki) | Domyślny tryb — Claude Code zawsze może edytować |
| Tryb Ask (tylko odpowiada) | Brak trybu — wszystkie narzędzia zawsze dostępne |
| Tryb Plan (plan → potwierdzenie) | `/plan` lub `claude --plan` — plan przed implementacją |
| `@workspace` | Niepotrzebny — Claude Code widzi pliki bezpośrednio |
| `#file:nazwa.java` | Podaj ścieżkę w prompcie: `src/main/java/.../OwnerController.java` |

---

## Ex 01 (CC): Zapytaj Claude Code o projekt

**Odpowiednik ex_01_chat_o_projekcie.md**

**W terminalu:**
```
claude
```

Wpisz:
```
Jaki framework używa ten projekt? Jakie są główne encje domenowe? Odpowiedz w 5 punktach.
```

Claude Code sam przeszuka pliki projektu (`pom.xml`, kod źródłowy) — nie potrzeba `@workspace`.

**Spodziewany wynik:** Claude wymieni Spring Boot, H2/PostgreSQL, Thymeleaf i encje: Owner, Pet, Vet, Visit. Odwoła się do konkretnych plików.

---

## Ex 02 (CC): Refaktoryzacja metody

**Odpowiednik ex_02_inline_refaktor.md**

W Claude Code wpisz:
```
W pliku src/main/java/org/springframework/samples/petclinic/vet/VetController.java
znajdź metodę showVetList i zaproponuj refaktoryzację — zastosuj Java records gdzie możliwe.
```

Lub w VSCode zaznacz metodę i użyj skrótu Claude Code Extension (sprawdź w palecie poleceń: `Ctrl+Shift+P` → "Claude").

**Różnica:** Nie ma Ctrl+I — ale Claude Code może edytować dowolny plik na podstawie opisu.

---

## Ex 02b (CC): Edycja wielu plików

**Odpowiednik ex_02b_multi_file_editing.md**

Claude Code domyślnie może edytować wiele plików. Wpisz:
```
Dodaj pole "email" do klasy Owner — zaktualizuj encję, formularz HTML i testy.
```

Claude Code zaplanuje zmiany, pokaże co zmieni, i wykona edycje po potwierdzeniu.

---

## Ex 03 (CC): Generuj Javadoc

**Odpowiednik ex_03_javadoc_inline.md**

```
Dodaj Javadoc po polsku do wszystkich publicznych metod w klasie VetController.
Javadoc powinien opisywać cel metody i parametry.
```

---

## Ex 03b (CC): Podpowiedzi kodu (Tab completion)

**Odpowiednik ex_03b_next_edit_suggestions.md**

Claude Code nie ma Tab completion jak Copilot. Zamiast tego:
- Użyj VSCode Extension z Claude Code — ma wsparcie dla podpowiedzi inline
- Lub poproś o wielokrokową edycję: `Kontynuuj ten wzorzec dla pozostałych metod`

---

## Ex 04 (CC): Terminal przez Claude

**Odpowiednik ex_04_terminal_przez_chat.md**

Claude Code ma bezpośredni dostęp do terminala (narzędzie `Bash`).

```
Uruchom testy projektu i pokaż mi wyniki. Jeśli coś nie przechodzi, wyjaśnij dlaczego.
```

Claude wykona `./mvnw test` i przeanalizuje wyniki — nie trzeba przełączać się do terminala.

---

## Żywe przykłady Claude Code w tym repo

| Plik | Co to? |
|---|---|
| `CLAUDE.md` | Instrukcje projektu (odpowiednik copilot-instructions.md) |
| `.claude/agents/mentor.md` | Subagent mentor |
| `.claude/settings.json` | Hooki i uprawnienia |

Zacznij od: `szkol_referencja/claude_code_guide/README.md`
