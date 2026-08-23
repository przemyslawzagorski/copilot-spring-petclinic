# Ekonomia kontekstu — materiał źródłowy

Zestaw modułów o tym, za co realnie płacisz, pracując z agentem CLI, i które
dźwignie faktycznie działają. Każdy moduł stoi na analogii, zmierzonych
liczbach i jednej rzeczy do zrobienia.

## Skąd te liczby

Wszystkie dane liczbowe pochodzą z pomiarów na tym warsztacie, nie z materiałów
marketingowych dostawcy:

| Korpus | Zakres |
|---|---|
| **226 sesji** | katalog narzędzi, rozkład tur, wywołania narzędzi |
| **159 sesji, 24 680 przejść między turami** | zachowanie cache w funkcji odstępu czasowego |
| **16 konfiguracji jednego zadania** | punkt optymalny katalog/tury/model |
| **23 165 wywołań** | zajętość okna kontekstu |

Fakty o samym mechanizmie cache (TTL, stawki, kolejność prefiksu) pochodzą z
dokumentacji Anthropica i są oznaczone w tekście.

## Moduły

| # | Moduł | Analogia | Jedno zdanie |
|---|---|---|---|
| 01 | [Kula śnieżna](01_kula_sniezna.md) | Powtarzanie całej rozmowy | Każda tura płaci za wszystko, co było wcześniej |
| 02 | [Cache i pięć minut](02_cache_5_minut.md) | Papiery na biurku | Klif jest na 5 minucie przerwy, nie na długości sesji |
| 03 | [Małe zadania](03_male_zadania.md) | Rachunek za wodę | Tanie razy dużo to nadal dużo |
| 04 | [Katalog narzędzi](04_katalog_narzedzi.md) | Skrzynka na każdą robotę | Płacisz za każde narzędzie w każdym wywołaniu |
| 05 | [Obserwacja](05_obserwacja.md) | Prąd bez licznika | Bez pomiaru optymalizujesz po omacku |
| 06 | [Reguły i skille](06_reguly_i_skille.md) | Tatuaż vs. notatka | Reguła kosztuje zawsze, skill tylko gdy trzeba |
| 07 | [Hooki](07_hooki.md) | Termostat vs. pilnowanie garnka | Robota deterministyczna nie potrzebuje modelu |
| 08 | [Wybór modelu](08_wybor_modelu.md) | Cena za litr ≠ cena przejazdu | Tańszy model potrafi być droższy |
| 09 | [Allowlist vs denylist](09_allowlist_denylist.md) | Lista gości vs. lista wykluczonych | Denylist starzeje się w stronę większych uprawnień |
| 10 | [Pułapki pomiaru](10_pulapki_pomiaru.md) | Lek bez grupy kontrolnej | Bez ramienia kontrolnego mierzysz własne życzenia |

Do tego [LICZBY.md](LICZBY.md) — wszystkie dane w jednym miejscu, do szybkiego
sprawdzenia.

## Kolejność

Moduły 01–05 to rdzeń i mają sens czytane po kolei: 01 pokazuje mechanizm,
02 jego najważniejszą konsekwencję, 03 wynikającą stąd taktykę, 04 największą
pojedynczą dźwignię, 05 sposób sprawdzenia u siebie.

Moduły 06–10 są niezależne — bierz te, które dotyczą Twojej pracy.

## Jedno ostrzeżenie na start

Trzy rady, które słyszy się najczęściej, są **fałszywe albo nieistotne**:

| Popularna rada | Co pokazuje pomiar |
|---|---|
| „Kończ sesje, żeby resetować kontekst" | W pracy ciągłej restart **przepłaca** — cache pokrywa 97% |
| „Ograniczaj liczbę tur flagą" | Limit tur nie oszczędza, tylko przerywa w połowie |
| „Pisz po angielsku, polski kosztuje +42%" | Twoja wiadomość to 0,5% rachunku → realny wpływ ~0,21% |

Każda z nich jest rozbrojona w odpowiednim module. Wspólny mianownik: **ludzie
optymalizują to, co widzą na ekranie, a płacą za to, czego nie widzą.**
