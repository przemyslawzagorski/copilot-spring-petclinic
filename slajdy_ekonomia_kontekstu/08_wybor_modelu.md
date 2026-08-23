# 08 — Wybór modelu: cena za token to nie cena zadania

## Analogia

Kupujesz samochód, bo pali o 20% mniej na setkę. Potem okazuje się, że ma tak
słabą skrzynię, że na tej samej trasie **kręcisz o połowę więcej kilometrów**,
bo nie wyprzedzisz na prostej i jedziesz objazdem.

Cena za litr nie jest ceną przejazdu.

Stawka za token nie jest ceną zadania. **Ceną zadania jest stawka razy liczba
tur razy narastający bufor.** Model o niższej stawce, który potrzebuje więcej
tur, wychodzi drożej — i to nie o kilka procent.

## Zmierzone

To samo zadanie, ten sam katalog narzędzi, różne modele:

| Model | Tury | Tokeny | vs baza | Ocena |
|---|---:|---:|---:|:---:|
| **`gpt5.6-luna`, 2 narzędzia, `--max-turns 4`** | 4 | **23 033** | **−72,4%** | 3/3 |
| *(baza)* pełny katalog, uncapped | 4 | 83 313 | — | 3/3 |
| `haiku4.5`, pełny katalog | 6 | 95 136 | **+14,2%** | 3/3 |
| `gemini-3.1-pro-preview`, pełny katalog | 11 | 157 594 | **+89,2%** | 3/3 |

Wszystkie trzy wykonały zadanie poprawnie — **ocena 3/3 w każdym wierszu**. To
nie jest tabela o jakości. To tabela o tym, ile tur zajęło dojście do tego
samego wyniku.

`haiku4.5` ma **niższą stawkę za token** i wypadł **drożej od bazy o 14,2%**,
bo potrzebował 6 tur zamiast 4.

`gemini-3.1-pro-preview` potrzebował 11 tur — **prawie dwukrotność bazy**.

## Mechanizm

Wraca [moduł 01](01_kula_sniezna.md): każda tura opłaca cały narastający
prefiks. Więc liczba tur nie wchodzi do rachunku liniowo — wchodzi przez sumę
rosnących buforów.

Model, który potrzebuje o połowę więcej tur, nie kosztuje o połowę więcej.
Kosztuje więcej niż o połowę, bo te dodatkowe tury są **najgrubsze** — historia
jest wtedy najdłuższa.

Stąd pozornie paradoksalny wniosek:

> **Model o wyższej stawce, który trafia za pierwszym razem, bywa tańszy niż
> model o niższej stawce, który się dobija.**

## Co z tego wynika praktycznie

**Nie wybieraj modelu po cenniku.** Zmierz na swoim zadaniu — kilka przebiegów,
z oceną jakości, licząc **koszt przebiegu**, nie koszt tury.

**Mniejsze modele mają swoje miejsce, ale węższe niż się wydaje.** Sprawdzają
się przy zadaniach **mechanicznych i wąsko określonych**, gdzie liczba tur jest
z góry znana i mała: przeformatowanie, prosta konwersja, wyciągnięcie danych
według ustalonego wzorca.

Rozpadają się przy zadaniach **wymagających rozpoznania sytuacji** — bo tam
płacisz za każdą nieudaną próbę pełnym buforem.

**Rozważ różne modele dla różnych zadań.** Komenda może nadpisać model dla
siebie ([moduł 06](06_reguly_i_skille.md)) — to sensowne dla powtarzalnej,
mechanicznej roboty, którą i tak wywołujesz świadomie.

## Interakcja z katalogiem narzędzi

Najlepszy wiersz w tabeli łączy **dwie** dźwignie: inny model **i** mały
katalog — `gpt5.6-luna` z dwoma narzędziami dał −72,4%.

Sam mały katalog na modelu bazowym dał −64,2%. Sam inny model przy pełnym
katalogu potrafił dać **+89,2%**.

To sugeruje kolejność działań:

1. **Najpierw katalog** — działa niezależnie od modelu, nie kosztuje jakości
2. **Potem model** — mierząc, bo efekt bywa ujemny

Odwrotna kolejność prowadzi do wniosku „zmieniłem model i jest drożej", który
jest prawdziwy, ale niepełny.

## Częsty błąd

> „Przełączę się na tańszy model na czas tego zadania."

Dwie rzeczy naraz idą nie tak.

Po pierwsze — **może wyjść drożej**, co pokazuje tabela.

Po drugie, i to jest pułapka ukryta: **zmiana modelu w trakcie sesji unieważnia
cały cache.** Cache jest per model. Przełączenie w połowie zadania oznacza
przeliczenie całego prefiksu od nowa po stawce 1,25× —
patrz [moduł 02](02_cache_5_minut.md).

Jeśli chcesz użyć innego modelu, zrób to **od początku sesji**, nie w trakcie.
