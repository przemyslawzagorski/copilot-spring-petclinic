# Moduł 03 - Konfiguracja zespołowa: adaptacja dla Augmenta

> Auggie współdzieli `CLAUDE.md`, a elementy specyficzne dla Augmenta przechowuje
> w `.augment/`.

## Ex 08 i 08b: instrukcje projektu i pamięć

Otwórz root `CLAUDE.md`. Auggie ładuje go automatycznie. Kolejność reguł zaczyna
się od `--rules`, następnie `CLAUDE.md`, `AGENTS.md`, `.augment-guidelines`,
`.augment/rules/` i reguł użytkownika.

Sprawdź aktywne źródła przez:

```text
/rules
```

Auggie zachowuje sesje, które można wznowić przez `/sessions`. Trwałych zasad
projektu nie zapisuj wyłącznie w historii rozmowy; umieszczaj je w commitowanych
rules albo `CLAUDE.md`.

## Ex 09: reguły kontekstowe

Przejrzyj `.augment/rules/java-spring.md`. Pole `type: agent_requested` i opis
powodują dołączenie reguły, gdy zadanie dotyczy Java/Spring.

Ćwiczenie: utwórz regułę `.augment/rules/tests.md`:

```markdown
---
type: agent_requested
description: Zasady testów Java w src/test/java
---

- Używaj JUnit 5 i Mockito.
- Dla kontrolerów używaj @WebMvcTest.
```

Rozpocznij nową sesję i sprawdź `/rules`.

## Ex 09b: wykluczanie plików

Otwórz `.augmentignore`. Format jest podobny do `.gitignore`; repo wyklucza
buildy, cache i sekrety z indeksowania. Dodaj tylko niesekretny testowy wzorzec,
sprawdź efekt, a potem cofnij zmianę.

## Ex 10: custom command

Przejrzyj `.augment/commands/training/exercise.md`. Podkatalog tworzy komendę
`/training:exercise`. Utwórz własną namespaced command, unikając nazw komend
wbudowanych.

## Ex 10b: wybór modelu

Użyj `/model` i wybierz model dostępny w Twojej organizacji. Dostępna lista
zależy od planu i konfiguracji Augmenta; materiał nie zakłada konkretnego modelu.