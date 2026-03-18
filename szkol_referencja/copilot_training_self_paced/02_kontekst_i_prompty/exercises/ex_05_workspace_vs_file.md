# Ex 05: @workspace vs #file — różnica zakresów

> Faza 2 · ~8 min · Źródło: moduł 05

**Po co:** Zrozumieć KIEDY dać Copilotowi cały projekt, a kiedy wskazać konkretny plik. To klucz do dobrego prompta.

## Co zrobić

**Krok A — szeroki kontekst:**
```
@workspace Opisz architekturę warstw tego projektu i relacje między kontrolerami a repozytoriami.
```

**Krok B — wąski kontekst (otwórz OwnerController.java):**
```
#file:OwnerController.java Jakie metody HTTP obsługuje ten kontroler? Wymień je w tabeli: metoda HTTP | ścieżka | co robi.
```

## Porównaj odpowiedzi

- **@workspace** → ogólne, architektoniczne, może pominąć detale
- **#file** → precyzyjne, trafne, ale nie widzi reszty projektu

**Zasada:** Używaj `@workspace` na pytania "co i gdzie", `#file` na pytania "jak dokładnie".

**Więcej:** `02_kontekst_i_prompty/README.md` — sekcja o scoping kontekstu
