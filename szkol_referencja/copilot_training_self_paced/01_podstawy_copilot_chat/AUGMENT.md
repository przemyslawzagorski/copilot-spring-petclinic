# Moduł 01 - Podstawy: adaptacja dla Augmenta

> Oryginalne ćwiczenia są dla GitHub Copilot w VS Code. W Auggie CLI wykonaj
> te same cele, używając poniższych odpowiedników. Na Windows pracuj w WSL.

## Mapa interfejsu

| GitHub Copilot | Auggie CLI |
|---|---|
| Chat view | `auggie` w terminalu |
| Ask | `/ask` |
| Plan | `/plan` |
| Agent | `/task` lub zwykły prompt z narzędziami |
| Quick Chat | `/btw <pytanie>` |
| `@workspace` | Automatycznie indeksowane repo |
| `#file` | Ścieżka pliku albo `@nazwa-pliku` |
| Ulepszenie promptu | `Ctrl+P` |

## Ex 01 (Auggie): pytanie o projekt

Uruchom `auggie`, przełącz na `/ask` i wpisz:

```text
Jaki framework używa ten projekt? Jakie są główne encje domenowe?
Odpowiedz w 5 punktach i wskaż pliki źródłowe.
```

Sprawdź `/context`, aby zobaczyć wykorzystanie kontekstu.

## Ex 02 i 02b (Auggie): edycje kodu

Najpierw użyj `/plan` dla refaktoryzacji `VetController.showVetList`. Po
zaakceptowaniu planu poproś o implementację. Dla edycji wieloplikowej wskaż
encję, szablon i testy w jednym prompcie. Wynik obejrzyj przez `/diffs`.

## Ex 03 i 03b (Auggie): Javadoc i kolejne zmiany

Poproś o polski Javadoc w konkretnej klasie. Auggie nie jest zamiennikiem Tab
completion w edytorze; zamiast tego poproś: `Kontynuuj ten wzorzec dla
pozostałych publicznych metod`.

## Ex 04 (Auggie): terminal

```text
Uruchom najwęższy test dla VetController. Pokaż wynik i nie zmieniaj kodu.
```

Auggie użyje `launch-process`. Destrukcyjne komendy blokują permissions i hooki
repozytorium. Szczegóły: `../../augment_guide/README.md`.