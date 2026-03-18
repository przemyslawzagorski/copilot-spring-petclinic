# Ex 06b: Few-shot, Chain-of-Thought, Role — techniki promptowania

> Bonus · ~10 min · Między ex_06 a ex_07

**Po co:** Trzy zaawansowane techniki, które drastycznie poprawiają jakość odpowiedzi Copilota.

## Technika 1: Few-shot (daj przykład)

W Copilot Chat wpisz:

```
Wygeneruj walidację dla klasy Pet. Oto przykład formatu jaki chcę:

Przykład dla Owner:
- firstName: @NotBlank, @Size(min=2, max=30), message="Imię jest wymagane"
- telephone: @Pattern(regexp="\\d{9}"), message="Format: 9 cyfr"

Teraz analogicznie dla Pet:
- name: niepuste, 1-50 znaków
- birthDate: nie z przyszłości
- type: wymagane
```

**Efekt:** Copilot naśladuje dokładnie Twój format — bo ma "przykład" (few-shot).

## Technika 2: Chain-of-Thought (myśl krok po kroku)

```
Przeanalizuj metodę processFindForm w OwnerController.java. Myśl krok po kroku:
1. Jaki jest flow danych od wejścia HTTP do odpowiedzi?
2. Jakie są możliwe ścieżki (brak wyników, 1 wynik, wiele)?
3. Czy jest potencjalny problem z wydajnością lub bezpieczeństwem?
4. Zaproponuj refaktor na podstawie analizy.
```

**Efekt:** Copilot nie zgaduje — analizuje systematycznie, wynik jest głębszy i trafniejszy.

## Technika 3: Role (nadaj rolę)

```
Jesteś senior Java developerem z 10-letnim doświadczeniem w Spring Boot. Twoje priorytety to: wydajność, czytelność, testowalność.

Zrób review metody processUpdateOwnerForm w OwnerController.java. Wskaż top 3 problemy i zaproponuj fix.
```

**Efekt:** Copilot odpowiada z perspektywy eksperta — priorytetyzuje poważne problemy, nie skupia się na kosmetyce.

## Porównaj

| Technika | Kiedy | Przykład użycia |
|---|---|---|
| Few-shot | Chcesz konkretny format wyjścia | Walidacja, testy, dokumentacja |
| Chain-of-Thought | Problem wymaga analizy | Debugging, architektura, review |
| Role | Chcesz ekspertyzę z perspektywy | Security, performance, design |
