# Konfiguracja zespołowa

> Źródło: https://code.visualstudio.com/docs/copilot/customization/instructions

## 🎯 Cele modułu

- Stworzyć `copilot-instructions.md` — globalne reguły dla całego zespołu.
- Dodać scoped instructions z `applyTo` dla konkretnych ścieżek.
- Stworzyć reużywalny prompt file (`.prompt.md`) z YAML frontmatter.
- Poznać Copilot Memory i `.copilotignore`.

---

## 📚 Teoria

### Hierarchia konfiguracji Copilota

```
1. copilot-instructions.md     → zawsze załadowane, globalne reguły repo
2. instructions/*.instructions.md → scoped — załadowane gdy plik pasuje do applyTo
3. prompts/*.prompt.md          → ręczne — wywoływane przez użytkownika
4. skills/*/SKILL.md            → auto-load lub / — reużywalna procedura (→ moduł 05)
5. agents/*.agent.md            → custom agent z osobowością i narzędziami (→ moduł 08)
6. hooks/*.json                 → enforcement — skrypt odpalany automatycznie (→ moduł 04)
```

Wszystkie pliki żyją w `.github/` w repozytorium.

### 1) copilot-instructions.md

Plik `.github/copilot-instructions.md` — zawsze załadowany dla każdego promptu w tym repo.

```markdown
# Reguły dla Copilot w tym projekcie

- Język kodu: Java 17+, używaj rekordów zamiast POJO gdzie to możliwe.
- Framework: Spring Boot 3.x, Spring Data JPA.
- Testy: JUnit 5 + Mockito. Nigdy JUnit 4.
- Nazewnictwo: camelCase, klasy z dużej litery, pakiety lowercase.
- Komentarze: Javadoc po polsku dla klas publicznych.
- Bezpieczeństwo: zawsze waliduj dane wejściowe. Nigdy nie loguj haseł.
```

> **Żywy przykład:** Otwórz `.github/copilot-instructions.md` w tym repo — to właśnie ten plik.

### 2) Scoped instructions (applyTo)

Plik `.github/instructions/java-spring.instructions.md`:

```markdown
---
description: "Reguły dla kodu Java Spring Boot"
name: "Java Spring Workspace Rules"
applyTo: "src/main/java/**/*.java,src/test/java/**/*.java"
---
# Java + Spring zasady repozytorium

- Używaj Java 17+ i stylu zgodnego z istniejącym kodem.
- Testy: tylko JUnit 5 + Mockito (nigdy JUnit 4).
- Bezpieczeństwo: waliduj dane wejściowe; nie loguj haseł.
```

Kluczowy mechanizm: **`applyTo`** — reguły aktywują się TYLKO gdy pracujesz z plikami pasującymi do globa. Dzięki temu:
- reguły Java nie przeszkadzają przy edycji YAML-a,
- reguły frontendowe nie obciążają kontekstu przy Javie.

> **Żywy przykład:** Otwórz `.github/instructions/java-spring.instructions.md` — ma marker diagnostyczny `INSTR_CHECK: java-spring.instructions.active`. Edytuj plik `.java` i sprawdź czy marker się pojawia w odpowiedzi.

### 3) Prompt files (.prompt.md)

Pliki w `.github/prompts/` — reużywalne prompty wywoływane ręcznie.

**Prosty prompt** (`refiner.prompt.md`):
```markdown
Jesteś "Prompt Refinerem". Twoim zadaniem jest wzięcie surowego zapytania
użytkownika i przekształcenie go w idealny prompt. NIE rozwiązuj problemu.
```

**Prompt z frontmatter** (`method-deep-dive.prompt.md`):
```markdown
---
description: "Analiza metody i zależności"
name: "Method Deep Dive"
argument-hint: "Podaj metodę (np. Service#doWork)"
agent: "agent"
---
Przeprowadź dogłębną analizę metody wskazanej przez użytkownika...
```

| Pole frontmatter | Co robi |
|-------------------|---------|
| `name` | Nazwa widoczna w menu |
| `description` | Kiedy pasuje do auto-complete |
| `argument-hint` | Podpowiedź po wybraniu promptu |
| `agent` | Wymuszony tryb (`"agent"`, `"ask"`) |
| `tools` | Lista narzędzi dostępnych dla promptu |

> **Żywy przykład:** Porównaj 3 prompt files w `.github/prompts/`:
> - `refiner.prompt.md` — minimalistyczny, bez frontmatter
> - `prompt-refiner.prompt.md` — z `agent: "ask"` i `argument-hint`
> - `method-deep-dive.prompt.md` — pełny: rola, sekcje, diagram Mermaid

### 4) Copilot Memory

Copilot zapamiętuje Twoje preferencje między sesjami (np. „preferuję rekordy zamiast POJO"). Memory jest osobista — nie jest współdzielona z zespołem.

Zarządzanie: Copilot Chat → „Zapamiętaj, że..." / „Zapomnij o..."

### 5) .copilotignore

Plik analogiczny do `.gitignore` — wyklucza pliki z kontekstu Copilota:

```
target/
build/
*.log
secrets/
```

---

## 📝 Ćwiczenia

| # | Ćwiczenie | Czas |
|---|-----------|------|
| ex_08 | Twój pierwszy `copilot-instructions.md` | ~10 min |
| 🅱️ ex_08b | Copilot Memory — AI zapamiętuje preferencje | ~5 min |
| ex_09 | Instrukcje per ścieżka (`applyTo`) | ~10 min |
| 🅱️ ex_09b | Exclude files — `.copilotignore` | ~5 min |
| ex_10 | Reużywalny plik promptu (`.prompt.md`) | ~10 min |
| 🅱️ ex_10b | Wybór modelu AI — porównanie GPT / Claude / Gemini | ~8 min |

Pliki ćwiczeń: `exercises/`
