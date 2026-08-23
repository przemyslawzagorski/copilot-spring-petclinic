# 07 — Hooki: robota, za którą nie płacisz modelowi

## Analogia

Nie zatrudniasz eksperta, żeby pilnował, czy woda się zagotowała. Do tego jest
**termostat** — urządzenie deterministyczne, które robi jedną rzecz niezawodnie
i za darmo.

Hook to termostat. Model to ekspert. **Płacenie modelowi za sprawdzenie, czy
plik ma poprawne zakończenia linii, to zatrudnianie radcy prawnego do
pilnowania garnka.**

## Do czego to jest

Hook uruchamia się na zdarzenie — start sesji, przed wywołaniem narzędzia, po
zapisie pliku, przy próbie zakończenia. Wykonuje zwykły skrypt. Może
**zablokować** operację.

Wszystko, co da się rozstrzygnąć deterministycznie, powinno być tutaj, a nie
w prompcie:

| Zadanie | Prompt | Hook |
|---|---|---|
| „Nie edytuj plików w `target/`" | prośba, którą model może zignorować | **twarda blokada** |
| „Formatuj kod po zapisie" | instrukcja kosztująca tokeny w każdej turze | skrypt, koszt zerowy |
| „Nie dotykaj `.env`" | prośba | **blokada** |
| „Uruchom testy przed zakończeniem" | prośba | brama `Stop` |

Różnica nie jest tylko kosztowa. **Prompt to prośba, hook to granica.** Reguła
w prompcie działa dopóty, dopóki model uznaje ją za istotną. Hook działa zawsze.

## Pierwszy koszt: kontekst wstrzykiwany

**To jest część, którą wszyscy pomijają.**

Niektóre hooki mogą **wstrzyknąć tekst do kontekstu** — przez wyjście na stdout
albo pole `additionalContext`. Ten tekst zachowuje się dokładnie jak reguła
`always_apply`: jest doliczany do **każdego kolejnego wywołania w sesji**.

Hook, który przy starcie sesji wypisuje dziesięć ostatnich commitów, wygląda
niewinnie. Ale ten listing jedzie potem w każdej turze — trzydzieści razy przy
zadaniu na trzydzieści tur.

Możesz to zobaczyć u siebie w trzech krokach:

1. Sprawdź rozbicie kontekstu, zanotuj pozycję z instrukcjami systemowymi
2. Dopisz do hooka startowego coś obszernego (np. `git log --oneline -10`)
3. Nowa sesja, znowu rozbicie — pozycja urosła **o tyle, ile hook wypisał**

I rośnie tak przy każdym kolejnym wywołaniu, nie raz.

> **Zasada:** hook, który **coś robi**, jest darmowy. Hook, który **coś mówi**,
> kosztuje jak reguła zawsze aktywna. To rozróżnienie decyduje o tym, czy hook
> jest oszczędnością, czy ukrytym wydatkiem.

## Drugi koszt: czas

Hook blokuje przebieg na czas wykonania. Skrypt, który odpytuje sieć albo
uruchamia pełny build, zamienia szybką pętlę w wolną — i robi to przy każdym
wyzwoleniu.

Trzymaj hooki szybkie. Jeśli coś musi trwać, niech trwa raz (przy starcie sesji),
a nie przy każdym zapisie pliku.

## Dwa sposoby blokowania

Warto wiedzieć, że są dwa mechanizmy i że różnią się tym, co widzi model. Jeden
zwraca decyzję odmowną w ustrukturyzowanej formie, drugi opiera się na kodzie
wyjścia. Pierwszy pozwala przekazać modelowi **powód** odmowy — co ma znaczenie,
bo model wtedy próbuje inaczej, zamiast walić głową w mur.

Przy projektowaniu blokady zawsze podawaj powód. „Odmowa" bez uzasadnienia
kończy się tym, że agent powtarza tę samą operację.

## Ostrożnie z bramką na zakończenie

Hook blokujący zakończenie sesji potrafi stworzyć pętlę: agent chce skończyć,
hook nie pozwala, agent próbuje coś poprawić, znowu chce skończyć, hook znowu
nie pozwala. Każde okrążenie to pełna tura po pełnym koszcie.

Jeśli używasz takiej bramki, **musi mieć warunek wyjścia**, który agent jest
w stanie spełnić — i najlepiej licznik prób.

## Co robić

**Przenieś do hooków wszystko, co deterministyczne.** Formatowanie, ochrona
ścieżek, blokady na wrażliwe pliki, uruchamianie testów. Zwalnia to prompt i
działa pewniej.

**Testuj hooki offline**, zanim je podepniesz. Hook z błędem składni potrafi
zablokować całą pracę w sposób trudny do zdiagnozowania.

**Sprawdź, czy któryś hook nie wstrzykuje kontekstu bez potrzeby.** To
najczęstszy ukryty koszt w tej kategorii — i jedyny, który rośnie z długością
sesji.

## Częsty błąd

> „Napiszę w regule, żeby model nie dotykał plików produkcyjnych."

To prośba, nie zabezpieczenie. Model może ją zignorować — nie ze złej woli,
tylko dlatego, że w danym kontekście uzna inną instrukcję za ważniejszą.
Płacisz za tę prośbę w każdej turze i **nie masz gwarancji**.

Hook daje gwarancję i kosztuje zero. To rzadki przypadek, w którym tańsze
rozwiązanie jest jednocześnie mocniejsze.
