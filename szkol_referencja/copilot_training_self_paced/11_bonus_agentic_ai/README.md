# Moduł 11 (BONUS) — Agentic AI: tokeny, pętla agenta i multinarzędziowość

> Moduł bonusowy, przekrojowy. Spina wiedzę z modułów 01–10 w trzy **recepty na codzienną pracę** z agentami AI w 2026 r.
> Działa dla GitHub Copilot, Claude Code i Augmenta (mapowanie różnic:
> [CLAUDE_CODE.md](CLAUDE_CODE.md) oraz [AUGMENT.md](AUGMENT.md)).

---

## 🎯 Cele modułu

- Zrozumieć **jak myśli agent** i ułożyć pod to swój workflow (pętla: zbadaj → zaplanuj → deleguj → zweryfikuj).
- Opanować **context engineering** — świadome zarządzanie tokenami zamiast „przepalania" kontekstu.
- Nauczyć się **multinarzędziowości** — łączyć Copilot, Claude Code i inne narzędzia zamiast szukać „jednego najlepszego".
- Wyjść z 3 gotowymi **recepturami**, które stosujesz od następnego zadania.

---

## 🤔 Czemu to robimy, po co, jak i co nam to daje

To pytanie wraca na każdym szkoleniu, więc odpowiadamy wprost — zanim wejdziemy w technikę.

| Pytanie | Odpowiedź |
|---------|-----------|
| **Czemu?** | Bo narzędzia przestały być „autouzupełniaczem". W 2026 r. agent **sam czyta repo, planuje, edytuje wiele plików, uruchamia testy i robi PR**. Kto pracuje z nim jak z autocomplete, traci 80% wartości. |
| **Po co?** | Żeby z „przypadkowego szczęścia" zrobić **powtarzalny proces**. Agent bez ramy generuje ładny kod, który nie pasuje do projektu. Z ramą — robi to, co trzeba, za mniej pieniędzy. |
| **Jak?** | Trzy filary: **(1)** pętla agentic (sterujesz procesem, nie pojedynczym promptem), **(2)** context engineering (pilnujesz budżetu tokenów), **(3)** multinarzędziowość (właściwe narzędzie do warstwy zadania). |
| **Co nam to daje?** | **Mniej kosztów** (Claude Code zużywa ~5,5× mniej tokenów niż Cursor na tym samym zadaniu — 33K vs 188K), **mniej błędów** (multi-agent z dedykowanym kontekstem = +90% jakości w badaniach Anthropic), **większą autonomię** (delegujesz całe zadania, nie linijki). |

> **Jedno zdanie do zapamiętania:** *Nie promptujesz lepiej — projektujesz to, co agent widzi (kontekst) i jak działa (proces).*

---

## 📚 Teoria — trzy filary

### Filar 1 · Pętla agentic — jak myśli agent

Agent nie „odpowiada na pytanie". Agent kręci pętlę: **plan → akcja → obserwacja → korekta**, aż osiągnie cel. Twoja rola to nie pisać kod, tylko **sterować tą pętlą**.

```
[ Ty: cel + ograniczenia ]
        │
        ▼
   ┌─────────┐  zbadaj repo (search/read)
   │ ZBADAJ  │──────────────┐
   └─────────┘              │
        │                   ▼
   ┌─────────┐        ┌──────────┐
   │ ZAPLANUJ│◀──────▶│  PĘTLA   │  akcja → obserwacja → korekta
   └─────────┘        └──────────┘
        │                   │
        ▼                   ▼
   ┌─────────┐        ┌──────────┐
   │ DELEGUJ │───────▶│ ZWERYFIKUJ│  testy / review / diff
   └─────────┘        └──────────┘
```

**Recepta na pracę z agentem (4 kroki):**

