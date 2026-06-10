# Ex 32: Recepta na tokeny — context engineering w praktyce

> Moduł 11 (bonus) · Filar 2 · ~20 min · Źródło: KDnuggets / Fundesk (2026)

**Po co:** Tokeny to Twój budżet — czasu, jakości i pieniędzy. Nauczysz się *diagnozować* i *ciąć* zużycie zamiast „przepalać" kontekst. Cel: ta sama robota za ułamek tokenów, bez spadku jakości.

**Twardy fakt na rozgrzewkę:** każda nowa wiadomość przesyła CAŁĄ historię sesji na nowo. W długiej sesji wiadomość 201 kosztuje tyle, co wiadomości 1–200 razem. Dlatego nie chodzi o „krótsze prompty", tylko o **higienę kontekstu**.

---

## Co zrobić

### Krok 1 — Diagnoza (`/context`)

Zanim cokolwiek zoptymalizujesz, zobacz co realnie zżera budżet.

```
/context
```

Zapisz, ile zajmuje: system prompt, narzędzia/MCP, pliki w kontekście, historia. Szukaj „cichych grzechów" — np. duży MCP albo plik instrukcji ładowany w każdej turze.

> Copilot: nie ma `/context`, ale ten sam efekt osiągniesz patrząc na *References* dołączone do odpowiedzi i ograniczając je. Patrz [CLAUDE_CODE.md](../CLAUDE_CODE.md).

### Krok 2 — Lean instrukcje projektu

Otwórz `CLAUDE.md` (lub `.github/copilot-instructions.md`). Sprawdź długość:

```
# PowerShell — policz linie
(Get-Content CLAUDE.md | Measure-Object -Line).Lines
```

**Reguła:** < 200 linii, tylko *stabilne* reguły (komendy testów, konwencje, bezpieczeństwo). Wytnij notatki, długie tutoriale, historię decyzji. Plik 5 000 tokenów kosztuje 5 000 tokenów **w każdej turze**.

> Zadanie: wskaż agentowi jedną sekcję `CLAUDE.md`, która jest „miła, ale nieobowiązkowa", i przenieś ją do osobnego pliku ładowanego na żądanie.

### Krok 3 — Precyzyjne wskazywanie zamiast dumpu

Porównaj dwa prompty na tym samym repo i oceń różnicę w zużyciu:

❌ **Rozrzutny:**
```
Przejrzyj cały projekt i powiedz, czy VetController ma problemy z wydajnością.
```

✅ **Oszczędny:**
```
Przeczytaj TYLKO src/main/java/.../vet/VetController.java linie 30–90
i oceń wydajność metody showVetList. Nie czytaj innych plików.
```

Semantyczne, celowane pobieranie zamiast „przejrzyj wszystko" daje **~40% mniej tokenów** przy tej samej jakości odpowiedzi.

### Krok 4 — Dobór modelu do zadania

Ustaw zasadę i zastosuj ją na żywo:

| Zadanie | Model |
|---------|-------|
| Mechaniczne (rename, formatowanie, prosty test) | tańszy/szybszy (Haiku / Sonnet) |
| Codzienna edycja, refaktor | średni (Sonnet) |
| Złożona analiza, architektura, debug | mocny (Opus) |

```
/model sonnet      # Claude Code — przełącz przed rutynową robotą
```

Opus kosztuje ~5× więcej za token niż Sonnet — nie płać za myślenie tam, gdzie go nie trzeba.

### Krok 5 — Kompaktuj proaktywnie i czyść

```
/compact     # zrób to przy 60–75% wypełnienia, NIE czekaj na ostrzeżenie
/clear       # po zamknięciu wątku — twardy reset kontekstu
```

Patrz na **procent wypełnienia**, nie na bezwzględną liczbę tokenów. Kompaktowanie streszcza sesję, zachowując decyzje architektoniczne i nierozwiązane wątki.

### Krok 6 — Deleguj gadatliwość subagentowi

Zadania o wielkim, „śmieciowym" wyjściu (skan bezpieczeństwa, duży grep, log z testów) oddaj subagentowi — do głównego kontekstu wróci tylko streszczenie (~10× oszczędności):

```
@"security-expert (agent)" przeskanuj walidację w pakiecie owner i zwróć
TYLKO listę: plik:linia + jedno zdanie ryzyka. Bez cytowania kodu.
```

---

## Spodziewany wynik

- Znasz rozkład swojego budżetu kontekstu (`/context`).
- `CLAUDE.md` / instrukcje < 200 linii, same esencje.
- Ten sam wynik analizy uzyskujesz promptem celowanym, zauważalnie taniej niż „przejrzyj projekt".
- Masz nawyk: `/compact` przy ~70%, `/clear` po wątku, model dobrany do zadania.

## Checklist walidacji

- [ ] Uruchomiłeś `/context` i wskazałeś największego „pożeracza" tokenów.
- [ ] Sprawdziłeś długość `CLAUDE.md` i wiesz, co z niego wyciąć.
- [ ] Masz dwa prompty (rozrzutny vs celowany) i widzisz różnicę w zakresie czytanych plików.
- [ ] Przełączyłeś model komendą `/model` zależnie od zadania.
- [ ] Wykonałeś `/compact` świadomie (a nie pod przymusem ostrzeżenia).
- [ ] Oddałeś gadatliwe zadanie subagentowi i dostałeś streszczenie zamiast ściany tekstu.

**Więcej:** [README — Filar 2](../README.md) · [CLAUDE_CODE.md](../CLAUDE_CODE.md)
