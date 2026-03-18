# Custom Agenty

## 🎯 Cele modułu

- Utworzyć własnego agenta w `.github/agents/`.
- Konfigurować frontmatter: tools, handoffs, argument-hint, hooks.
- Zaprojektować multi-agent workflow: Planner → Executor → Reviewer.
- Stosować ograniczenia narzędzi (read-only agent, agent bez terminala).

---

## 📚 Teoria

### Agent = plik `.agent.md`

Lokalizacja: `.github/agents/<nazwa>.agent.md`

```yaml
---
name: Mój Agent
description: "Krótki opis — wyświetlany w UI i przy auto-invokacji."
tools: [read, edit, search, execute, todo]
argument-hint: "Co ma robić agent — wyświetlane jako placeholder."
user-invocable: true
---

Treść systemowa agenta — instrukcje, zasady, format odpowiedzi.
```

### Kluczowe pola frontmatter

| Pole | Opis |
|------|------|
| `name` | Nazwa wyświetlana w UI |
| `description` | Opis do discovery (modele czytają to pole przy wyborze agenta) |
| `tools` | Lista dozwolonych narzędzi: `read`, `edit`, `search`, `execute`, `todo`, `fetch` |
| `argument-hint` | Placeholder w polu tekstowym |
| `user-invocable` | `true` = widoczny w `/` menu. `false` = tylko przez handoff |
| `disable-model-invocation` | `true` = model nie wywoła automatycznie tego agenta |
| `model` | Wymuszony model, np. `gpt-4o`, `claude-sonnet-4-20250514` |
| `agents` | Lista sub-agentów, do których ten agent ma dostęp |

### Handoffs — przekazywanie między agentami

Handoffs definiuj **w YAML frontmatter** (nie w body!):

```yaml
---
handoffs:
  - label: "Przekaż do Reviewera"
    agent: ReviewerAgent
    prompt: "Przejrzyj zmiany z poprzedniego kroku."
    send: false
    model: claude-sonnet-4-20250514
---
```

| Pole | Opis |
|------|------|
| `label` | Tekst przycisku widocznego po odpowiedzi agenta |
| `agent` | Nazwa agenta docelowego (bez `.agent.md`) |
| `prompt` | Kontekst przekazany do agenta docelowego |
| `send` | `true` = wyślij automatycznie, `false` = pokaż przycisk |
| `model` | Opcjonalny model dla docelowego agenta |

### Ograniczanie narzędzi — wzorce

- **Read-only agent** (code review): `tools: [read, search, todo]`
- **Bez terminala** (bezpieczny): pomiń `execute` w liście tools
- **Pełny autonomiczny**: `tools: [read, edit, search, execute, todo, fetch]`

### Wbudowane agenty VS Code

VS Code dostarcza 3 wbudowane agenty (nie trzeba ich tworzyć):

| Agent | Skrót | Rola |
|-------|-------|------|
| **Agent** | domyślny | Autonomiczne wykonywanie zadań (edycja, terminal, testy) |
| **Ask** | `@ask` | Odpowiada na pytania bez modyfikowania kodu |
| **Plan** | `@plan` | Tworzy plan krokowy, realizuje po zatwierdzeniu |

### 🔗 Żywe przykłady w `.github/agents/`

W tym repozytorium jest 5 gotowych agentów — przeanalizuj ich budowę:

| Agent | Kluczowa cecha |
|-------|---------------|
| `mentor.agent.md` | Prosty agent bez frontmatter tools — dziedziczony domyślny zestaw |
| `mkdocs-documentation.agent.md` | `tools: [read, edit, search, execute, todo]` — pełny zestaw |
| `ports-adapters-refactor.agent.md` | `argument-hint` + fazowy workflow |
| `senior-security-code-review.agent.md` | `tools: [read, search, todo]` — **celowo read-only** |
| `vet-crud-feature.agent.md` | Pełny workflow: analiza → plan → pytania → implementacja |

---

## 📝 Ćwiczenia

| # | Ćwiczenie | Czas |
|---|-----------|------|
| 🅱️ ex_18b | Migracja między językami — Java → Python | ~15 min |
| 🅱️ ex_18c | Refaktoring architektury z AI | ~12 min |
| ex_19 | Multi-agent: Planner → Executor | ~15 min |
| ex_20 | Handoffs — przyciski przekazania | ~15 min |
| ex_21 | Quality gate — Reviewer agent | ~15 min |
| 🅱️ ex_21c | Bonus: pełny pipeline Plan→Execute→Review | ~20 min |

Pliki ćwiczeń: `exercises/`

Przykładowe agenty do podglądu: `examples/.github/agents/`
