# Ex 21b: Copilot Code Review — AI w procesie review

> Bonus · ~8 min · Między ex_21 a ex_22

**Po co:** Copilot potrafi robić code review — zarówno lokalnie (w VS Code), jak i na GitHubie w Pull Requestach.

## Co zrobić

### Krok 1: Review lokalne (VS Code)

1. Otwórz `OwnerController.java`
2. Zaznacz cały plik (Ctrl+A)
3. W Copilot Chat wpisz:

```
Zrób profesjonalny code review tego pliku. Format:

## Podsumowanie
Ogólna ocena: X/10

## Problemy
| # | Severity | Linia | Problem | Sugerowany fix |
|---|----------|-------|---------|---------------|

## Pochwały
Co jest dobrze zrobione w tym kodzie?

## Zalecenia
Top 3 zmiany do wdrożenia w następnym sprincie.
```

### Krok 2: Review stylem PR

Teraz bardziej realistyczny scenariusz — review zmian, nie całego pliku:

```
Wyobraź sobie, że recenzujesz Pull Request dodający pole "email" do Owner.
Zmiany to: nowe pole w Owner.java, getter/setter, @Email walidacja, update formularza w OwnerController.

Zrób review jak na GitHubie:
- Approved / Changes Requested / Comment?
- Inline komentarze do konkretnych linii
- Sugestie code changes (blok ```suggestion)
```

**Spodziewany wynik:** Strukturalny review z priorytetyzacją — nie lista 50 nitpicków, ale TOP problemy.

### Bonus: Copilot Code Review na GitHubie

Jeśli masz dostęp do Copilot Code Review na GitHubie:
1. Otwórz dowolny PR w repozytorium
2. Kliknij "Copilot" → "Review"
3. Copilot doda inline komentarze z sugestiami

**Kiedy AI review, a kiedy człowiek?**
- AI: styl, typowe błędy, security patterns, spójność
- Człowiek: logika biznesowa, trade-offs architektoniczne, kontekst zespołowy
