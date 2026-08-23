# Moduł 11 (BONUS) — Agentic AI: adaptacja dla Claude Code

> Filary modułu (pętla agentic, tokeny, multinarzędziowość) są tool-agnostyczne. Tu masz **mapowanie komend i pojęć** Copilot ↔ Claude Code oraz dodatkowe sztuczki specyficzne dla CC.

---

## Mapa komend i pojęć

| Pojęcie / akcja | GitHub Copilot | Claude Code |
|---|---|---|
| Diagnoza budżetu kontekstu | Podgląd *References* dołączonych do odpowiedzi | `/context` |
| Kompaktowanie sesji | Nowy wątek / „Clear conversation" | `/compact` (proaktywnie @ ~70%) |
| Twardy reset kontekstu | Nowy czat | `/clear` |
| Wybór modelu | Picker modeli w UI | `/model haiku\|sonnet\|opus` lub `/config` |
| Tryb planu (plan-before-build) | Agent `@plan` | `Shift+Tab` (plan mode) lub agent `Plan` |
| Budżet myślenia (extended thinking) | brak bezpośredniej kontroli | `/effort`, `/config`, `MAX_THINKING_TOKENS=8000` |
| Instrukcje projektu | `.github/copilot-instructions.md` | `CLAUDE.md` |
| Subagenci | `.github/agents/*.agent.md` | `.claude/agents/*.md` |
| Konfiguracja MCP | `.vscode/mcp.json` / ustawienia | `.mcp.json` |
| Autonomiczny tryb wieloagentowy | Coding Agent / Agent HQ | `/goal`, Workflows, `ultracode` |

---

## Filar 2 (tokeny) — sztuczki specyficzne dla Claude Code

Claude Code daje Ci twarde dźwignie, których Copilot nie ma:

```bash
# 1. Zdiagnozuj, zanim zoptymalizujesz
/context

# 2. Ogranicz narzut wyjścia narzędzi (settings.json)
#    "tool output ~8000, bash output ~20000" — patrz docs/costs
# 3. Obniż koszt myślenia tam, gdzie nie trzeba głębokiego rozumowania
MAX_THINKING_TOKENS=8000

# 4. Preferuj narzędzia CLI nad serwerami MCP — mniejszy stały narzut
#    (Anthropic zaleca standardowe narzędzia zamiast MCP tam, gdzie się da)
```

**Reguła CC:** złożoną pracę trzymaj w pierwszych ~80% sesji (świeży kontekst). Ogon sesji → lekkie zadania. Po wątku → `/clear`.

> ⚠️ Subagenci **nie są automatycznie tańsi** — sama architektura dokłada narzut startowy. Używaj ich, gdy *oszczędność na odgruzowaniu głównego kontekstu* przewyższa ten narzut (gadatliwe skany, duże grepy, równoległe wątki). Dla drobnicy — rób inline.

---

## Filar 1 (pętla) — różnica: brak handoff chain

W Copilot definiujesz sztywny łańcuch `handoffs:` (A → B → C). **Claude Code tego nie ma.** Zamiast tego:

- **Claude sam deleguje** na podstawie pola `description` subagenta (im dokładniejszy opis, tym lepsza delegacja).
- Możesz **jawnie prosić** o delegację w prompcie: „użyj `@"tdd-expert (agent)"`".
- Dla deterministycznych workflow → **Workflows** (`ultracode`) albo `/goal` (agent nie odpuszcza, aż skończy cel).

Pętlę z ex_33 w czystym CC zapiszesz tak (bez ręcznego klikania handoffów):

```
Wykonaj pełny cykl dla walidacji telephone (9 cyfr) w Owner:
1. Najpierw zbadaj Owner.java i OwnerController.java (nie pisz kodu).
2. Pokaż plan, poczekaj na moją akceptację.
3. Zaimplementuj (deleguj do feature-builder).
4. Napisz testy (deleguj do tdd-expert).
5. Zrób review (deleguj do reviewer), raport Critical/Major/Minor.
```

