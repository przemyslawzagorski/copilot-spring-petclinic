# Ex 06c: Characterization Test — bezpieczny refaktor

> Bonus · ~10 min · Między ex_06b a ex_07

**Po co:** Zanim refaktoryzujesz legacy code, NAJPIERW uchwyć jego aktualne zachowanie testem. Characterization test nie sprawdza "czy jest poprawnie" — sprawdza "co robi TERAZ".

## Co zrobić

1. Otwórz `OwnerController.java`
2. W Copilot Chat wpisz:

```
#file:OwnerController.java Wygeneruj characterization test dla metody processFindForm. Test NIE waliduje poprawności, tylko uchwytuje AKTUALNE zachowanie:
- Co zwraca gdy lastName jest pusty?
- Co zwraca gdy jest 0 wyników?
- Co zwraca gdy jest dokładnie 1 wynik?
- Co zwraca gdy jest >1 wyników?
Użyj MockMvc, JUnit 5. Nazwij klasę OwnerControllerCharacterizationTest.
```

3. Skopiuj wygenerowany test do `src/test/java/.../owner/OwnerControllerCharacterizationTest.java`
4. Uruchom: `.\mvnw.cmd test -Dtest=OwnerControllerCharacterizationTest`

**Spodziewany wynik:** Wszystkie testy PRZECHODZĄ — bo testują to, co metoda faktycznie robi, nie to co "powinna".

## Po co to?

Teraz masz "siatkę bezpieczeństwa". Jeśli zrefaktoryzujesz `processFindForm` (np. w ex_02), characterization test złapie regresję.

**Workflow:** Characterization Test → Refaktor → Testy przechodzą → bezpiecznie.

**Kiedy stosować?** Przy każdym refaktorze legacy kodu, którego nie napisałeś i nie rozumiesz w 100%.
