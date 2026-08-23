# 10 — Pułapki pomiaru: jak nie skłamać sobie w wynikach

## Analogia

Podajesz pacjentom z przeziębieniem nowy syrop. Po tygodniu 90% jest zdrowych.
**Skuteczność 90%!**

Problem w tym, że przeziębienie mija samo w tydzień. Bez **grupy kontrolnej** —
pacjentów, którzy nie dostali niczego — nie zmierzyłeś działania syropu.
Zmierzyłeś upływ czasu.

Dokładnie ten błąd popełnia się przy optymalizacji kontekstu, i to bardzo
łatwo, bo wynik zawsze wygląda przekonująco.

## Pułapka pierwsza: brak ramienia kontrolnego

Wyłączasz połowę narzędzi, uruchamiasz zadanie, wychodzi taniej. Wniosek:
wyłączenie narzędzi pomogło.

Niekoniecznie. Mogło być tak, że:

- ten przebieg trafił na krótszą ścieżkę (wariancja jest realna)
- zadanie było uruchamiane drugi raz i coś zostało w cache
- model wybrał inne podejście z powodów niezwiązanych z Twoją zmianą

**Ramię kontrolne** to ten sam przebieg, w tym samym momencie, bez zmiany.
Bez niego porównujesz z pamięcią, a pamięć jest życzliwa dla własnych hipotez.

**Naiwne ramię kontrolne też zawodzi** — jeśli „kontrola" to przebieg sprzed
tygodnia, w innej konfiguracji, na innym stanie repozytorium, to nie jest
kontrola. To drugi eksperyment.

## Pułapka druga: pomiar bez oceny jakości

To jest błąd, który potrafi zniszczyć cały wniosek. Wróćmy do tabeli
z [modułu 04](04_katalog_narzedzi.md):

| Wariant | Tokeny | vs baza | Ocena |
|---|---:|---:|:---:|
| Wszystkie narzędzia usunięte, `--max-turns 1` | 4 571 | **−94,5%** | **0/3** |
| 2 narzędzia, uncapped | 29 830 | −64,2% | **3/3** |

Bez kolumny „Ocena" pierwszy wiersz jest bezkonkurencyjnym zwycięzcą. **Z nią —
jest zadaniem niewykonanym.**

> **Każdy pomiar kosztu musi mieć obok siebie pomiar jakości.** Inaczej mierzysz,
> jak tanio da się nie zrobić roboty.

## Pułapka trzecia: mylenie tur z wywołaniami

Rozliczana jest **tura**. Interfejs często pokazuje **kroki narzędziowe**.
Różnica bywa **czterokrotna**.

Porównanie „przedtem 40 kroków, teraz 12" może opisywać zmianę kosztu
z 10 do 8 tur — czyli poprawę czterokrotnie mniejszą, niż się wydaje.

Zawsze ustal, którą wielkość podajesz, i trzymaj się jej w całym zestawieniu.

## Pułapka czwarta: pojedynczy przebieg

Wariancja między przebiegami tego samego zadania na tej samej konfiguracji
jest realna. Nasze własne powtórzenie pomiaru dało **−24,5%** tam, gdzie
pierwotny wynik mówił **−31,5%** — przy tej samej redukcji tur i tej samej
ocenie.

Oba pomiary są poprawne. Różnią się, bo tak działa wariancja.

**Minimum trzy przebiegi na wariant.** Jeden przebieg to anegdota.

## Pułapka piąta: pomiar, który nie powstał

Zanim uwierzysz w jakąkolwiek liczbę, sprawdź, czy **plik sesji w ogóle
powstał**. Jeśli nie — odczytujesz poprzedni przebieg albo pustkę.

Liczby wyglądają wtedy zupełnie wiarygodnie. To najgorszy rodzaj błędu:
cichy i przekonujący.

## Pułapka szósta: uogólnianie z jednego zadania

Wynik zmierzony na jednym zadaniu **opisuje to zadanie**.

Reguła oszczędnościowa dała −24,5% na zadaniu, które bez niej rozłaziło się na
cztery tury. Na zadaniu, które i tak zajęłoby dwie, ta sama reguła to czysty
narzut — płacisz za jej treść i nie oszczędzasz żadnej tury.

Rozdzielaj więc dwie rzeczy:

- **Kierunek** — zwykle uogólnia się dobrze („mniejszy katalog jest tańszy")
- **Wielkość efektu** — praktycznie nigdy się nie uogólnia

Do decyzji o konfiguracji używaj **rozkładów z korpusu** (p50 = 9 tur,
p95 = 100), nie liczb z pojedynczego eksperymentu.

## Lista kontrolna

Zanim ogłosisz, że coś działa:

- [ ] Ramię kontrolne **w tym samym momencie**, nie z pamięci
- [ ] Ocena jakości obok każdego kosztu
- [ ] Ustalone, czy liczysz tury czy wywołania
- [ ] Minimum trzy przebiegi na wariant
- [ ] Potwierdzone, że pliki sesji powstały
- [ ] Rozdzielony kierunek od wielkości efektu

## Częsty błąd

> „Zmierzyłem, wyszło −40%, wdrażam."

Pytanie kontrolne, które warto sobie zadać: **co musiałoby być prawdą, żeby ten
wynik był przypadkiem?**

Jeśli odpowiedź brzmi „nic, sprawdziłem wszystko z listy" — wdrażaj.

Jeśli brzmi „no, mógł trafić się krótszy przebieg" — masz jeszcze jeden pomiar
do zrobienia.
