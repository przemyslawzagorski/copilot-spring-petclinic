# Ex 18c: Refaktoring architektury z AI

> Bonus · ~12 min · Między ex_18b a ex_19

**Po co:** Copilot może proponować zmiany architektoniczne: wydzielenie warstwy serwisowej, rozdzielenie odpowiedzialności, przejście z monolitu na moduły.

## Co zrobić

### Krok 1: Analiza obecnej architektury

W Copilot Chat wpisz:

```
@workspace Przeanalizuj architekturę spring-petclinic. Myśl krok po kroku:
1. Ile jest warstw? (controller, service, repository, model)
2. Czy kontrolery bezpośrednio używają repozytoriów (łamanie warstw)?
3. Jakie wzorce projektowe są użyte?
4. Co zrefaktoryzowałbyś w pierwszej kolejności? Top 3 z uzasadnieniem.
Format: tabela priorytetów z wysiłkiem (S/M/L) i ryzykiem.
```

### Krok 2: Wydzielenie warstwy serwisowej

```
W OwnerController.java logika biznesowa jest bezpośrednio w kontrolerze. Zaproponuj refaktor:
1. Utwórz OwnerService (interfejs + implementacja)
2. Przenieś logikę z kontrolera do serwisu
3. Kontroler wstrzykuje OwnerService zamiast OwnerRepository
4. Pokaż TYLKO plan zmian (pliki, co się zmienia) — bez kodu. Format: tabela.
```

### Krok 3: Ocena realności

Po zobaczeniu planu, zapytaj:

```
Dla tego planu refaktoryzacji oceń:
1. Ile czasu zajmie (S: godziny, M: dni, L: tygodnie)?
2. Jakie testy trzeba dodać/zmienić?
3. Jakie ryzyko regresji?
4. Czy warto to robić dla tego rozmiaru projektu?
```

**Granice AI w architekturze:**
- ✅ Widzi structural issues (brakujące warstwy, za duże klasy)
- ✅ Generuje poprawny plan kroków
- ⚠️ Nie zna kontekstu biznesowego (dlaczego coś było tak zrobione)
- ❌ Nie oceni trade-offs specyficznych dla Twojego zespołu

**Wniosek:** Copilot to świetny "architecture advisor" na etapie analizy. Decyzję o wdrożeniu podejmuje człowiek.
