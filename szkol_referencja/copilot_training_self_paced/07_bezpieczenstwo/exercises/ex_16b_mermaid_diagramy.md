# Ex 16b: Generowanie diagramów Mermaid

> Bonus · ~5 min · Między ex_16 a ex_17

**Po co:** Copilot potrafi generować diagramy architektoniczne jako kod Mermaid. Renderuje się wprost w Markdownie na GitHubie.

## Co zrobić

1. W Copilot Chat wpisz:

```
@workspace Wygeneruj diagram Mermaid (classDiagram) pokazujący relacje między encjami: Owner, Pet, Vet, Visit, Specialty. Pokaż pola, typy relacji (1:N, M:N) i kierunek asocjacji.
```

2. Skopiuj wynik do pliku `docs/domain-model.md` (utwórz folder `docs/`).

3. Teraz drugi diagram — sekwencyjny:

```
@workspace Wygeneruj diagram Mermaid (sequenceDiagram) pokazujący flow HTTP: przeglądarka → OwnerController → OwnerRepository → H2 Database dla scenariusza "wyszukaj właściciela po nazwisku".
```

4. Dopisz do tego samego pliku.

**Spodziewany wynik:** Dwa bloki Mermaid w Markdownie:
- `classDiagram` z 5 encji i relacjami
- `sequenceDiagram` z 4 uczestnikami

**Podgląd:** Otwórz Markdown Preview (Ctrl+Shift+V) — niektóre rozszerzenia VS Code renderują Mermaid. Na GitHubie renderuje się automatycznie.

**Zastosowanie w zespole:** Dokumentacja architektury "as code" — zmienia się razem z kodem, nie gnije w Confluence.
