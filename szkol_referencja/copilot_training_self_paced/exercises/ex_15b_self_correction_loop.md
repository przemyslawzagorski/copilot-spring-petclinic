# Ex 15b: Self-Correction Loop — agent naprawia własne błędy

> Bonus · ~10 min · Między ex_15 a ex_16

**Po co:** Najważniejsza supermoc Agent Mode: agent uruchamia kod, widzi błąd w terminalu, i SAM go naprawia. Pętla: kod → błąd → fix → ponowna próba.

## Co zrobić

### Krok 1: Celowo trudne zadanie

W Copilot Chat (tryb Agent) wpisz:

```
Dodaj nowy endpoint REST GET /api/owners/statistics do OwnerController.java, który zwraca JSON:
{
  "totalOwners": <liczba>,
  "totalPets": <liczba>,
  "avgPetsPerOwner": <średnia zaokrąglona do 2 miejsc>,
  "mostPopularPetType": "<nazwa>"
}
Użyj istniejących repozytoriów. Po implementacji uruchom: .\mvnw.cmd compile
```

### Krok 2: Obserwuj pętlę

1. Agent wygeneruje kod i uruchomi kompilację
2. Prawdopodobnie będą błędy (brak importu, zły typ zwracany, brakująca metoda w repo)
3. **Nie interweniuj** — obserwuj jak agent:
   - Czyta output z terminala
   - Identyfikuje błąd
   - Proponuje fix
   - Ponownie kompiluje
4. Powtarza aż do sukcesu (lub się podda po kilku próbach)

### Krok 3: Weryfikacja

```
.\mvnw.cmd compile
```

Jeśli kompilacja przechodzi — sukces. Agent sam się naprawił.

**Spodziewany wynik:** 2-4 iteracje correction loop zanim kod się skompiluje. Agent pokaże każdy krok w czacie.

**Kiedy to nie działa?** Przy błędach logicznych (kod się kompiluje, ale robi coś złego). Self-correction łapie tylko błędy kompilacji/runtime. Logikę musisz weryfikować sam (testami!).

**Wniosek:** Agent Mode ≠ autopilot. To pair programmer, który Sam naprawia literówki i brakujące importy, ale decyzje architektoniczne są Twoje.
