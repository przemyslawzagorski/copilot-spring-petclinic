# Ex 18b: Migracja między językami — Java → Python

> Bonus · ~15 min · Między ex_18 a ex_19

**Po co:** Copilot potrafi tłumaczyć kod między językami. To nie jest "kopiuj-wklej" — to konwersja idiomów, frameworków i konwencji.

## Co zrobić

### Krok 1: Prosta konwersja encji

1. Otwórz `Owner.java`
2. W Copilot Chat wpisz:

```
#file:Owner.java Przekonwertuj tę encję JPA na Python (SQLAlchemy + Pydantic). Wygeneruj:
1. Model SQLAlchemy (owner_model.py) z relacją do Pet
2. Schema Pydantic (owner_schema.py) z walidacją
3. Zachowaj walidacje (NotBlank → validator, Size → constr)
Użyj Python 3.11+, type hints.
```

3. Przejrzyj wygenerowany kod — zwróć uwagę na jak Copilot tłumaczy:
   - `@Entity` → `class Owner(Base)`
   - `@NotBlank` → Pydantic `validator`
   - `@OneToMany` → `relationship()`

### Krok 2: Konwersja kontrolera → router FastAPI

```
#file:OwnerController.java Przekonwertuj ten Spring MVC Controller na FastAPI router (Python). Mapuj:
- @GetMapping → @router.get
- @PostMapping → @router.post
- @ModelAttribute → Pydantic schema jako parametr
- BindingResult → HTTPException z 422
Generuj plik owner_router.py.
```

### Krok 3: Oceń wynik krytycznie

Porównaj Java i Python. Zapisz:

| Aspekt | Czy Copilot dobrze przetłumaczył? |
|---|---|
| Typy danych | |
| Walidacja | |
| ORM / relacje | |
| Obsługa błędów | |
| Idiomy języka | |

**Granice AI w migracjach:**
- ✅ Dobrze: proste encje, CRUD, mapowanie 1:1
- ⚠️ Średnio: złożona logika biznesowa, transakcje
- ❌ Słabo: framework-specific magic (Spring AOP, Interceptory), wewnętrzne konwencje zespołu

**Wniosek:** Copilot to świetny "first draft" migracji. Ale kod wynikowy ZAWSZE wymaga review eksperta w języku docelowym.
