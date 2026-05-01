# Agent Skills — specjalistyczne umiejętności Copilota

> Źródło: https://code.visualstudio.com/docs/copilot/customization/agent-skills
> Standard: https://agentskills.io/

## 🎯 Cele modułu

- Zrozumieć czym jest Skill i czym się różni od Prompt File, Instruction, Hook i Agent.
- Stworzyć własny skill w formacie `SKILL.md` zgodny z oficjalną dokumentacją.
- Przetestować auto-load i wywołanie przez `/slash` command.
- Nauczyć się projektować skille z zasobami (skrypty, szablony, przykłady).

---

## 📚 Teoria

### Czym jest Agent Skill?

**Skill to folder z plikiem `SKILL.md`** zawierający instrukcje, procedury, skrypty i zasoby, które Copilot wczytuje gdy są potrzebne do wykonania zadania.

Kluczowa różnica: skill to **nie prompt** i **nie instrukcja**. Skill to kompletna „umiejętność" — procedura krok po kroku, często z towarzyszącymi plikami (szablony, skrypty, przykłady).

### Jak Copilot używa skilli — 3 poziomy ładowania

```
1. Discovery    → Copilot czyta TYLKO name + description z frontmatter
2. Instructions → Copilot wczytuje body SKILL.md (procedury, kroki)
3. Resources    → Copilot sięga po pliki w folderze skilla (skrypty, szablony)
```

Dzięki temu możesz mieć **dziesiątki skilli** bez obciążania kontekstu — Copilot ładuje tylko to, co jest potrzebne.

### Gdzie trzymać skille

| Typ | Lokalizacja | Zakres |
|---|---|---|
| **Projektowy** | `.github/skills/<nazwa>/SKILL.md` | Współdzielony w repo |
| **Osobisty** | `~/.copilot/skills/<nazwa>/SKILL.md` | Tylko Twój, we wszystkich projektach |
| **Alternatywne** | `.claude/skills/` lub `.agents/skills/` | Kompatybilne z innymi agentami |

> **Tip monorepo:** Włącz `chat.useCustomizationsInParentRepositories`, aby skille z katalogu nadrzędnego były widoczne.
> **Tip dodatkowe lokalizacje:** Setting `chat.agentSkillsLocations` pozwala wskazać dowolne foldery.

### Struktura folderu skilla

```
.github/skills/
└── project-versions/          ← nazwa folderu = name w frontmatter
    ├── SKILL.md               ← WYMAGANY — definicja skilla
    ├── check-versions.sh      ← opcjonalny skrypt pomocniczy
    ├── version-template.md    ← opcjonalny szablon
    └── examples/              ← opcjonalne przykłady
        └── sample-output.md
```

### Format pliku SKILL.md

```markdown
---
name: project-versions
description: "Raportuje wersje Java, Spring Boot i zależności z pom.xml. Użyj gdy pytasz o wersje, stack technologiczny lub zależności."
argument-hint: "[opcjonalnie: nazwa zależności do sprawdzenia]"
---

# Instrukcje skilla

Czytaj pom.xml i podaj wersje w tabeli Markdown...
(dalsze instrukcje, kroki, przykłady)
```

#### Pola frontmatter

| Pole | Wymagane | Opis |
|---|---|---|
| `name` | **Tak** | Unikalna nazwa, lowercase z myślnikami. **Musi = nazwa folderu**. Max 64 znaki. |
| `description` | **Tak** | Co skill robi i kiedy go użyć. Max 1024 znaki. **Im lepszy opis, tym lepszy auto-load.** |
| `argument-hint` | Nie | Podpowiedź widoczna w polu chat po wybraniu `/skill-name`. |
| `user-invocable` | Nie | `true` (domyślnie) = widoczny w menu `/`. `false` = ukryty, ale auto-load działa. |
| `disable-model-invocation` | Nie | `true` = TYLKO ręcznie przez `/`. `false` (domyślnie) = auto-load + ręcznie. |

#### Kombinacje widoczności

| user-invocable | disable-model-invocation | Efekt |
|---|---|---|
| `true` (domyślne) | `false` (domyślne) | Widoczny w `/` + auto-load — **najczęstszy wariant** |
| `false` | `false` | Ukryty w `/`, ale model go ładuje gdy pasuje — **wiedza tła** |
| `true` | `true` | Widoczny w `/`, ale TYLKO ręcznie — **na żądanie** |
| `false` | `true` | Wyłączony |

#### Body — co pisać w instrukcjach

- Co skill pomaga osiągnąć
- Kiedy go używać (a kiedy NIE)
- Procedura krok po kroku
- Przykłady wejścia i wyjścia
- Referencje do plików w folderze skilla: `[skrypt](./check-versions.sh)`

### Wywoływanie skilli

