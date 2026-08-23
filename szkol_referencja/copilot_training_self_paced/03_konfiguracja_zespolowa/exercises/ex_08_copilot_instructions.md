# Ex 08: Twój pierwszy copilot-instructions.md

> Faza 3 · ~8 min · Źródło: moduł 03 + 06

**Po co:** Ten plik zmienia zachowanie Copilota dla CAŁEGO repozytorium. Jak firmowy styl promptowany raz, działa zawsze.

> 📁 **Ten plik już istnieje w repo.** `.github/copilot-instructions.md` jest
> jednym z „żywych przykładów" wymienionych w START_HERE. Nie twórz go od zera —
> otwórz i pracuj na nim.

## Co zrobić

1. Otwórz `.github/copilot-instructions.md` i przeczytaj. Zwróć uwagę, że
   reguły są **konkretne i sprawdzalne** („JUnit 5, nigdy JUnit 4"), a nie
   życzeniowe („pisz dobry kod").

2. **Zanim przetestujesz — zepsuj go celowo.** Zakomentuj albo usuń linię
   o testach:

```markdown
- Testy: JUnit 5 + Mockito. Nigdy JUnit 4.
```

3. W **nowym** chacie wpisz:

```
Napisz test jednostkowy dla klasy Owner.
```

Zanotuj, czy dostałeś JUnit 4 czy 5.

4. Przywróć usuniętą linię, otwórz **kolejny nowy** chat i powtórz ten sam
   prompt.

5. Teraz przetestuj całość — w nowym chacie wpisz:

```
Wygeneruj nową encję Appointment z polami: date, description, pet. Dodaj repozytorium.
```

**Spodziewany wynik:** Copilot użyje Java 17+, Spring Data JPA, Javadoc po polsku — zgodnie z instrukcjami.

**Wynik kroków 2–4 jest ciekawszy:** bez tej jednej linii Copilot potrafi
sięgnąć po JUnit 4, bo tak wygląda większość przykładów w internecie. Z linią —
trzyma się JUnit 5. Widzisz na własne oczy, że jedno zdanie w tym pliku realnie
przestawia wynik, i że **plik działa dopiero w nowej sesji chatu**.

**Nie działa?** Zamknij i otwórz ponownie chat po zapisaniu pliku. Instructions ładują się przy starcie sesji.

> 🧹 **Posprzątaj:** upewnij się, że przywróciłeś usuniętą linię, zanim
> przejdziesz dalej. Kolejne ćwiczenia zakładają komplet reguł.

**Więcej:** `03_konfiguracja_zespolowa/README.md` — sekcja Custom Instructions
