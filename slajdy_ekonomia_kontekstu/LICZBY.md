# Wszystkie liczby w jednym miejscu

Zestawienie do szybkiego sprawdzenia. Kolumna „Skąd" rozróżnia pomiar własny
od dokumentacji dostawcy — to rozróżnienie ma znaczenie przy powoływaniu się
na te dane.

## Korpusy pomiarowe

| Korpus | Co z niego pochodzi |
|---|---|
| 226 sesji | katalog narzędzi, rozkład tur, narzędzia nigdy nieużyte |
| 159 sesji, 24 680 przejść | zachowanie cache w funkcji odstępu |
| 16 konfiguracji jednego zadania | punkt optymalny katalog/tury/model |
| 23 165 wywołań | zajętość okna kontekstu |

## Cache — klif pięciu minut

*Pomiar własny, 159 sesji*

| Odstęp od poprzedniej tury | Cache read | Śr. cache creation/turę |
|---|---:|---:|
| < 1 min | 97,4% | 3 409 |
| 1–5 min | 95,9% | 5 375 |
| **5–15 min** | **15,7%** | **105 853** |
| 15–60 min | 3,1% | 102 982 |
| > 60 min | 2,8% | 96 112 |

Skok cache creation: **31×**

## Cache — mechanizm

*Dokumentacja Anthropica*

| Fakt | Wartość |
|---|---|
| Domyślny TTL | **5 minut** |
| Opcjonalny TTL | 1 godzina |
| Koszt odczytu | 0,1× stawki input |
| Koszt zapisu (5 min) | 1,25× |
| Koszt zapisu (1 h) | 2× |
| Próg opłacalności (5 min) | 2 zapytania |
| Próg opłacalności (1 h) | 3 zapytania |
| Kolejność składania prefiksu | narzędzia → system → wiadomości |
| Maks. punktów cache w zapytaniu | 4 |
| Minimalny cache'owalny prefiks | zależny od modelu (512–4096), **nie rośnie liniowo z generacjami** |

## Kula śnieżna — zajętość tura po turze

*Pomiar własny*

| Model | Tury | Zajętość narastająco |
|---|---:|---|
| `haiku4.5` | 4 | 20 284 → 29 343 → 38 260 → 45 335 |
| `sonnet4.6` | 7 | 20 284 → 22 592 → 26 031 → 29 086 → 31 251 → 32 231 → 32 673 |

Stały prefiks (oba modele): **20 284**

## Katalog narzędzi — cennik

*Pomiar własny*

| Podmiot | Koszt/wywołanie | Realne użycie |
|---|---:|---|
| Subagenci (7 narzędzi) | 3 805 | **0,83%** |
| Zarządzanie zadaniami (4) | 1 869 | 5,3% |
| `str-replace-editor` | 1 631 | niezbędny |
| `view` | 1 493 | niezbędny |
| `launch-process` | 1 092 | |
| `codebase-retrieval` | 332 | |
| `save-file` | 322 | |
| `web-fetch` | 173 | |

| Konfiguracja | Koszt stały | Zmiana |
|---|---:|---:|
| Pełny katalog | 17 219 | — |
| Bez subagentów i zadaniowych | 11 545 | −33% |
| Minimum read-only | 9 045 | −47,5% |

**Jeden nieużywany serwer MCP: ~46 000 tokenów na wywołanie.**

## Punkt optymalny — 16 konfiguracji

*Pomiar własny, jedno zadanie*

| Wariant | Tury | Tokeny | vs baza | Ocena |
|---|---:|---:|---:|:---:|
| Wszystkie 32 usunięte, `--max-turns 1` | 1 | 4 571 | −94,5% | **0/3** |
| Wszystkie usunięte, uncapped | 1 | 4 574 | −94,5% | **0/3** |
| 2 narzędzia, `--max-turns 2` | 2 | 18 854 | −77,4% | **0/3** |
| 2 narzędzia, `--max-turns 2` (powt.) | 2 | 18 882 | −77,3% | **0/3** |
| `gpt5.6-luna`, 2 narzędzia, `--max-turns 4` | 4 | 23 033 | −72,4% | 3/3 |
| **2 narzędzia, uncapped** | 3 | **29 830** | **−64,2%** | **3/3** |
| 2 narzędzia, `--max-turns 4` | 4 | 39 988 | −52,0% | 3/3 |
| Pełny katalog, `--max-turns 2` | 2 | 40 245 | −51,7% | 3/3 |
| Pełny katalog, uncapped *(baza)* | 4 | 83 313 | — | 3/3 |
| `haiku4.5`, pełny katalog | 6 | 95 136 | **+14,2%** | 3/3 |
| `gemini-3.1-pro-preview`, pełny katalog | 11 | 157 594 | **+89,2%** | 3/3 |

## Reguły — koszt spoczynkowy

*Pomiar własny, reguła 81 KB, `auggie 0.32.0`, 2026-08-11*

| Konfiguracja | Instrukcje systemowe | Koszt reguły |
|---|---:|---:|
| bez reguły | 6 689 | — |
| `always_apply` | 33 729 | **27 040** |
| `agent_requested` | 6 745 | **56** |

**Stosunek: 483×**

Koszt spoczynkowy skilla: **~66 tokenów** (sam opis). Komendy: **~0**.

## Rozkład tur

*Pomiar własny, 226 sesji*

| p50 | p95 |
|---:|---:|
| 9 | 100 |

**22% zadań powyżej 30 tur zużywa 72,8% wszystkich tokenów.**

Próg bezpiecznika ~60 tur zostawia **88,7%** realnych zadań nietkniętych.

## Zajętość okna kontekstu

*Pomiar własny, 226 sesji / 23 165 wywołań*

| Fakt | Wartość |
|---|---|
| Mediana historii, pierwsze 25 wywołań | 23 262 |
| Mediana historii, od 50. wywołania | ~64 000 |
| Sesje automatycznie skompaktowane | **0** |
| Wywołania przekraczające okno 200 000 | **3 z 23 165** |

Historia **osiąga plateau** — działa okno przesuwne.

## Reguła oszczędnościowa

*Pomiar własny, jedno zadanie*

| Pomiar | Wynik | Tury | Ocena |
|---|---:|---|:---:|
| Pierwotny | −31,5% | 4 → 3 | 3/3 |
| Powtórzenie | −24,5% | 4 → 3 | 3/3 |

Kierunek powtarzalny, wielkość efektu zależna od zadania.

## Język promptu

*Wyliczenie na podstawie pomiaru własnego*

| Twierdzenie | Realny wpływ |
|---|---|
| „Polski kosztuje +42%" | Mechanizm prawdziwy (~1,42× tokenów) |
| Twoja wiadomość to 0,5% rachunku | → wpływ na całość: **~0,21%** |
| Gdyby cały system prompt był po polsku | → **~3,2%** |

Dla porównania: jeden zbędny serwer MCP to ~46 000 tokenów na wywołanie.
