# 02 — Cache providera: kiedy działa, a kiedy nie

## Analogia

Cache to **papiery zostawione na biurku**.

Wychodzisz na minutę po kawę, wracasz — leżą dokładnie tak, jak je zostawiłeś.
Siadasz i pracujesz dalej.

Wychodzisz na kwadrans, wracasz — **biurko jest sprzątnięte.** Wszystko trzeba
wydrukować od nowa.

I najgorsze: **nic Ci o tym nie powie.** Ta sama sesja, ta sama historia na
ekranie, ten sam znak zachęty. Jedyna różnica jest na rachunku.

## Mechanizm

Cache dostawcy działa na zasadzie **dopasowania prefiksu**. Zapytanie jest
składane zawsze w tej samej kolejności:

```
narzędzia  →  system prompt  →  wiadomości
```

Dopasowanie idzie od początku. **Zmiana jednego bajtu w dowolnym miejscu
unieważnia wszystko, co jest po nim.** Nie „trochę mniej trafień" — całą resztę.

Stawki (dokumentacja Anthropica):

| Operacja | Koszt względem input |
|---|---:|
| Odczyt z cache | **0,1×** |
| Zapis do cache (TTL 5 min) | **1,25×** |
| Zapis do cache (TTL 1 h) | **2×** |

## Zmierzony klif

To jest najważniejsza liczba w całym materiale. **159 sesji, 24 680 przejść
między turami.** Dla każdej tury policzyliśmy odstęp od poprzedniej:

| Odstęp od poprzedniej tury | Udział cache read | Śr. cache creation na turę |
|---|---:|---:|
| < 1 min | **97,4%** | 3 409 |
| 1–5 min | **95,9%** | 5 375 |
| **5–15 min** | **15,7%** | **105 853** |
| 15–60 min | 3,1% | 102 982 |
| > 60 min | 2,8% | 96 112 |

**Klif jest dokładnie na pięciu minutach.** To domyślny TTL cache Anthropica,
a pomiar potwierdza, że narzędzie używa właśnie jego.

Skok cache creation z ~3 400 do ~106 000 tokenów na turę: **31×**.

## Co to rozstrzyga

Istnieją dwie popularne, sprzeczne rady. **Obie są prawdziwe — w różnych
sytuacjach**, i dopiero pomiar pokazuje w których.

> **„Długie sesje są tanie."** Prawda dla pracy **ciągłej**. Dopóki piszesz co
> kilka minut, 97% kontekstu odtwarza się z cache po 0,1× stawki.

> **„Kończ sesje, żeby resetować kontekst."** Prawda **po przerwie**. Cache i
> tak wygasł, więc przeliczenie prefiksu zapłacisz niezależnie od tego, czy
> zrobisz reset, czy nie.

Nie chodzi o długość sesji. **Chodzi o jej ciągłość.**

## Jedyna reguła do zapamiętania

> ### Przerwa dłuższa niż 5 minut to darmowy moment na reset
>
> Cache creation zapłacisz tak czy inaczej. **Więc lepiej zapłacić za kondensat
> 5 000 tokenów niż za 100 000 tokenów historii.**

Wracasz po obiedzie? Zrób podsumowanie stanu w kilku zdaniach, otwórz nową
sesję, wklej. Kosztuje tyle, co nic, a alternatywa to przeliczenie całej
historii po stawce 1,25×.

Wracasz po dwóch minutach? **Nie dotykaj niczego.** Reset w pracy ciągłej to
czysta strata — wyrzucasz cache, za który już zapłaciłeś.

## Kiedy TTL 1 godzina ma sens

Dłuższy TTL kosztuje 2× przy zapisie zamiast 1,25×. Rachunek progu opłacalności:

| TTL | Próg opłacalności |
|---|---|
| 5 min | **2 zapytania** (1,25× + 0,1× = 1,35× wobec 2× bez cache) |
| 1 h | **3 zapytania** (2× + 0,2× = 2,2× wobec 3× bez cache) |

Godzinny TTL opłaca się przy pracy **zrywami z długimi przerwami** — gdy wiesz,
że wrócisz do tej samej sesji, ale nie w ciągu pięciu minut. Przy pracy ciągłej
to przepłacanie.

## Co cicho psuje cache

Te rzeczy unieważniają cache bez żadnego komunikatu. Warto ich poszukać
u siebie:

| Wzorzec | Dlaczego psuje |
|---|---|
| `datetime.now()` w system prompcie | Prefiks inny przy każdym zapytaniu |
| UUID / identyfikator sesji na początku | To samo |
| Serializacja JSON bez sortowania kluczy | Bajty się różnią mimo tej samej treści |
| Zmiana katalogu narzędzi w trakcie | Narzędzia są na pozycji 0 — unieważniają **wszystko** |
| Zmiana modelu w trakcie | Cache jest per model |

Hierarchia unieważnień jest warstwowa i warto ją znać, bo nie wszystko boli
tak samo:

| Co zmieniasz | Cache narzędzi | Cache systemu | Cache wiadomości |
|---|:---:|:---:|:---:|
| Definicje narzędzi | ❌ | ❌ | ❌ |
| Model | ❌ | ❌ | ❌ |
| Treść system promptu | ✅ | ❌ | ❌ |
| Treść wiadomości | ✅ | ✅ | ❌ |

Czyli: dopisanie zdania do rozmowy jest tanie. **Dorzucenie jednego narzędzia
w połowie sesji kasuje wszystko.**

## Jak sprawdzić, czy cache działa

Odpowiedź API zawiera pola zużycia:

- `cache_read_input_tokens` — ile poszło z cache (płacisz 0,1×)
- `cache_creation_input_tokens` — ile zapisano (płacisz 1,25×)
- `input_tokens` — **tylko niezcache'owana reszta**

Ostatnie pole myli najczęściej. Jeśli agent pracował godzinę, a `input_tokens`
pokazuje 4 000 — to nie znaczy, że było tanio. Reszta poszła przez cache.
**Sumuj wszystkie trzy pola**, nie patrz na jedno.

Jeśli `cache_read_input_tokens` jest zerowe przy powtarzanych zapytaniach —
masz jednego z cichych zabójców z tabeli wyżej.

## Częsty błąd

> „Włączę cache i będzie taniej."

Cache przy **jednym** zapytaniu jest droższy niż jego brak — płacisz 1,25×
zamiast 1×. Zwraca się dopiero od drugiego odczytu. Jeśli każde Twoje zapytanie
ma inny początek, cache tylko dokłada narzut.

Minimalny cache'owalny prefiks zależy od modelu i **nie rośnie liniowo
z generacjami** — bywa 512 tokenów, bywa 4096. Poniżej progu cache po prostu
nie powstaje, bez żadnego błędu: `cache_creation_input_tokens` wynosi zero
i tyle.
