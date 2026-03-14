# Ex 08b: Copilot Memory — kontekst zapamiętywany przez AI

> Bonus · ~5 min · Między ex_08 a ex_09

**Po co:** Copilot Memory pozwala AI zapamiętywać fakty o Twoim repozytorium i preferencjach. Działa między sesjami — nie musisz powtarzać kontekstu.

## Co zrobić

### Krok 1: Sprawdź Memory

1. Otwórz Copilot Chat
2. Wpisz:

```
Co wiesz o moich preferencjach i tym projekcie? Wymień zapamiętane fakty.
```

3. Jeśli pusta — to normalne, jeszcze nic nie zapisano.

### Krok 2: Naucz Copilot

Wpisz:

```
Zapamiętaj: w tym projekcie używamy Java 17, Spring Boot 3.x, JUnit 5 z Mockito. Testy nazywamy should_X_when_Y. Javadoc piszemy po polsku. Commits w formacie conventional commits.
```

Copilot powinien potwierdzić zapisanie.

### Krok 3: Weryfikacja

Zamknij chat. Otwórz nowy. Wpisz:

```
Wygeneruj test dla metody findByLastName w OwnerRepository.
```

**Spodziewany wynik:** Test z nazewnictwem `should_X_when_Y`, JUnit 5, Mockito — **bez przypominania** w prompcie.

## Memory vs Instructions

| Cecha | Memory | copilot-instructions.md |
|---|---|---|
| Zakres | Twoje konto / repo | Repozytorium |
| Trwałość | Między sesjami | W pliku (git) |
| Dostęp zespołu | Tylko Ty | Wszyscy |

**Tip:** Memory na preferencje osobiste. Instructions na standardy zespołowe. Razem dają pełny kontekst.
