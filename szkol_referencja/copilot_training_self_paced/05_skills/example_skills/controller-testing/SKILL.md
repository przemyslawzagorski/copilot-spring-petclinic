---
name: controller-testing
description: >
  Generuje testy integracyjne dla kontrolerów Spring MVC
  z użyciem MockMvc, @WebMvcTest i szablonów z folderu zasobów.
  Zawiera gotowy szablon testu i przykłady asercji.
argument-hint: "Podaj nazwę kontrolera do przetestowania, np. OwnerController"
---

# Procedura tworzenia testu kontrolera

## Krok 1 — Analiza kontrolera
Przeczytaj wskazany kontroler i zidentyfikuj:
- Endpointy (metody HTTP + ścieżki)
- Zależności do zamockowania (@MockBean)
- Modele danych przekazywane do widoków

## Krok 2 — Wygeneruj test
Użyj szablonu z `test-template.java` w tym folderze.
Dla każdego endpointu utwórz minimum:
- Test happy path (status 200/302)
- Test walidacji (niepoprawne dane → errors)

## Krok 3 — Asercje
Wzoruj się na przykładach w `examples/`:
- `get-endpoint.java` — GET + model attributes
- `post-with-validation.java` — POST + BindingResult

## Krok 4 — Uruchom testy
```bash
./mvnw test -pl spring-petclinic -Dtest=<NazwaTestu>
```
