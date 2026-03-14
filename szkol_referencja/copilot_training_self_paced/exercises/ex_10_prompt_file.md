# Ex 10: Reużywalny plik promptu (.prompt.md)

> Faza 3 · ~8 min · Źródło: moduł 03

**Po co:** Prompt file to "makro" — zapisujesz raz, wołasz wielokrotnie. Standaryzuje powtarzalne zadania w zespole.

## Co zrobić

1. Utwórz plik `.copilot/prompts/create_service.prompt.md`:

```markdown
---
description: "Stwórz nowy serwis Spring z repozytorium i testami"
---
Dla podanej encji stwórz:
1. Interfejs serwisu w pakiecie `service/`
2. Implementację z wstrzykniętym repozytorium (@Service, constructor injection)
3. Metody: findAll, findById, save, deleteById
4. Test jednostkowy z Mockito dla każdej metody

Użyj konwencji tego projektu (Spring Boot 3.x, JUnit 5).
```

2. Teraz wywołaj go — w Copilot Chat kliknij ikonę załącznika (spinacz) lub wpisz `/` i wybierz swój prompt.
3. Podaj kontekst: "Stwórz serwis dla encji Vet."

**Spodziewany wynik:** Copilot wygeneruje VetService (interfejs + implementacja) i VetServiceTest.

**Tip:** Prompt files działają jak szablony zespołowe. Wrzuć je do repo i cały zespół ma ten sam standard.

**Więcej:** `03_module_03/EXERCISES.md` — ćwiczenie 2