**Slash command:** Wpisz `/` w Copilot Chat → wybierz skill z listy → dodaj kontekst.

```
/project-versions
/webapp-testing for the login page
/github-actions-debugging PR #42
```

**Auto-load:** Jeśli `disable-model-invocation` jest `false`, Copilot sam wczyta skill gdy uzna, że pasuje do Twojego pytania.

**Tip:** Wpisz `/skills` w chat, aby otworzyć menu Configure Skills.

### Generowanie skilla za pomocą AI

Zamiast pisać od zera:
- `/create-skill` + opis czego chcesz → Copilot zadaje pytania i generuje `SKILL.md`
- Po sesji debugowania: *"create a skill from how we just debugged that"* → Copilot zamienia wielokrokową procedurę w reużywalny skill

---

## 🔑 Skill vs Prompt File vs Instruction vs Hook vs Agent

To jest **najważniejsza tabela tego modułu**. Musisz to rozumieć, żeby wiedzieć kiedy czego użyć.

| | **Skill** | **Prompt File** | **Instruction** | **Hook** | **Agent** |
|---|---|---|---|---|---|
| **Plik** | `.github/skills/*/SKILL.md` | `.github/prompts/*.prompt.md` | `*.instructions.md` | `.github/hooks/*.json` | `.github/agents/*.agent.md` |
| **Kiedy działa** | Auto-load LUB `/slash` | Gdy użytkownik jawnie wybierze `/` | Zawsze (lub via `applyTo` glob) | Automatycznie na zdarzeniu agenta | Gdy przełączysz agenta |
| **Zawiera zasoby** | **Tak** (skrypty, szablony, przykłady) | Nie | Nie | Tak (skrypt shell/python) | Nie |
| **Wykonuje kod** | Agent może użyć skryptów z folderu | Nie | Nie | **Tak** (wymusza deterministycznie) | Nie |
| **Portable** | **Tak** (agentskills.io standard) | Tylko VS Code | Tylko VS Code | Tylko VS Code | Tylko VS Code |
| **Zastosowanie** | Specjalistyczna procedura wielokrokowa | Szablon promptu do powtórzenia | Stałe reguły kodowe | Enforcement / walidacja | Persona z ograniczonym scope |

### Kiedy co wybrać — zasada kciuka

```
"Chcę żeby Copilot ZAWSZE pamiętał konwencję"     → Instruction (.instructions.md)
"Chcę reużywalny szablon do odpalenia ręcznie"     → Prompt File (.prompt.md)
"Chcę specjalistyczną procedurę z plikami"         → Skill (SKILL.md)
"Chcę ZABLOKOWAĆ / WYMUSIĆ coś deterministycznie" → Hook (.json + skrypt)
"Chcę ograniczoną personę z jasnym scope"          → Agent (.agent.md)
```

### Analogia do życia codziennego

| Koncept | Analogia |
|---|---|
| Instruction | Tabliczka „W biurze mówimy po polsku" — obowiązuje zawsze |
| Prompt File | Formularz urzędowy — wypełniasz gdy potrzebujesz |
| Skill | Podręcznik procedury awaryjnej — czytasz gdy jest pożar |
| Hook | Bramka na lotnisku — MUSISZ przejść, nie da się ominąć |
| Agent | Specjalista (np. audytor) — przychodzi gdy go wezwiesz |

---

## 💡 Przykłady skilli dla Spring PetClinic

### Przykład 1: Skill do raportowania wersji

```
.github/skills/project-versions/
└── SKILL.md
```

```markdown
---
name: project-versions
description: "Raportuje wersje Java, Spring Boot i główne zależności projektu. Użyj gdy ktoś pyta o stack technologiczny, wersje zależności lub kompatybilność."
argument-hint: "[opcjonalnie: nazwa konkretnej zależności]"
---

# Raport wersji projektu

## Procedura

1. Otwórz `pom.xml` w katalogu głównym projektu.
2. Odczytaj:
   - Wersję Java z `<java.version>` w `<properties>`
   - Wersję Spring Boot z `<parent><version>`
   - Listę zależności z `<dependencies>` — podaj nazwę artefaktu i wersję
3. Sprawdź datę ostatniego commita: `git log -1 --format="%cd" --date=short`
4. Zwróć wynik w tabeli Markdown:

## Format wyjścia

| Komponent | Wersja |
|---|---|
| Java | (z pom.xml) |
| Spring Boot | (z parent) |
| spring-boot-starter-web | (wersja) |
| ... | ... |
| Ostatni commit | (data) |
```

### Przykład 2: Skill do testowania webowych endpoints

```
.github/skills/webapp-testing/
├── SKILL.md
├── test-template.java
└── examples/
    └── controller-test-example.java
```

