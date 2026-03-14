# Ex 02: Inline edit — refaktor metody

> Faza 1 · ~5 min · Źródło: moduł 09

**Po co:** Nauczyć się edytować kod bezpośrednio w pliku, bez przełączania do chatu.

## Co zrobić

1. Otwórz `src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java`
2. Zaznacz całą metodę `processFindForm` (~linia 85)
3. Naciśnij **Ctrl+I** (inline chat)
4. Wpisz:

```
Uprość tę metodę używając Stream API. Zachowaj logikę.
```

5. Przejrzyj propozycję i kliknij Accept/Discard.

**Spodziewany wynik:** Copilot zaproponuje wersję z `.stream().filter()` zamiast warunkowego if/else.

**Nie działa?** Zaznacz DOKŁADNIE ciało metody (od `{` do `}`). Ctrl+I działa na zaznaczeniu.

## Bonus: Identyfikacja code smells

Zaznacz cały `OwnerController.java` i w inline chat (Ctrl+I) wpisz:

```
Zidentyfikuj code smells w tym pliku. Format: linia | smell | severity. Top 5.
```

Zobacz, czy Copilot wskaże: God Class, Long Method, Feature Envy. Porównaj z własną oceną.

**Więcej teorii:** `09_module_09/README.md`
