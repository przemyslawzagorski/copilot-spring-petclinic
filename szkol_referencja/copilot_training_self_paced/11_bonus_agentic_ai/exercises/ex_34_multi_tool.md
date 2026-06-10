# Ex 34: Recepta na multinarzędziowość — specjalizacja, cross-check, wspólny MCP

> Moduł 11 (bonus) · Filar 3 · ~20 min · Źródło: Scopir / The New Stack (2026)

**Po co:** W 2026 r. nie wybierasz „jednego najlepszego" narzędzia — **komponujesz stack**. Każde narzędzie obsługuje swoją warstwę (orkiestracja / wykonanie / review), a MCP spina je wspólnym kontekstem. Nauczysz się 4 wzorców i zastosujesz 2 z nich w tym repo.

> Uwaga: nie musisz mieć zainstalowanych wszystkich narzędzi. Ćwiczenie pokazuje *wzorce* — część zrobisz „na sucho" (decyzja routingu), część realnie (cross-check dwoma agentami, wspólny MCP).

---

## Co zrobić

### Krok 1 — Specjalizacja: routing zadań do warstwy (na sucho)

Przypisz każde zadanie do właściwego narzędzia wg jego *warstwy*. Uzupełnij tabelę dla 4 zadań z PetClinic:

| Zadanie | Warstwa | Narzędzie | Dlaczego |
|---------|---------|-----------|----------|
| Refaktor `vet` → porty i adaptery (wiele plików) | architektura | **Claude Code** | duże okno (do 1 mln tok.), wielokrokowość |
| Algorytm sortowania wizyt + testy | wykonanie | **Codex** | mocny w algorytmach/testach |
| Dopisanie pola w formularzu Thymeleaf | inline | **Copilot** | szybkie edycje w IDE, autocomplete |
| `___ (wybierz własne zadanie z repo)` | `___` | `___` | `___` |

**Reguła:** architektura/refaktor wielu plików → Claude Code · algorytm/testy → Codex · inline/szybkie edycje → Copilot.

### Krok 2 — Cross-check zmiany wysokiego ryzyka (realnie)

Wybierz *jedną* wrażliwą rzecz — np. regex walidacji `telephone` z ex_33 albo zapytanie wyszukujące w `VetController`. Zadaj **ten sam prompt dwóm niezależnym agentom** i porównaj:

```
# Agent A (np. security-expert)
@"security-expert (agent)" oceń bezpieczeństwo regexu walidacji telephone:
ReDoS? dopuszcza znaki spoza cyfr? Zwróć werdykt + propozycję.

# Agent B (np. reviewer)
@"reviewer (agent)" oceń ten sam regex walidacji telephone pod kątem
poprawności i edge-case'ów. Zwróć werdykt + propozycję.
```

Porównaj odpowiedzi:
- **Zgodne** → masz wysoką pewność, działasz szybciej.
- **Rozbieżne** → rozbieżność wskazuje, gdzie problem jest naprawdę niejednoznaczny — tam skup uwagę człowieka.

> Koszt cross-check ≈ 2× tokenów, więc rezerwuj go dla zmian krytycznych (security, migracje, ścieżki wydajnościowe), nie dla rutyny.

### Krok 3 — Wspólny MCP jako współdzielony kontekst (realnie)

To repo ma już skonfigurowane MCP (`.mcp.json`, moduł 09). Idea: **jeden serwer MCP = wiele agentów czyta te same dane bez duplikowania kontekstu**.

```
# PowerShell — zobacz, jakie serwery MCP są wspólne dla agentów
Get-Content .mcp.json
```

Zadanie myślowe + praktyczne: wskaż, który serwer MCP (`jira-wiki` / `publiczne-api`) mógłby być **wspólnym źródłem** dla dwóch agentów pracujących nad tym samym ticketem — jeden czyta wymagania z Jira, drugi implementuje. Zapisz, dlaczego wspólny MCP jest tańszy niż wklejanie treści ticketu do każdego agenta osobno.

### Krok 4 — Izolacja gałęzi (warunek równoległości)

Gdy agenty pracują równolegle, muszą siedzieć na **osobnych gałęziach / git worktree**, żeby nie deptać sobie po plikach:

```
# Każdy równoległy agent na swojej gałęzi
git switch -c feat/telephone-validation-agentA
# ...drugi agent:
git switch -c feat/telephone-validation-agentB
```

Potem porównaj wyniki `git diff` obu gałęzi — to jest wzorzec **fan-out → review porównawcze** (w GitHub Agent HQ robi to automatycznie: jedno issue → kilka PR-ów).

---

## Spodziewany wynik

- Masz wypełnioną tabelę routingu (które narzędzie do której warstwy) z własnym 4. zadaniem.
- Wykonałeś realny cross-check: dwie niezależne oceny tej samej wrażliwej zmiany i wiesz, gdzie się rozeszły.
- Rozumiesz, czemu wspólny MCP < duplikowanie kontekstu, i czemu równoległe agenty potrzebują osobnych gałęzi.

## Checklist walidacji

- [ ] Tabela routingu uzupełniona, w tym własne 4. zadanie z uzasadnieniem warstwy.
- [ ] Cross-check: dwie niezależne odpowiedzi na ten sam prompt, wskazany punkt rozbieżności (lub zgodność).
- [ ] Zajrzałeś do `.mcp.json` i wskazałeś kandydata na wspólny MCP dla dwóch agentów.
- [ ] Wiesz, czemu cross-check rezerwujemy dla zmian krytycznych (koszt ~2×).
- [ ] Potrafisz wymienić wzorzec izolacji równoległych agentów (osobne gałęzie / worktree).

**Więcej:** [README — Filar 3](../README.md) · moduł 09 (MCP) · [CLAUDE_CODE.md](../CLAUDE_CODE.md)
