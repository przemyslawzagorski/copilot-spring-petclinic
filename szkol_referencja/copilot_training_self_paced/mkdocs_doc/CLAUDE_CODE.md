# MkDocs — adaptacja dla Claude Code

> Generowanie dokumentacji MkDocs działa identycznie w Claude Code. Kluczowa różnica: używasz subagenta zamiast prompt file.

---

## Sposób 1: Subagent mkdocs-documentation (zalecany)

Ten projekt ma skonfigurowanego subagenta w `.claude/agents/mkdocs-documentation.md`.

```
@"mkdocs-documentation (agent)" wygeneruj pełną dokumentację projektu
```

Subagent sam:
- Przeanalizuje `pom.xml`, kod źródłowy, `application.properties`
- Wygeneruje `docs/` z architekturą C4 w Mermaid
- Stworzy `mkdocs.yml` z Material theme
- Uruchomi `mkdocs serve`

---

## Sposób 2: Prompt bezpośredni

Zamiast `.github/prompts/create_first_documentation.prompt.md` (Copilot) — po prostu wpisz w sesji:

```
Wygeneruj kompletną dokumentację MkDocs dla tego projektu.
Sekcje: Introduction, Configuration (tabela properties), Architecture (C4 Mermaid), API.
Dokumentacja po angielsku. Uruchom mkdocs serve na końcu.
```

Claude Code odczyta pliki projektu i wygeneruje dokumentację bez `@workspace`.

---

## Instalacja MkDocs

```bash
pip install mkdocs mkdocs-material
```

Weryfikacja:
```bash
mkdocs --version
```

Uruchomienie podglądu:
```bash
mkdocs serve
# Otwórz: http://127.0.0.1:8000/
```

---

## Porównanie: Copilot prompt vs Claude Code

| Copilot | Claude Code |
|---|---|
| `.github/prompts/create_first_documentation.prompt.md` | `.claude/agents/mkdocs-documentation.md` |
| `agent: 'agent'` w frontmatter | `tools: Read, Edit, Write, Bash, Glob, Grep` |
| Wywołanie przez prompt picker | `@"mkdocs-documentation (agent)"` |
| `mkdocs-example.instructions.md` z `applyTo: mkdocs.yml` | Wzorzec inline w system prompcie agenta |

**Efekt końcowy jest identyczny** — dokumentacja MkDocs Material z C4 Mermaid.

---

## Ten projekt już ma dokumentację

Folder `docs/` i `mkdocs.yml` są już wygenerowane. Sprawdź:

```bash
mkdocs serve
```

Jeśli chcesz zaktualizować po zmianach w kodzie:
```
@"mkdocs-documentation (agent)" zaktualizuj dokumentację — dodano nowe endpointy do OwnerController
```