Claude poprowadzi pętlę sam, delegując do subagentów z `.claude/agents/`.

---

## Filar 3 (multi-tool) — Claude Code jako warstwa, nie monopol

Nawet jeśli głównie używasz Claude Code, multinarzędziowość zostaje:

- **Claude Code wewnątrz Copilot** — od lutego 2026 CC działa jako third-party agent w Copilot Pro+/Enterprise. Nie musisz wybierać platformy.
- **Wspólny MCP** — ten sam serwer MCP (`.mcp.json`) obsługuje CC i innych agentów; jedno źródło danych, brak duplikacji kontekstu.
- **Cross-check w CC** — odpal dwie sesje CC (lub CC + Codex) na ten sam prompt, porównaj `git diff`. Dla krytycznych zmian.
- **Równoległość = osobne gałęzie / worktree** — w CC możesz prowadzić kilka wątków; trzymaj je na osobnych gałęziach, by nie deptać plików.

```bash
# Cross-check dwóch niezależnych przebiegów na osobnych gałęziach
git switch -c feat/x-claude
# (drugi przebieg / drugie narzędzie)
git switch -c feat/x-codex
git diff feat/x-claude feat/x-codex   # porównaj rozbieżności
```

---

## Skrót: te same recepty, komendy CC

| Recepta | Komendy / akcje w Claude Code |
|---------|-------------------------------|
| **Tokeny** | `/context` → lean `CLAUDE.md` (<200 linii) → celowane pliki → `/model` do zadania → `/compact` @ ~70% → `/clear` po wątku |
| **Pętla** | każ zbadać (read-only) → `Shift+Tab` plan → deleguj do `.claude/agents/` → uruchom testy + `@"reviewer (agent)"` |
| **Multi-tool** | routing wg warstwy → wspólny `.mcp.json` → cross-check na osobnych gałęziach → `ultracode`/`/goal` dla orkiestracji |

**Więcej:** [README modułu 11](README.md) · moduł 08 [CLAUDE_CODE.md](../08_custom_agenty/CLAUDE_CODE.md) · `szkol_referencja/claude_code_guide/README.md`

---

## Pomiar: `/usage` i `/insights` obok `/context`

Ex_32 uczy czytać `/context` — czyli **ile** kontekstu zajmujesz teraz. Do
domknięcia pętli pomiarowej brakują dwie komendy.

| Komenda | Odpowiada na pytanie |
|---|---|
| `/context` | Co **w tej chwili** siedzi w oknie i ile zajmuje |
| `/usage` | Ile tokenów i pieniędzy poszło **do tej pory** |
| `/insights` | Raport HTML z **ostatnich sesji** — gdzie naprawdę uciekał budżet |

**Ćwiczenie (~10 min), rozszerzenie ex_32:**

1. Zacznij świeżą sesję i od razu sprawdź `/context`. Zapisz zajętość
   **zanim** cokolwiek zrobisz — to Twój koszt w spoczynku: system prompt,
   katalog narzędzi, `CLAUDE.md`.
2. Wykonaj ćwiczenie z modułu 06 (cykl TDD) w całości.
3. `/usage` — ile kosztowało to, co przed chwilą zrobiłeś.
4. `/insights` — otwórz raport i znajdź, która sesja z ostatnich dni była
   najdroższa. Odpowiedz sobie: **dlaczego?**

**Spodziewany wynik:** koszt startowy jest niezerowy i płacisz go w każdej
turze — to jest efekt opisany w slajdach jako kula śnieżna. Największe sesje
zwykle nie są tymi, w których zrobiłeś najwięcej.

**Powiązanie:** [slajdy o ekonomii kontekstu](../../../slajdy_ekonomia_kontekstu/00_PRZEWODNIK.md)
opierają się na dokładnie takich pomiarach, tylko zebranych z 226 sesji.
Moduły [01](../../../slajdy_ekonomia_kontekstu/01_kula_sniezna.md)
i [05](../../../slajdy_ekonomia_kontekstu/05_obserwacja.md) tłumaczą, co z tymi
liczbami zrobić.
