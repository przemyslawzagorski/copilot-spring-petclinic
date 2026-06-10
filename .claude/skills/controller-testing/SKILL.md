---
name: controller-testing
description: Generuje testy integracyjne MockMvc dla kontrolerów Spring MVC. Używaj gdy chcesz napisać testy dla *Controller.java lub gdy jesteś w ćwiczeniu TDD z modułu 06.
argument-hint: "Podaj nazwę kontrolera (np. OwnerController) lub ścieżkę do pliku"
allowed-tools: Read Grep Glob Write
---

# Generowanie testów integracyjnych MockMvc

## Krok 1 — Analiza kontrolera

Znajdź kontroler:

!`find src/main/java -name "*Controller.java" | head -10`

Wczytaj wskazany kontroler i zidentyfikuj:
- Wszystkie endpointy (`@GetMapping`, `@PostMapping`, etc.)
- Parametry i walidację (`@Valid`, `@ModelAttribute`, `@PathVariable`)
- Widoki Thymeleaf (wartości zwracane jako String)

## Krok 2 — Szablon testu

Wygeneruj klasę testową według wzorca:

```java
@WebMvcTest(NazwaController.class)
class NazwaControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private NazwaSerwis serwis;

    @Test
    void shouldDisplayListPage() throws Exception {
        // given
        given(serwis.findAll()).willReturn(List.of(...));

        // when & then
        mockMvc.perform(get("/endpoint"))
            .andExpect(status().isOk())
            .andExpect(view().name("nazwa-widoku"))
            .andExpect(model().attributeExists("attrName"));
    }
}
```

## Zasady

- JUnit 5 (`@Test`), Mockito (`@MockBean`), MockMvc (`@WebMvcTest`)
- Nigdy JUnit 4
- Jeden test = jeden scenariusz
- Nazwy testów: `shouldDoSomethingWhenCondition`
- Testy w: `src/test/java/org/springframework/samples/petclinic/`

## Przykładowe scenariusze do przetestowania

1. GET endpoint — status 200, poprawny widok, dane w modelu
2. GET z parametrem — status 200 lub 404 gdy nie znaleziono
3. POST valid form — redirect po sukcesie
4. POST invalid form — powrót do formularza z błędami