| Krok | Co robisz | Dlaczego to działa |
|------|-----------|--------------------|
| 1. **Zbadaj** | Każ agentowi najpierw *przeczytać* relevantne pliki, zanim cokolwiek napisze. | Cognition zmierzyło: agenty spędzają **60% czasu na szukaniu kontekstu** przed pisaniem. Pomóż mu — wskaż pliki. |
| 2. **Zaplanuj** | Wymuś *plan-before-build* (tryb Plan / `Shift+Tab` / agent `Plan`). Zatwierdź plan, dopiero potem kod. | Plan jest tani w tokenach i łatwy do poprawienia. Zły kod jest drogi do cofnięcia. |
| 3. **Deleguj** | Rozdziel pracę na **subagentów** z osobnym kontekstem (badanie ≠ implementacja ≠ review). | Multi-agent z dedykowanym kontekstem: **+90% jakości** (Anthropic). Jeden agent robiący wszystko „przepala własny kontekst". |
| 4. **Zweryfikuj** | Niech agent uruchomi testy / pokaże `diff` / przejdzie review-agentem. Nie ufaj „na słowo". | Zamyka pętlę self-correction. Agent łapie własne błędy, zanim Ty je zobaczysz. |

> 🔗 W tym repo masz gotowych subagentów do każdego kroku: `feature-builder` (badanie+implementacja), `tdd-expert` (testy), `reviewer` / `security-expert` (weryfikacja). Patrz moduł 08.

---

### Filar 2 · Tokeny = context engineering

**Najdroższy mit:** „mam duże okno kontekstu, więc wrzucam wszystko". Prawda jest odwrotna.

Dwa twarde fakty z 2026 r.:

