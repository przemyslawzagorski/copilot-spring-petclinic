# 03 — Dlaczego warto rozbijać na małe zadania

> **Uwaga na wstępie — sprostowanie popularnej tezy.**
>
> Krąży przekonanie, że „po 30 turach dobijasz do 200 000 tokenów kontekstu
> i dlatego trzeba rozbijać zadania". **Nasze pomiary tego nie potwierdzają.**
>
> W 226 sesjach: historia **osiąga plateau** (mediana 23 262 tokeny przez
> pierwsze 25 wywołań, ~64 000 od pięćdziesiątego — działa okno przesuwne),
> **żadna** sesja nie została automatycznie skompaktowana, a okno 200 000
> przekroczyły **3 wywołania z 23 165**.
>
> Wniosek o rozbijaniu zadań jest słuszny. **Ale nie z tego powodu** — i warto
> znać prawdziwy, bo prowadzi do innych decyzji.

## Analogia

Kropla z nieszczelnego kranu waży tyle, co nic. Rachunek za wodę pod koniec
kwartału potrafi być zaskakujący.

Cache read jest tani — **0,1× stawki**. Problem w tym, że mnożysz go przez
liczbę tur, a potem przez liczbę zadań w miesiącu.

## Prawdziwy mechanizm

**Tanie razy dużo to nadal dużo.**

100 000 tokenów historii × 30 tur = **3 miliony tokenów cache read**.

Każdy z nich kosztuje grosze. Suma — nie. I nie ma tu żadnego alarmu,
przekroczonego limitu ani ostrzeżenia. Wszystko działa poprawnie, po prostu
narasta.

## Zmierzone

Rozkład, który to potwierdza — z korpusu 226 sesji:

| p50 | p95 |
|---:|---:|
| 9 tur | 100 tur |

Mediana zadania to **dziewięć tur**. Ale ogon jest długi, i to on płaci
rachunek:

> **22% zadań przekraczających 30 tur zużywa 72,8% wszystkich tokenów.**

Jedna piąta zadań to prawie trzy czwarte kosztu. To jest miejsce, w którym
warto interweniować — nie w medianie.

## Dlaczego rozbicie pomaga

Trzy niezależne powody, każdy wystarczający:

**1. Krótsza pętla to mniejsza suma prefiksów.** Zadanie na 3 tury sumuje trzy
narastające bufory. Na 30 tur — trzydzieści, każdy grubszy od poprzedniego.
Zależność nie jest liniowa.

**2. Zadanie źle postawione rozłazi się właśnie w ogonie.** Zadania powyżej
30 tur to zwykle nie „zadania trudne", tylko **zadania niedoprecyzowane** —
agent szuka, wraca, próbuje inaczej. Każda taka próba jest opłacana pełnym
buforem.

**3. Po skończonym podzadaniu masz naturalny moment na reset.** A jeśli minęło
5 minut, ten reset jest darmowy — patrz [moduł 02](02_cache_5_minut.md).

## Co robić

**Formułuj zadanie tak, żeby dało się skończyć w kilku turach.** Nie „ogarnij
moduł płatności", tylko „dodaj walidację kwoty w `PaymentController`, test
jednostkowy do tego, nic więcej".

**Poproś o mniej tur w prompcie** — to działa. Reguła oszczędnościowa skróciła
pętlę z 4 do 3 tur przy niezmienionej ocenie 3/3, dając **−24,5%**. Ważniejsze
od samego procentu: **zniknęła wariancja liczby tur**. Przewidywalność bywa
cenniejsza niż oszczędność.

**Nie ustawiaj twardego limitu tur jako oszczędności.** To nie działa i
[moduł 01](01_kula_sniezna.md) pokazuje dlaczego. Limit ma sens wyłącznie jako
**bezpiecznik przed ucieczką** — przy p95 = 100 tur, próg ~60 zostawia 88,7%
realnych zadań nietkniętych, a łapie tylko te, które i tak się zapętliły.

## Częsty błąd

> „Rozbiję na małe zadania, więc będę częściej robił reset."

Uwaga: jeśli pracujesz **ciągle**, reset między podzadaniami **kosztuje**.
Wyrzucasz cache, za który zapłaciłeś, i przeliczasz prefiks od nowa po 1,25×.

Rozbijaj **zadania**, nie **sesje**. To dwie różne rzeczy. Sesję resetuj wtedy,
gdy cache i tak wygasł — czyli po przerwie dłuższej niż pięć minut.
