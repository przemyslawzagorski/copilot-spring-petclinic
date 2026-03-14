# Ex 06: Iteracja promptu v1 → v2 → v3

> Faza 2 · ~10 min · Źródło: moduł 05

**Po co:** Pierwszy prompt rzadko jest idealny. Nauczysz się iterować i poprawiać wynik.

## Co zrobić

Otwórz `Owner.java` i wykonaj kolejno 3 prompty w tym samym czacie:

**v1 (za ogólny):**
```
Dodaj walidację do klasy Owner.
```

**v2 (lepszy — precyzujesz reguły):**
```
Dodaj walidację Bean Validation do pól firstName i lastName: oba niepuste, 2-30 znaków, tylko litery i spacje. Pole telephone: opcjonalne, format 9 cyfr.
```

**v3 (najlepszy — dodajesz kontekst techniczny):**
```
Dodaj walidację jak w v2. Użyj adnotacji jakarta.validation. Dodaj custom message_pl w messages.properties. Nie zmieniaj istniejących pól.
```

## Porównaj wyniki

- v1: ogólnikowy, może dodać przypadkowe reguły
- v2: trafny, ale może użyć złego pakietu (javax vs jakarta)
- v3: precyzyjny, kontrolujesz framework i lokalizację

**Wniosek:** Im więcej ograniczeń w parze z kontekstem, tym lepszy wynik. Iteruj.

## Bonus: SOLID refaktor z precyzyjnym promptem

Otwórz `OwnerController.java` i wpisz:

```
#file:OwnerController.java Ta klasa łamie Single Responsibility Principle — kontroler zawiera logikę biznesową.
Zaproponuj refaktor do SOLID:
1. Wydziel logikę wyszukiwania do OwnerService
2. Kontroler deleguje do serwisu
3. Pokaż TYLKO plan (tabela: plik | zmiana | uzasadnienie), BEZ kodu
```

Oceń, czy plan jest realistyczny. To umiejętność, której AI nie zastąpi.