```markdown
---
name: webapp-testing
description: "Generuje i uruchamia testy integracyjne Spring MVC kontrolerów z MockMvc. Użyj gdy chcesz przetestować endpoint HTTP, formularz lub REST API."
argument-hint: "[klasa kontrolera] [opcjonalnie: konkretna metoda]"
---

# Testowanie kontrolerów Spring MVC

## Kiedy użyć
- Testujesz endpoint HTTP (GET/POST/PUT/DELETE)
- Chcesz sprawdzić walidację formularzy
- Potrzebujesz test integracyjny z MockMvc

## Procedura
1. Zidentyfikuj kontroler i endpoint do przetestowania
2. Użyj szablonu z [test-template.java](./test-template.java)
3. Dla każdego endpointu utwórz test:
   - Happy path (HTTP 200/302)
   - Walidacja błędów (HTTP 400)
   - Brak danych (HTTP 404)
4. Uruchom: `./mvnw test -pl . -Dtest=NazwaTestuKontrolera`

## Konwencje
- Klasa testowa: `{Controller}IntegrationTest`
- Metoda testowa: `test{Endpoint}_{scenariusz}`
- Użyj `@WebMvcTest` + `@MockitoBean` dla zależności (Spring Boot 4.x — `@MockBean` jest usunięte)

## Przykład
Zobacz [controller-test-example.java](./examples/controller-test-example.java)
```

### Przykład 3: Skill do debugowania GitHub Actions

```
.github/skills/github-actions-debugging/
├── SKILL.md
└── common-errors.md
```

```markdown
---
name: github-actions-debugging
description: "Diagnozuje i naprawia problemy w GitHub Actions workflow. Użyj gdy pipeline CI/CD nie działa, build fail, lub potrzebujesz pomocy z YAML workflow."
argument-hint: "[numer PR lub opis problemu]"
---

# Debugowanie GitHub Actions

## Procedura diagnostyczna
1. Sprawdź logi ostatniego uruchomienia workflow
2. Zidentyfikuj step, który failuje
3. Porównaj z listą typowych błędów w [common-errors.md](./common-errors.md)
4. Zaproponuj fix z wyjaśnieniem

## Typowe kategorie problemów
- Dependency resolution (cache, wersje)
- Environment (zmienne, sekrety)
- Permissions (token, GITHUB_TOKEN scope)
- Timing (timeout, race condition)
```

---

## ✅ Best Practices

1. **Jeden skill = jedna umiejętność.** Nie rób mega-skilla „do wszystkiego". Lepiej 5 małych niż 1 duży.
2. **Description decyduje o auto-load.** Pisz konkretnie co skill robi I kiedy go użyć. Złe: *"Pomaga z testami"*. Dobre: *"Generuje testy integracyjne MockMvc dla kontrolerów Spring. Użyj gdy testujesz endpoint HTTP."*
3. **Nazwa folderu = name.** Jeśli folder to `webapp-testing/`, to `name: webapp-testing`. Inaczej skill nie zadziała.
4. **Referencje relatywne.** W body odwołuj się do plików w folderze `[szablon](./template.java)` — Copilot wczyta je gdy będą potrzebne.
5. **Nie powtarzaj instrukcji.** Jeśli reguła dotyczy ZAWSZE (np. „używaj JUnit 5"), to daj ją do `.instructions.md`, nie do skilla.
6. **Shared skills — weryfikuj!** Przed użyciem cudzych skilli z [awesome-copilot](https://github.com/github/awesome-copilot) lub [anthropics/skills](https://github.com/anthropics/skills) — przeczytaj `SKILL.md` i sprawdź bezpieczeństwo.

## ⚠️ Common Pitfalls

| Błąd | Co się stanie | Jak naprawić |
|---|---|---|
| `name` ≠ nazwa folderu | Skill nie zostanie załadowany | Zmień name lub nazwę folderu |
| Brak `description` | Copilot nie wie kiedy użyć skilla | Dodaj opis z "Użyj gdy..." |
| Zbyt ogólny opis | Auto-load wczytuje skill bez potrzeby, zjada kontekst | Bądź konkretny w description |
| Brak sekcji „kiedy NIE użyć" | Skill odpala się w złym kontekście | Dodaj wykluczenia do body |
| Zasoby poza folderem skilla | Copilot ich nie znajdzie | Trzymaj wszystko w folderze skilla |
| Zbyt długi SKILL.md | Zjada kontekst | Przenieś szczegóły do osobnych plików, referencuj je |

---

## 🔗 Zasoby

- [Oficjalna dokumentacja Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Agent Skills standard (agentskills.io)](https://agentskills.io/)
- [Referencyjne skille (Anthropic)](https://github.com/anthropics/skills)
- [Awesome Copilot — kolekcja społeczności](https://github.com/github/awesome-copilot)
- [Porównanie z Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Prompt Files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [Custom Agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
