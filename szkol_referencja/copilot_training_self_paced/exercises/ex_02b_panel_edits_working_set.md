# Ex 02b: Panel Edits — refaktor wielu plików naraz

> Bonus · ~10 min · Między ex_02 a ex_03

**Po co:** Inline chat (Ctrl+I) działa na jednym pliku. **Panel Edits** pozwala zmieniać wiele plików jednocześnie z jednego promptu — to główny tryb pracy przy większych zmianach.

## Co zrobić

1. Otwórz panel Copilot Edits: **Ctrl+Shift+I** → przełącz na tryb **Edits** (ikona ołówka u góry okna czatu)
2. Dodaj pliki do **Working Set** — kliknij "Add Files" i dodaj:
   - `OwnerController.java`
   - `Owner.java`
   - `OwnerRepository.java`

3. Wpisz prompt:

```
Dodaj pole "email" (String, opcjonalny, walidacja @Email) do encji Owner. Zaktualizuj kontroler (formularz tworzenia i edycji) i repozytorium (metoda findByEmail). Nie usuwaj istniejących pól.
```

4. Copilot pokaże diff dla KAŻDEGO pliku w Working Set. Przejrzyj zmiany — możesz zaakceptować/odrzucić per plik.

**Spodziewany wynik:** Zmiany w 3 plikach jednocześnie: nowe pole w encji, nowa metoda w repo, zaktualizowane formularze w kontrolerze.

**Kiedy Edits zamiast Chat?**
- Chat → pytania, analiza, jeden plik
- Edits → modyfikacje kodu w wielu plikach naraz
- Inline (Ctrl+I) → szybka zmiana w zaznaczeniu

**Tip:** Working Set kontroluje zakres — im precyzyjniej dodasz pliki, tym lepsze wyniki. Nie dodawaj 20 plików "na wszelki wypadek".
