# 06 — Reguły i skille: koszt spoczynkowy

## Analogia

**Reguła zawsze aktywna to tatuaż.** Widoczny przy każdym spotkaniu, niezależnie
od tego, czy ktoś o niego pytał.

**Skill to notatka w kieszeni.** Wyjmujesz, gdy temat się pojawi. Reszta czasu
nie zajmuje nikomu uwagi — kosztuje tylko tyle, ile trzeba, żeby pamiętać, że
ją masz.

Różnica w rachunku jest większa, niż ktokolwiek się spodziewa.

## Trzy mechanizmy, trzy koszty

| | **Rule** | **Skill** | **Command** |
|---|---|---|---|
| Kto uruchamia | agent automatycznie | agent lub Ty | **tylko Ty** |
| Kiedy ładowane | `always_apply`: zawsze<br>`agent_requested`: gdy pasuje opis | po wyzwoleniu | po wywołaniu |
| **Koszt spoczynkowy** | pełne ciało **albo** sam opis | **~66 tok** (sam opis) | **~0** |
| Do czego | konwencje, styl, niezmienniki | wiedza specjalistyczna | powtarzalny workflow |

Kluczowe jest pole **koszt spoczynkowy** — ile płacisz, gdy dana rzecz **nie
jest używana**. Bo tak jest przez większość czasu.

## Zmierzone: 483×

Ten sam plik reguły (przypadek skrajny — 81 KB), dwie wartości jednego pola:

| Konfiguracja | Instrukcje systemowe | Koszt samej reguły |
|---|---:|---:|
| bez reguły (baza) | 6 689 | — |
| `type: always_apply` | **33 729** | **27 040** |
| `type: agent_requested` | **6 745** | **56** |

> **27 040 / 56 = 483×**

Jedna linia w nagłówku pliku. Ta sama treść, ta sama funkcjonalność, ta sama
dostępność dla agenta — różnica prawie pięciusetkrotna w koszcie stałym.

Przy `agent_requested` do kontekstu trafia **sam opis**. Pełna treść dociąga się
dopiero, gdy agent uzna, że temat pasuje. To jest **progressive disclosure** i to
jest cały mechanizm.

## Kiedy `always_apply` jest uzasadnione

Nie zawsze jest błędem. Ma sens dla rzeczy, które muszą obowiązywać **bez
wyjątku i bez rozpoznawania tematu**:

- Twarde zakazy bezpieczeństwa („nigdy nie loguj haseł")
- Niezmienniki, których naruszenie jest kosztowne
- Bardzo krótkie konwencje, gdzie koszt jest w praktyce zerowy

Warunek jest jeden: **musi być krótkie.** Reguła zawsze aktywna o objętości
200 znaków to koszt pomijalny. Ta sama treść rozpisana na dwie strony to koszt
przy każdym wywołaniu, do końca życia projektu.

## Kiedy skill

Wszystko, co jest **wiedzą specjalistyczną wywoływaną sytuacyjnie**: procedury,
checklisty, wzorce dla konkretnej technologii, standardy przeglądu kodu.

Skill kosztuje ~66 tokenów w spoczynku — tyle, ile jego opis. To cena za
możliwość, żeby agent w ogóle wiedział, że taki skill istnieje.

Konsekwencja praktyczna: **możesz mieć dużo skilli.** Dziesięć skilli to ~660
tokenów stałego kosztu. Dziesięć reguł `always_apply` o tej samej treści to
wielokrotność tej liczby przy każdym wywołaniu.

## Kiedy komenda

Gdy chcesz **kontrolować moment uruchomienia** i przekazać argumenty. Koszt
spoczynkowy zerowy, bo nic nie ładuje się, dopóki nie wywołasz.

Dodatkowo komenda może nadpisać model dla siebie — co ma sens przy zadaniach
mechanicznych, patrz [moduł 08](08_wybor_modelu.md).

## Co robić

**Przejrzyj swoje reguły i sprawdź pole `type`.** To najszybszy audyt w całym
materiale — kilka minut, potencjalnie kilkaset razy mniejszy koszt stały.

**Domyślnie `agent_requested`.** Przechodź na `always_apply` tylko wtedy, gdy
umiesz uzasadnić, dlaczego ta konkretna treść musi być w każdym wywołaniu.

**Przy `agent_requested` opis jest krytyczny.** To po nim agent decyduje, czy
regułę wciągnąć. Zły opis = reguła, która nigdy się nie uruchamia i jest tylko
martwym kosztem 56 tokenów. Pisz opis jako warunek wyzwolenia („gdy pracujesz
nad kontrolerami REST"), nie jako tytuł („konwencje REST").

## Częste błędy

> „Ustawię `type: always` / `auto` / `agent`."

Żadna z tych wartości nie istnieje. Dozwolone są **`always_apply`,
`agent_requested`, `manual`**. Nieprawidłowa wartość zwykle nie wywala błędu —
po prostu reguła zachowuje się inaczej, niż zakładasz, i dowiadujesz się o tym
z rachunku.

> „`system_prompt` w telemetrii to inna nazwa na `always_apply`."

Nie. `system_prompt` to **nazwa pola w liczniku tokenów**, nie typ reguły.
Treść reguł `always_apply` tam ląduje, ale to nie to samo pojęcie — i mylenie
ich prowadzi do złych wniosków przy diagnozie.
