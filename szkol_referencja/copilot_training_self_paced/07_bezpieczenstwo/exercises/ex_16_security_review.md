# Ex 16: Security review pliku

> Faza 5 · ~8 min · Źródło: moduł 10

**Po co:** Copilot potrafi znaleźć luki bezpieczeństwa w kodzie. Wystarczy zapytać.

## Co zrobić

1. Otwórz `OwnerController.java`
2. W Copilot Chat wpisz:

```
#file:OwnerController.java Przeprowadź security review tego pliku. Sprawdź: walidację inputu, ochronę przed injection, brakujące adnotacje bezpieczeństwa, wycieki danych w logach. Format: tabela z kolumnami: problem | lokalizacja | severity | fix.
```

3. Przeczytaj raport i oceń trafność.

**Spodziewany wynik:** Copilot wskaże np. brak walidacji `@Valid`, potencjalny open redirect, brak CSRF (choć Spring domyślnie chroni). Niektóre uwagi mogą być false positive — i to dobrze, uczysz się oceniać.

**Tip:** Powtórz to na `VetController.java` i `application.properties` (szukanie jawnych credentials).

**Więcej:** `07_bezpieczenstwo/EXERCISES.md`