1. **Każda wiadomość przesyła CAŁĄ historię na nowo.** Wiadomość 201 kosztuje w tokenach wejściowych tyle, co wiadomości 1–200 razem. Długa sesja = kwadratowy wzrost kosztu.
2. **Context rot** — *mierzalny* spadek trafności modelu wraz z długością wejścia. Badanie Chroma (2025): **wszystkie 18 frontier-modeli** się degraduje („lost in the middle", rozcieńczenie uwagi). Więcej kontekstu ≠ lepiej.

**Context engineering** = świadome kuratorowanie tego, co agent widzi (system prompt, narzędzia, pliki, pamięć, wyniki narzędzi), żeby zmaksymalizować jakość przy minimum tokenów.

**Recepta na tokeny (7 ruchów):**

| # | Ruch | Konkret |
|---|------|---------|
| 1 | **Diagnozuj, nie zgaduj** | Zacznij od `/context` — zobacz co realnie zżera budżet („ciche grzechy" w tle). |
| 2 | **Lean `CLAUDE.md` / instructions** | Trzymaj < 200 linii, tylko stabilne reguły. Plik 5 000 tokenów kosztuje **5 000 tokenów w każdej turze**. |
| 3 | **Kompaktuj proaktywnie** | `/compact` przy **60–75%** wypełnienia, *zanim* pojawi się ostrzeżenie. Patrz na % wypełnienia, nie na liczbę tokenów. |
| 4 | **Dobieraj model do zadania** | Mechaniczne → tańszy/szybszy model; złożona analiza → mocniejszy. Opus kosztuje ~5× więcej niż Sonnet za token. |
| 5 | **Wskazuj dokładne pliki i linie** | `VetController.java` linie 30–90, zamiast „przejrzyj projekt". Semantyczne pobieranie zamiast dumpu = **~40% mniej tokenów** przy tej samej jakości. |
| 6 | **Deleguj gadatliwe rzeczy subagentom** | Verbose output (logi, duże skany) trzymaj w osobnym agencie — wraca tylko streszczenie (~10× oszczędności). |
| 7 | **Trzymaj tooling prosty** | Każde MCP/narzędzie to stały narzut w kontekście. Dokładaj tylko to, co rozwiązuje realny, powtarzalny problem. |

> **Reguła budżetu:** złożoną pracę rób w pierwszych ~80% sesji (gdy kontekst „świeży"). Ogon sesji zostaw na lekkie zadania. Po skończonym wątku — `/clear`.

---

### Filar 3 · Multinarzędziowość — composition over consolidation

W 2026 r. branża przestała szukać „jednego najlepszego narzędzia". Cursor, Claude Code, Codex i Copilot **zrastają się w jeden stack**: warstwa orkiestracji + wykonania + review. Spoiwem jest **MCP** (otwarty protokół Anthropic, standaryzuje dostęp agentów do narzędzi i danych).

**Recepta na multinarzędziowość (4 wzorce):**

| Wzorzec | Kiedy | Jak |
|---------|-------|-----|
| **1. Specjalizacja** | Codziennie, domyślnie | Architektura / refaktor wielu plików → **Claude Code**. Algorytm / testy → **Codex**. Inline autocomplete / szybkie edycje → **Copilot**. Dobierasz narzędzie do *warstwy* zadania. |
| **2. Cross-check** | Zmiany wysokiego ryzyka (security, migracje, perf) | Ten sam prompt do dwóch agentów niezależnie, potem `diff` wyników. Zgodne → działasz szybciej. Rozbieżne → rozbieżność wskazuje, gdzie problem jest naprawdę niejednoznaczny. (Koszt ~2×, więc tylko dla krytycznych zmian.) |
| **3. Fan-out (Agent HQ)** | Jedno zadanie, kilka pomysłów | Przypisz to samo issue do kilku agentów → 2–3 niezależne PR-y → review porównawcze. |
| **4. Wspólny MCP** | Full-stack, wiele agentów | Jeden serwer MCP = wszystkie agenty czytają **te same dane bez duplikowania kontekstu**. |

> **Izolacja:** agenty równoległe pracują na **osobnych gałęziach / git worktree**, żeby nie deptać sobie po plikach. Agent HQ wymusza to domyślnie.

**Krajobraz narzędzi (stan na maj/czerwiec 2026):**

| | Claude Code | GitHub Copilot |
|---|---|---|
| Natura | Terminalowy agent — deleguje całe zadania | IDE-owy asystent + tryb agentowy (Agent HQ, Coding Agent) |
| Okno kontekstu | do **1 mln tokenów** (całe średnie repo) | ~32K–128K (mniejsze, skupione zadania) |
| Mocna strona | Wielokrokowe, wieloplikowe zadania z mniejszą liczbą błędów | Inline flow, integracja z GitHub, wybór wielu modeli |
| Rozliczenie | Subskrypcja / API | Od **1 czerwca 2026** usage-based: GitHub AI Credits (zamiast PRU), pula na org |
| Razem? | Od lutego 2026 Claude Code działa **wewnątrz** Copilot Pro+/Enterprise jako third-party agent |

> **Wniosek:** to nie „albo–albo". Dobierasz narzędzie do warstwy, a MCP spina je wspólnym kontekstem.

---

## 📝 Ćwiczenia

| # | Ćwiczenie | Filar | Czas |
|---|-----------|-------|------|
| ex_32 | Recepta na tokeny — context engineering w praktyce | Tokeny | ~20 min |
| ex_33 | Recepta na pętlę agentic — zbadaj → zaplanuj → deleguj → zweryfikuj | Pętla agentic | ~25 min |
| ex_34 | Recepta na multinarzędziowość — specjalizacja, cross-check, wspólny MCP | Multi-tool | ~20 min |
| 🅱️ ex_35 | Capstone: jedno zadanie, wszystkie trzy filary naraz | Wszystkie | ~30 min |

Pliki ćwiczeń: [`exercises/`](exercises/) · Index: [EXERCISES.md](EXERCISES.md) · Adaptacja Claude Code: [CLAUDE_CODE.md](CLAUDE_CODE.md)

---

## 📎 Źródła (maj/czerwiec 2026)

Materiał oparty na bieżących publikacjach i badaniach:

- [Context Engineering: 9 Techniques for AI Coding Agents (2026) — Fundesk](https://www.fundesk.io/context-engineering-techniques-ai-coding-agents-2026)
- [7 Practical Ways to Reduce Claude Code Token Usage — KDnuggets](https://www.kdnuggets.com/7-practical-ways-to-reduce-claude-code-token-usage)
- [23 Tips for Smart Claude Code Token Saving — Analytics Vidhya (maj 2026)](https://www.analyticsvidhya.com/blog/2026/05/tips-for-claude-code-token-saving/)
- [Manage costs effectively — Claude Code Docs](https://code.claude.com/docs/en/costs)
- [Multi-Agent Orchestration: Running Claude, Codex, Copilot in Parallel (2026) — Scopir](https://scopir.com/posts/multi-agent-orchestration-parallel-coding-2026/)
- [Cursor, Claude Code, Codex merging into one stack — The New Stack](https://thenewstack.io/ai-coding-tool-stack/)
- [Claude Code vs GitHub Copilot (May 2026) — MetaCTO](https://www.metacto.com/blogs/comparing-claude-code-and-github-copilot-for-engineering-teams)
- [Best LLMs for Agentic Coding in 2026 — DEV Community](https://dev.to/danishashko/the-best-llms-for-agentic-coding-in-2026-real-world-not-just-benchmarks-96n)
