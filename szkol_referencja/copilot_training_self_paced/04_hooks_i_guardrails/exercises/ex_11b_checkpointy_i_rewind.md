# Ex 11b: Checkpointy — co naprawdę da się cofnąć

> Bonus · ~12 min · Między ex_11 a ex_18

**Po co:** Hook blokuje coś, zanim się wydarzy. Checkpoint ratuje po fakcie. Oba
narzędzia mają wbudowane cofanie — i oba mają tę samą dziurę, o której nikt nie
mówi na demo. Znalezienie jej jest właściwym celem tego ćwiczenia.

---

## Część A — Copilot: Restore Checkpoint

VS Code robi migawkę plików **przed każdym requestem** w trybie agentowym.

1. Włącz podgląd zmian (Ctrl+, → wyszukaj `chat.checkpoints`):

```text
chat.checkpoints.enabled          = true   (domyślnie włączone)
chat.checkpoints.showFileChanges  = true   (pokazuje pliki i +/- linie)
```

2. W trybie Agent poproś o zmianę w kilku plikach:

```
Dodaj pole "email" do encji Owner — zaktualizuj encję, formularz HTML i testy.
```

3. Najedź na **poprzedni** request w widoku chatu → **Restore Checkpoint** → potwierdź.
4. Zobacz, co się stało: pliki wróciły do stanu sprzed requestu, a kolejne
   requesty zniknęły z historii rozmowy. Sam prompt zostaje nietknięty.
5. Kliknij **Redo** — zmiany wracają **bez ponownego odpytywania modelu**
   (czyli za darmo).

**Edycja starego promptu:** każdy request w historii da się edytować
(`chat.editRequests`). VS Code cofa wtedy zmiany tego requestu i wszystkich
następnych, po czym wysyła poprawioną wersję.

---

## Część B — Claude Code: `/rewind`

Claude Code robi checkpoint **przed każdym Twoim promptem** i trzyma 100
ostatnich w sesji.

1. Poproś o analogiczną zmianę w kilku plikach.
2. Wpisz `/rewind` albo naciśnij **Esc dwa razy** przy pustym polu wejścia.

> Jeśli w polu jest tekst, podwójny Esc go czyści zamiast otwierać menu.
> Tekst ląduje w historii — odzyskasz go strzałką w górę.

3. Wybierz punkt na liście i porównaj opcje, których Copilot nie ma:

| Opcja | Co robi |
|---|---|
| Restore code and conversation | cofa kod **i** rozmowę |
| Restore conversation | cofa rozmowę, **kod zostaje** |
| Restore code | cofa pliki, **rozmowa zostaje** |
| Summarize from here | zwija rozmowę od tego miejsca w streszczenie |
| Summarize up to here | zwija rozmowę **przed** tym miejscem |

4. Wybierz **Restore conversation** i zobacz efekt: masz kod, ale bez historii,
   która do niego doprowadziła. To jest narzędzie do odzyskiwania okna
   kontekstu, nie tylko do naprawiania błędów.

**Różnica trwałości:** checkpointy Claude Code zapisują się razem z sesją, więc
`/rewind` działa też po `--resume`. Kasują się po 30 dniach
(`cleanupPeriodDays`). Checkpointy Copilota żyją w obrębie sesji chatu.

---

## Część C — dziura, o której trzeba wiedzieć

Poproś agenta (**dowolnego z dwóch**) o coś takiego:

```
Utwórz plik roboczy notatka.txt z dowolną treścią, a potem usuń go poleceniem
terminala rm (Linux/macOS) albo del (Windows). Pokaż mi wynik.
```

Teraz spróbuj cofnąć tę operację checkpointem.

**Spodziewany wynik: nie da się.**

- **Claude Code** śledzi wyłącznie edycje przez własne narzędzia plikowe.
  Zmiany wprowadzone komendą w terminalu (`rm`, `mv`, `cp`) **nie są objęte
  checkpointem**.
- **Copilot** robi migawkę *plików objętych requestem* — to, co proces
  potomny zrobił w systemie plików, jest poza tym obrazem.

## Checklist walidacji

- [ ] Restore Checkpoint w Copilocie cofnął pliki **i** uciął historię rozmowy
- [ ] Redo przywrócił zmiany bez odpytywania modelu
- [ ] `/rewind` → **Restore conversation** zostawił kod nietknięty
- [ ] Operacja wykonana w terminalu **nie** cofnęła się w żadnym z narzędzi

## Wniosek

Checkpoint to nie jest kontrola wersji — to cofnięcie *tury*, i obejmuje tylko
to, co agent zmienił **własnymi rękami w Twojej turze**. Poza zasięgiem
zostają: komendy terminala, edycje subagentów i zmiany wprowadzone równolegle
poza narzędziem.

> **W Claude Code jest tego jeszcze więcej:** edycje subagenta zwykle nie
> wracają przy `/rewind` (wyjątek: skill z `context: fork` działający na
> pierwszym planie). Dotyczy to również `/code-review --fix`, który domyślnie
> działa w tle. Cofasz to gitem, nie rewindem.

Praktyczny wniosek na warsztat: **commituj przed puszczeniem agenta na większe
zadanie.** Checkpoint jest wygodny, ale git jest jedyną granicą, która trzyma
zawsze.

---

> 🧹 **Posprzątaj:** `git checkout -- .` — część A zostawia zmiany w encji
> `Owner`, których checkpoint mógł nie cofnąć w całości. To zresztą dobra
> pointa tego ćwiczenia.

**Powiązane:** ex_11 (hook blokujący — obrona *przed*), ex_18 (hook kontra prompt)
