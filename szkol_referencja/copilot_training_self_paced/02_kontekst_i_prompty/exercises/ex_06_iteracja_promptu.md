# Ex 06: Iteracja promptu v1 → v2 → v3

> Faza 2 · ~10 min · Moduł 02

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
Dodaj walidację jak w v2. Użyj adnotacji z pakietu jakarta.validation.
Komunikaty błędów wynieś do src/main/resources/messages/messages.properties
i odwołaj się do nich przez {klucz}. Nie zmieniaj istniejących pól.
```

> **Uwaga na ścieżkę:** pliki komunikatów leżą w
> `src/main/resources/messages/`, nie bezpośrednio w `resources/`. Repo ma
> tłumaczenia `de`, `en`, `es`, `fa`, `ko`, `pt`, `ru`, `tr` — **polskiego nie
> ma**.

> ⚠️ **Nie dodawaj `messages_pl.properties` „na próbę".** Projekt ma test
> `I18nPropertiesSyncTest`, który porównuje klucze we wszystkich lokalizacjach.
> Niekompletny plik **wywala build** komunikatem `Missing keys in
> messages_pl.properties`. Sprawdzone: dwa klucze zamiast **83** = czerwony
> build.
>
> Jeśli chcesz dodać polski, to osobne zadanie na 83 klucze — i całkiem dobre
> ćwiczenie na Copilota. Poproś o przetłumaczenie **całego**
> `messages.properties` naraz, a potem uruchom
> `./mvnw test -Dtest=I18nPropertiesSyncTest`, żeby zweryfikować komplet.
> To zresztą świetny przykład tego, jak testy repo pilnują roboty agenta.

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
