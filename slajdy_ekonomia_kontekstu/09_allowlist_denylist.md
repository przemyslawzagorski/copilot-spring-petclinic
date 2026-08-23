# 09 — Allowlist vs denylist: jak uprawnienia starzeją się w złą stronę

## Analogia

Organizujesz przyjęcie. Masz dwa sposoby pilnowania drzwi:

**Lista gości** — wpuszczamy wymienionych. Ktoś, kogo nie ma na liście, nie
wejdzie.

**Lista niewpuszczanych** — wpuszczamy wszystkich poza wymienionymi.

Dopóki znasz wszystkich, obie działają. Ale świat produkuje nowych ludzi.
**Nowa osoba przy liście gości nie wejdzie. Przy liście niewpuszczanych —
wejdzie.**

Ta asymetria jest całym modułem.

## Mechanizm

Zestaw narzędzi agenta można ograniczyć dwojako:

| | Nowe narzędzie w systemie | Wybierz, gdy |
|---|---|---|
| **Allowlist** (lista dozwolonych) | **niedostępne**, dopóki nie dopiszesz | zależy Ci na przewidywalności |
| **Denylist** (lista zakazanych) | **dostępne od razu** | zależy Ci na wygodzie |

> **Denylist starzeje się w stronę WIĘKSZYCH uprawnień. Allowlist w stronę
> MNIEJSZYCH.**

Przy profilu „tylko do odczytu" to przesądza wybór. Agent zdefiniowany
denylistą przestanie być read-only w dniu, w którym ktoś doda nowe narzędzie
zapisu — i nikt tego nie zauważy, bo nic się nie zepsuje.

## To się zdarzyło naprawdę

Uruchomiliśmy na tym warsztacie agenta-recenzenta zdefiniowanego **denylistą**
i zapytaliśmy go wprost, czym może pisać:

| Zakres | Wynik |
|---|---|
| Pliki w katalogu roboczym | **Nie może.** Denylist zadziałał — żadne z wymienionych narzędzi zapisu nie utworzyło pliku |
| Systemy zewnętrzne | **Może.** Zakładanie ticketów, tworzenie stron wiki, zapis do repozytorium, wypychanie commitów, otwieranie merge requestów |

Nikt tych uprawnień nie nadawał. Pochodzą z **serwera MCP podpiętego już po
napisaniu definicji agenta** — a denylist przepuszcza wszystko, czego nie
wymieniono z nazwy.

Agent opisany jako „recenzent bez prawa zapisu" mógł założyć ticket i wypchnąć
commit.

## Dlaczego to trudno zauważyć

Trzy powody, każdy wystarczający:

**Nic się nie psuje.** Nadmiarowe uprawnienie nie generuje błędu. Objawia się
dopiero wtedy, gdy zostanie użyte — a wtedy jest już po fakcie.

**Definicja wygląda poprawnie.** Plik z denylistą nadal wymienia wszystkie
narzędzia zapisu, które wymieniał w dniu napisania. Zmienił się świat wokół,
nie plik.

**Serwery MCP dokładają narzędzia poza polem widzenia.** Podpinasz serwer dla
jednej funkcji, dostajesz komplet — łącznie z operacjami zapisu, o których nie
myślałeś w kategoriach uprawnień agenta.

## Jak sprawdzić u siebie

Nie zgaduj z pliku konfiguracyjnego. **Zapytaj agenta.**

```
Wypisz, które narzędzia zapisu MASZ dostępne, a których nie. Podaj nazwy.
```

To jedno pytanie i odpowiedź jest jednoznaczna. Konfiguracja mówi, co
wyłączyłeś. Agent mówi, co mu zostało — a to jest pytanie, które ma znaczenie.

## Co robić

**Dla profilu read-only używaj allowlisty.** Zawsze. Wygoda denylisty nie jest
warta uprawnienia, które pojawi się samo.

**Po podpięciu każdego serwera MCP powtórz pytanie kontrolne.** To jest moment,
w którym uprawnienia się zmieniają, i jedyny, w którym łatwo to złapać.

**Nazywaj agentów precyzyjnie.** „Recenzent bez prawa zapisu" to obietnica,
której definicja może nie dotrzymać. „Bez prawa zapisu **do plików**" jest
prawdziwe i nie usypia czujności.

## Ważne zastrzeżenie

> **Ani allowlist, ani denylist nie są granicą bezpieczeństwa.** To
> konfiguracja agenta — sposób na przewidywalność, nie na powstrzymanie kogoś
> zdeterminowanego.
>
> Twarde granice to uprawnienia systemowe i hooki blokujące
> ([moduł 07](07_hooki.md)). Jeśli operacja **musi** być niemożliwa, nie
> polegaj na liście narzędzi.

## Metodologiczny morał

To znalezisko zgłosił **sam agent-recenzent**, uruchomiony na własnym
repozytorium. Ale postawił **błędną diagnozę** — twierdził, że nazwy narzędzi
w denyliście są przestarzałe. Nie były; sprawdziliśmy.

Kierunek był trafny, uzasadnienie fałszywe, a luka realna i groźniejsza, niż
opisał.

> **Tak właśnie należy czytać wyniki agenta-recenzenta: jako trop, nie
> werdykt.** Wart sprawdzenia, niewart przyjęcia na wiarę.
