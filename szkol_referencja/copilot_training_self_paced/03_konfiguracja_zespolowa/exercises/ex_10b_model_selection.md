# Ex 10b: Wybór modelu AI — porównanie na żywym zadaniu

> Bonus · ~8 min · Między ex_10 a ex_11

**Po co:** Copilot pozwala wybrać model AI. Różne modele = różna jakość dla różnych zadań. Warto wiedzieć, kiedy zmienić.

## Co zrobić

### Krok 1: Sprawdź dostępne modele

1. W Copilot Chat kliknij dropdown z nazwą modelu (u dołu okna chatu)
2. Zobaczysz listę dostępnych modeli — **zapisz, co faktycznie masz**.
   Oferta zmienia się co kilka miesięcy i zależy od Twojego planu, więc
   konkretne nazwy w tym pliku szybko się dezaktualizują. Zwykle są to modele
   z rodzin GPT, Claude i Gemini.

### Krok 2: Porównanie na tym samym zadaniu

Wykonaj TEN SAM prompt na 2-3 różnych modelach. Wpisz:

```
#file:OwnerController.java Zrefaktoryzuj metodę processFindForm: wydziel
ustalanie lastName oraz wybór widoku do osobnych metod prywatnych. Zachowaj
zachowanie i komentarze po polsku. Nie zmieniaj sygnatury metody.
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
| (model 1 z Twojej listy) | | | | |
| (model 2) | | | | |
| (model 3) | | | | |

**Kryterium „Instrukcje"** jest tu najważniejsze i najłatwiej mierzalne:
sprawdź, czy model zachował komentarze **po polsku** i **nie zmienił
sygnatury**. To dwa jednoznaczne warunki z promptu — albo je spełnił, albo nie.
Ocena „jakości kodu" jest subiektywna, więc nie próbuj z niej robić rankingu.

**Kiedy zmieniać model?**
- Kod/refaktor → Claude lub GPT-4o (precyzja)
- Szybkie pytania → model szybszy (Flash)
- Duży kontekst (wiele plików) → model z dużym oknem kontekstowym

**Tip:** W VS Code Settings możesz ustawić domyślny model: `github.copilot.chat.defaultModel`.

> 🧹 **Posprzątaj:** `git checkout -- src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java`
> — przepuściłeś ten plik przez kilka modeli. Ex_16 robi na nim security
> review i opisuje **oryginalny** kod.
