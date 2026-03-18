# Ex 02b: Edycja wielu plików w trybie Agent

> Bonus · ~10 min · Między ex_02 a ex_03

**Po co:** Inline chat (Ctrl+I) działa na jednym fragmencie. **Agent** (Ctrl+Alt+I) potrafi edytować wiele plików jednocześnie z jednego promptu — to główny tryb pracy przy większych zmianach.

## Co zrobić

1. Otwórz Chat view: **Ctrl+Alt+I**
2. Upewnij się, że wybrany jest tryb **Agent** (domyślny — widoczny u góry okna czatu)
3. Wpisz prompt:

```
Dodaj pole "email" (String, opcjonalny, walidacja @Email) do encji Owner.
Zaktualizuj kontroler (formularz tworzenia i edycji) i repozytorium (metoda findByEmail).
Nie usuwaj istniejących pól.
```

4. Agent przejrzy strukturę projektu, znajdzie odpowiednie pliki i zaproponuje zmiany w wielu plikach naraz. Przejrzyj diff dla każdego pliku — możesz zaakceptować/odrzucić per plik.

**Spodziewany wynik:** Zmiany w 3+ plikach jednocześnie: nowe pole w encji, nowa metoda w repo, zaktualizowane formularze w kontrolerze.

## Kiedy który tryb?

| Tryb | Skrót | Kiedy? |
|------|-------|--------|
| **Agent** (Chat view) | Ctrl+Alt+I | Zmiany w wielu plikach, złożone zadania, autonomiczna praca |
| **Inline Chat** | Ctrl+I | Szybka zmiana w zaznaczonym fragmencie |
| **Quick Chat** | Ctrl+Shift+Alt+L | Szybkie pytanie bez otwierania panelu |

## 3 wbudowane tryby agentów

- **Agent** — autonomicznie edytuje pliki, uruchamia terminal, używa narzędzi
- **Ask** — tylko odpowiada na pytania, nie modyfikuje plików
- **Plan** — tworzy plan krok po kroku, ale czeka na Twoje potwierdzenie przed zmianami

**Tip:** Im precyzyjniej opiszesz co zmienić, tym lepszy wynik. Agent sam znajdzie pliki — nie musisz ich wskazywać ręcznie.
