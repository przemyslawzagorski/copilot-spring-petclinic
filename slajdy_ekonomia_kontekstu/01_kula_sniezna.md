# 01 — Efekt kuli śnieżnej: zajętość kontekstu i tury

## Analogia

Wyobraź sobie rozmowę, w której obowiązuje jedna zasada: **zanim powiesz kolejne
zdanie, musisz na głos powtórzyć całą dotychczasową rozmowę od początku.**

Pierwsze zdanie jest tanie. Dziesiąte wymaga przeczytania dziewięciu
poprzednich. Trzydzieste — dwudziestu dziewięciu.

To nie jest metafora. **To dosłownie tak działa.** Model nie ma pamięci między
wywołaniami. Za każdym razem dostaje komplet: instrukcję systemową, opis
wszystkich narzędzi i całą historię. Jedyne, co się zmienia, to że historia
z każdą turą jest dłuższa.

## Mechanizm

Każda tura wysyła ponownie trzy rzeczy:

1. **System prompt** — stały
2. **Katalog narzędzi** — stały, opisany w [module 04](04_katalog_narzedzi.md)
3. **Cała historia** — rośnie

Punkty 1 i 2 to koszt, który płacisz zanim agent cokolwiek zrobi. W naszym
pomiarze to **20 284 tokeny**. Identyczne dla każdego modelu, bo to ta sama
konfiguracja.

## Zmierzone

To samo zadanie, dwa modele, zajętość tura po turze:

| Model | Tury | Zajętość narastająco |
|---|---:|---|
| `haiku4.5` | 4 | 20 284 → 29 343 → 38 260 → 45 335 |
| `sonnet4.6` | 7 | 20 284 → 22 592 → 26 031 → 29 086 → 31 251 → 32 231 → 32 673 |

Dwie rzeczy warte uwagi:

**Oba startują z 20 284.** To stały prefiks — zapłacony, zanim którykolwiek
model cokolwiek zrobił. Różnica między modelami bierze się wyłącznie z tego,
co każda tura dołożyła.

**`haiku4.5` w 4 turach urósł bardziej niż `sonnet4.6` w 7.** Mniejszy model
dokładał więcej na turę i potrzebował grubszych kroków. To zapowiedź
[modułu 08](08_wybor_modelu.md).

## Uwaga terminologiczna, która zmienia liczby

**Tura ≠ wywołanie narzędzia.**

Tura to jedna **rozliczana runda**. W jednej rundzie model może wywołać kilka
narzędzi — dostawca nie wycenia ich osobno i nie da się ich osobno policzyć.

Te dwie liczby potrafią różnić się **nawet czterokrotnie**. Jeśli ktoś mówi
„zadanie zajęło 40 kroków", a rachunek pokazuje 10 tur — obie liczby mogą być
prawdziwe. Zawsze dopytaj, którą podano.

## Co z tego wynika

Koszt sesji nie jest sumą kosztów kolejnych pytań. Jest **sumą narastających
prefiksów**. Zadanie na 30 tur nie kosztuje 30 × „jedno pytanie" — kosztuje
tyle, ile wyjdzie z sumowania rosnącego bufora.

Stąd trzy wnioski, które rozwijają kolejne moduły:

- Stały prefiks warto obciąć raz i mieć spokój → [moduł 04](04_katalog_narzedzi.md)
- Rosnącą historię ratuje cache — ale tylko przez 5 minut → [moduł 02](02_cache_5_minut.md)
- Suma po wielu turach jest tym, co widać na fakturze → [moduł 03](03_male_zadania.md)

## Częsty błąd

> „Ograniczę liczbę tur flagą i będzie taniej."

Nie będzie. Limit tur nie zmniejsza kosztu tury — **przerywa pracę w połowie**.
Dostajesz niedokończone zadanie za prawie te same pieniądze, a potem płacisz
drugi raz za dokończenie. W naszej tabeli 16 konfiguracji warianty z ostrym
limitem tur dawały ocenę **0/3** przy oszczędności, która nie miała żadnej
wartości, bo zadanie nie zostało wykonane.

Działającą dźwignią jest **prośba o mniej tur w prompcie**, nie twardy limit.
Reguła oszczędnościowa skróciła pętlę z 4 do 3 tur przy niezmienionej ocenie
3/3 — zysk −24,5% w naszym powtórzeniu (−31,5% w pierwotnym pomiarze).
