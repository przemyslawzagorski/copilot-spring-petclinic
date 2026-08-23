# 05 — Świadomość i obserwacja

## Analogia

Rachunek za prąd przychodzi raz na dwa miesiące i jest jedną liczbą. Bez
licznika na każdym urządzeniu nie wiesz, czy płacisz za lodówkę, za ogrzewanie,
czy za zapomniany grzejnik w piwnicy.

Wszystkie poprzednie moduły opisują dźwignie. **Ten opisuje licznik** — bez
niego nie wiesz, którą pociągnąć, i nie wiesz, czy pociągnięcie pomogło.

## Zasada nadrzędna

> **Zmierz, zanim cokolwiek zmienisz.**

Nie dlatego, że pomiar jest cnotą. Dlatego, że **bez punktu odniesienia nie
odróżnisz poprawy od przypadku** — a wariancja między przebiegami tego samego
zadania bywa większa niż efekt optymalizacji.

## Co mierzyć

Trzy poziomy, w kolejności użyteczności:

### 1. Stały koszt konfiguracji

Ile płacisz, **zanim agent cokolwiek zrobi**. To najważniejsza liczba, bo
mnoży się przez każdą turę każdej sesji.

Metoda: uruchom trywialne zadanie (jedno, na które odpowiedź jest natychmiastowa)
i odczytaj zajętość pierwszej tury. U nas: **20 284 tokeny** przy pełnym
katalogu, **11 545** po cięciu.

To jest liczba, którą warto znać na pamięć dla swojej konfiguracji.

### 2. Rozbicie bieżącego kontekstu

Co siedzi w oknie **w tej chwili** i w jakich proporcjach. W trybie
interaktywnym służy do tego polecenie `/context`.

Uwaga na interpretację: to pokazuje stan **już opłacony**. Przydaje się do
diagnozy („dlaczego mam 90 000 tokenów po trzech pytaniach?"), nie do
oszczędzania w locie.

### 3. Koszt przebiegu, nie wywołania

Najczęstszy błąd w pomiarach. **Licz koszt całego zadania**, nie pojedynczej
tury — bo optymalizacja, która obniża koszt tury i podnosi liczbę tur, jest
stratą przebraną za zysk.

Dokładnie to zobaczyliśmy przy modelach: `haiku4.5` ma niższą stawkę i wypadł
**+14,2% drożej** od bazy, bo potrzebował 6 tur zamiast 4.
Patrz [moduł 08](08_wybor_modelu.md).

## Pola zużycia, które warto czytać

Odpowiedź API zawiera rozbicie. Trzy pola i jedna pułapka:

| Pole | Znaczenie | Stawka |
|---|---|---:|
| `cache_read_input_tokens` | odtworzone z cache | 0,1× |
| `cache_creation_input_tokens` | zapisane do cache | 1,25× |
| `input_tokens` | **tylko niezcache'owana reszta** | 1× |

> **Pułapka:** `input_tokens` to **nie** rozmiar promptu. To resztka, która nie
> trafiła do cache. Agent, który pracował godzinę, może pokazywać `input_tokens`
> rzędu 4 000 — reszta poszła przez cache.
>
> **Rozmiar promptu = suma wszystkich trzech pól.**

Ta pułapka jest powodem, dla którego wiele „pomiarów" zaniża koszt
kilkudziesięciokrotnie.

## Pułapka, która psuje wszystkie kolejne pomiary

Zanim uwierzysz w jakikolwiek wynik, sprawdź, **czy plik sesji w ogóle
powstał**. Jeśli po zakończeniu przebiegu nie ma nowego pliku sesji — nie
mierzyłeś tego, co myślisz, że mierzyłeś. Odczytujesz wtedy poprzedni przebieg
albo pustkę, a liczby wyglądają wiarygodnie.

Jest to na tyle częste, że warto mieć to jako pierwszy krok każdego pomiaru,
przed patrzeniem na jakiekolwiek tokeny.

## Czego CLI Ci nie powie

Narzędzie pokazuje część obrazu, ale nie całość. W szczególności:

- **Tury a wywołania narzędzi** — rozliczana jest tura, a interfejs często
  pokazuje kroki. Różnica bywa czterokrotna
  ([moduł 01](01_kula_sniezna.md))
- **Wygaśnięcie cache** — nic tego nie sygnalizuje. Ta sama sesja, ten sam
  ekran, 31× wyższy koszt tury ([moduł 02](02_cache_5_minut.md))
- **Koszt narzędzi nigdy nieużytych** — nie ma wiersza „zapłaciłeś za
  subagentów, których nie wywołałeś"

Wszystkie trzy trzeba zmierzyć samodzielnie. Żadnej z nich nie zobaczysz,
patrząc na ekran.

## Co robić

**Ustal swoją linię bazową** — stały koszt konfiguracji, zapisz.

**Mierz przebiegami, nie turami** — i zawsze z oceną jakości. Tabela z
[modułu 04](04_katalog_narzedzi.md) ma kolumnę „Ocena" nie dla ozdoby: bez niej
wariant za 4 571 tokenów wygląda jak zwycięzca, a jest zadaniem niewykonanym.

**Powtórz pomiar co najmniej trzy razy.** Wariancja między przebiegami tego
samego zadania jest realna. Pojedynczy przebieg nie jest pomiarem.

**Zawsze miej ramię kontrolne.** Dlaczego — [moduł 10](10_pulapki_pomiaru.md).

## Częsty błąd

> „Widzę w interfejsie, ile tokenów zużyłem, to mi wystarczy."

Nie wystarczy, z trzech powodów. Widzisz **jedną liczbę zamiast rozbicia**
(nie wiesz, ile poszło po 0,1×, a ile po 1,25×). Widzisz **stan, nie trend**
(nie wiesz, czy rośnie szybciej niż powinno). I nie widzisz **kosztu
alternatywnego** — ile by było, gdybyś skonfigurował to inaczej.

To ostatnie jest najważniejsze i wymaga uruchomienia wariantu porównawczego.
Nie da się tego odczytać z żadnego ekranu.
