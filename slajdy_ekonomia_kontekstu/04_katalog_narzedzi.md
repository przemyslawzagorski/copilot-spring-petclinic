# 04 — Katalog narzędzi: największa pojedyncza dźwignia

## Analogia

Wyobraź sobie hydraulika, który **do każdego zlecenia przywozi całą warsztatową
skrzynkę** — spawarkę, komplet gwintownic, kamerę inspekcyjną — i **liczy sobie
za jej przywiezienie**, niezależnie od tego, czy wymienił uszczelkę za pięć
złotych, czy przebudował instalację.

Tak działa katalog narzędzi. Opis **każdego** narzędzia jedzie w **każdym**
wywołaniu, czy zostanie użyte, czy nie.

## Mechanizm

Narzędzia są składane na **pozycji zerowej** zapytania — przed system promptem
i przed historią. To ma dwie konsekwencje:

1. **Płacisz za nie w każdej turze.** Zawsze, w całości.
2. **Zmiana katalogu unieważnia cały cache.** Nie tylko cache narzędzi —
   wszystko, co jest po nich, czyli dosłownie całą resztę.

Punkt drugi bywa zaskoczeniem: dorzucenie jednego narzędzia w połowie sesji
kosztuje przeliczenie **całej** historii od nowa.

## Zmierzony cennik

Ile kosztuje trzymanie poszczególnych narzędzi — koszt na **każde** wywołanie:

| Podmiot | Koszt stały | Realne użycie |
|---|---:|---|
| Subagenci (7 narzędzi) | **3 805** tok/wywołanie | **0,83%** wywołań |
| Zarządzanie zadaniami (4) | 1 869 tok/wywołanie | 5,3% — zostaw w pracy interaktywnej |
| `str-replace-editor` | 1 631 | niezbędny do edycji |
| `view` | 1 493 | niezbędny do czytania |
| `launch-process` | 1 092 | |
| `codebase-retrieval` | 332 | |
| `save-file` | 322 | |
| `web-fetch` | 173 | |

Pierwszy wiersz to sedno: **subagenci kosztują 3 805 tokenów w każdym
wywołaniu, a są używani w 0,83% przypadków.** Płacisz za nie w stu procentach
tur, korzystasz w jednym.

## Skala efektu

| Konfiguracja | Koszt stały | Zmiana |
|---|---:|---:|
| Pełny katalog | 17 219 | — |
| Bez subagentów i narzędzi zadaniowych (11 usuniętych) | **11 545** | **−33%** |
| Minimum read-only (18 usuniętych) | **9 045** | **−47,5%** |

Jedna decyzja konfiguracyjna, podjęta raz, zdejmuje **jedną trzecią stałego
kosztu każdej tury** — do końca życia tej konfiguracji.

## Narzędzia nigdy nieużyte

W 226 sesjach te miały **zero wywołań**, a były opłacane przy każdym:

```
sub-agent-validate
codebase-retrieval-raw
view-session
```

Warto zrobić taki przegląd u siebie. Wzorzec jest przewidywalny: **narzędzia
wąsko wyspecjalizowane prawie nigdy nie są wywoływane, a kosztują tyle samo, co
te używane stale.**

## Serwery MCP — ta sama pułapka, większa skala

Podpięty serwer MCP dokłada swoje narzędzia do katalogu. Ten sam mechanizm, ale
rzędy wielkości wyżej:

> **Jeden nieużywany serwer MCP to ~46 000 tokenów na wywołanie.**

Dla porównania: cały stały prefiks z pełnym katalogiem to 17 219. Jeden zbędny
serwer MCP potrafi być **trzykrotnie droższy niż wszystkie narzędzia wbudowane
razem wzięte**.

Serwery MCP mają też drugą konsekwencję, niekosztową, opisaną
w [module 09](09_allowlist_denylist.md): dokładają uprawnienia, o których
nikt nie pamięta.

## Punkt optymalny

Szesnaście konfiguracji tego samego zadania, posortowane po koszcie:

| Wariant | Tury | Tokeny | vs baza | Ocena |
|---|---:|---:|---:|:---:|
| Wszystkie 32 narzędzia usunięte, `--max-turns 1` | 1 | 4 571 | −94,5% | **0/3** |
| 2 narzędzia, `--max-turns 2` | 2 | 18 854 | −77,4% | **0/3** |
| **2 narzędzia, uncapped** | 3 | **29 830** | **−64,2%** | **3/3** |
| 2 narzędzia, `--max-turns 4` | 4 | 39 988 | −52,0% | 3/3 |
| Pełny katalog, `--max-turns 2` | 2 | 40 245 | −51,7% | 3/3 |
| Pełny katalog, uncapped *(baza)* | 4 | 83 313 | — | 3/3 |

Wiersze z oceną **0/3** to zadania **niewykonane** — oszczędność bez wartości.

> ### Optimum to mały katalog, nie mały budżet
>
> Dwa narzędzia bez limitu tur: **−64,2% przy niezmienionej ocenie 3/3.**
>
> Oszczędność bierze się z mniejszej liczby schematów w *każdym* wywołaniu,
> nie z wcześniejszego zatrzymania. **I dlatego nie kosztuje jakości.**

To jest różnica, która decyduje. Cięcie katalogu odejmuje koszt, który i tak
był marnowany. Cięcie tur odejmuje pracę.

## Co robić

**Zrób przegląd raz i zapisz trwale.** To nie jest decyzja na każdą sesję —
raz ustawiona konfiguracja pracuje dalej.

**Zacznij od subagentów, jeśli ich nie używasz.** Największy stosunek kosztu
do wykorzystania w całej tabeli.

**Odepnij serwery MCP, których nie używasz w tym projekcie.** Największa
pojedyncza kwota.

**Zostaw narzędzia zadaniowe w pracy interaktywnej.** 5,3% użycia to już
realne, a w trybie interaktywnym poprawiają przebieg.

## Częsty błąd

> „Usunę wszystkie narzędzia, będzie najtaniej."

Będzie. I zadanie nie zostanie wykonane — patrz wiersze **0/3** w tabeli.
Agent bez narzędzi nie przeczyta pliku ani go nie zapisze.

Celem nie jest minimalny katalog, tylko **katalog bez balastu**. Różnica
w liczbach: minimum bez balastu dało −64,2% przy pełnej jakości, minimum
absolutne dało −94,5% przy zerowej.
