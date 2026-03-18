# Ex 10b: Wybór modelu AI — porównanie na żywym zadaniu

> Bonus · ~8 min · Między ex_10 a ex_11

**Po co:** Copilot pozwala wybrać model AI. Różne modele = różna jakość dla różnych zadań. Warto wiedzieć, kiedy zmienić.

## Co zrobić

### Krok 1: Sprawdź dostępne modele

1. W Copilot Chat kliknij dropdown z nazwą modelu (u dołu okna chatu)
2. Zobaczysz listę dostępnych modeli, np.:
   - GPT-4o
   - Claude Sonnet 4
   - Gemini 2.5 Pro

### Krok 2: Porównanie na tym samym zadaniu

Wykonaj TEN SAM prompt na 2-3 różnych modelach. Wpisz:

```
#file:OwnerController.java Zrefaktoryzuj metodę processFindForm: wydziel logikę wyszukiwania do prywatnej metody, zastosuj Stream API, dodaj obsługę null. Zachowaj komentarze po polsku.
```

Przełącz model i powtórz prompt. Porównaj:
- Jakość kodu
- Czytelność
- Czy zachował instrukcje (polski, Stream API)
- Szybkość odpowiedzi

### Krok 3: Tabelka porównawcza

Zapisz wyniki:

| Model | Jakość kodu | Instrukcje | Szybkość | Uwagi |
|---|---|---|---|---|
| GPT-4o | | | | |
| Claude Sonnet 4 | | | | |
| Gemini 2.5 Pro | | | | |

**Kiedy zmieniać model?**
- Kod/refaktor → Claude lub GPT-4o (precyzja)
- Szybkie pytania → model szybszy (Flash)
- Duży kontekst (wiele plików) → model z dużym oknem kontekstowym

**Tip:** W VS Code Settings możesz ustawić domyślny model: `github.copilot.chat.defaultModel`.
