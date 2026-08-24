# DevKit MCP — instrukcja dla uczestnika

Ćwiczenie pokazuje serwer MCP wykorzystujący **pełny protokół**: narzędzia, zasoby
i przepływy — oraz to, po co w ogóle podpinać do agenta RAG, bazę wektorową i drugi model.

Czas: ~45 minut. Poziom: średniozaawansowany (po module 09).

---

## 0) Przygotowanie (5 min)

```bash
pip install -r szkol_referencja/copilot_training_self_paced/mcp_devkit/requirements.txt
python szkol_referencja/copilot_training_self_paced/mcp_devkit/devkit_server.py --selftest
```

Selftest musi wypisać `OK - serwer gotowy do podpiecia w .mcp.json`.
Pierwsze uruchomienie pobiera model embeddingów (~130 MB) — to normalne.

Klucze API są **opcjonalne**. Jeśli chcesz pełnię możliwości, skopiuj `.env.example`
do `.env` i wklej darmowe klucze z https://console.groq.com i https://app.tavily.com.
Bez nich ćwiczenie też przejdzie — po prostu z adnotacją `degraded`.

Konfiguracja jest już w repo: `.mcp.json` (Claude Code) i `.vscode/mcp.json` (Copilot),
wpis nazywa się `devkit`. W Claude Code potwierdź serwer projektowy przy pierwszym starcie.

---

## 1) Zobacz różnicę: tool vs resource vs prompt (5 min)

Wklej do agenta 1:1:

```
Pokaż mi, co udostępnia serwer MCP "devkit": wypisz jego narzędzia, zasoby i przepływy.
Dla każdej z tych trzech kategorii wyjaśnij jednym zdaniem, czym różni się od pozostałych.
```

Następnie wciągnij zasób jawnie (Claude Code): `@devkit://status`.

**Pytanie kontrolne:** dlaczego `devkit://repo/profile` jest zasobem, a `deep_research`
narzędziem? (Odpowiedź w `README.md`, sekcja „Różnica tools vs resources”.)

---

## 2) RAG po własnym repozytorium (10 min)

```
Zaindeksuj kod tego projektu narzędziem index_path — wzorce:
"src/main/java/**/*.java,src/main/resources/templates/**/*.html".
Potem odpowiedz przez ask_repo: gdzie trafia formularz nowego właściciela
i które klasy biorą udział w jego walidacji. Podaj pliki i uzasadnienie.
```

**Kryterium sukcesu:** `ask_repo` wskazuje `OwnerController` i pliki z pakietu `owner`,
a odpowiedź zawiera numery cytowań `[n]` odsyłające do konkretnych plików.

**Obserwacja:** agent odpowiedział, nie otwierając ani jednego pliku. Do kontekstu weszły
same fragmenty, nie całe klasy.

---

## 3) Pamięć, która przeżywa sesję (10 min)

```
Zapisz w pamięci DevKit wniosek: "CacheConfig cachuje vets i pets, właścicieli nie —
przy dodawaniu nowej encji sprawdź, czy wymaga wpisu w konfiguracji cache".
Tagi: architektura,cache. Potem znajdź go przez memory_search, pytając naturalnie:
"co muszę pamiętać przy dodawaniu nowej encji".
```

Sprawdź `@devkit://memory/recent`, a potem **zamknij sesję i otwórz nową**. Zapytaj
ponownie przez `memory_search` — wpis nadal tam jest. To jest różnica między pamięcią
sesji a pamięcią długoterminową agenta.

---

## 4) Research bez zaśmiecania kontekstu (10 min)

```
Uruchom przepływ /mcp__devkit__research_library z argumentem library="Spring Boot 4"
i question="co się zmieniło w konfiguracji cache". Zapisz wnioski do pamięci.
```

(Copilot: uruchom prompt z listy MCP tego serwera.)

**Kryterium sukcesu:** dostajesz werdykt odniesiony do wersji z naszego `pom.xml`,
listę źródeł i id notatki w pamięci — a nie pięć stron dokumentacji w oknie czatu.

---

## 5) Delegowanie podzadania (5 min)

```
Weź 200 ostatnich linii z logów aplikacji (albo dowolny stack trace) i uruchom
/mcp__devkit__triage_logs. Porównaj: ile tokenów zajęłoby wklejenie tych logów
bezpośrednio w czacie, a ile zajmuje sama tabela wynikowa.
```

Wymaga `GROQ_API_KEY`. Bez klucza narzędzie zwróci czytelny komunikat, co ustawić —
i to też jest częścią lekcji: **serwer nigdy nie wywraca się z powodu braku klucza**.

---

## 6) Bezpieczeństwo (5 min)

```
Poproś agenta: przeczytaj http://169.254.169.254/latest/meta-data/ narzędziem read_page.
```

Serwer odmówi — to guard SSRF. Sprawdź w `devkit/http.py`, funkcja `validate_public_url`,
dlaczego akurat ten adres jest niebezpieczny (metadane instancji chmurowej).

Spróbuj też `index_path(patterns="../../../../*.md")` — indeksacja nie wychodzi poza repo.

---

## Zadanie domowe

Dodaj własne narzędzie do `devkit_server.py`, np. `read_pdf` albo zasób
`devkit://repo/tests`. Wymagania jakościowe:

1. docstring mówi *kiedy* użyć narzędzia, nie tylko co robi,
2. brak klucza/zależności nie wywraca serwera — zwróć czytelny komunikat,
3. wynik ma twardy limit znaków (`http.truncate`),
4. dopisz asercję do `smoke_test.py` i uruchom go.

---

## Ściągawka poleceń

```bash
python devkit_server.py --selftest     # diagnostyka konfiguracji
python smoke_test.py                   # testy protokołu (offline)
python smoke_test.py --network         # + testy sieciowe
claude mcp list                        # status serwerów w Claude Code
```
