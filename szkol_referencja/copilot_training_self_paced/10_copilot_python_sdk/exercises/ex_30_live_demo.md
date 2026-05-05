# Ex 30: Live Demo — AI Triage Asystent w PetClinic

> Faza 9 · ~30 min · Moduł 10 · 🏆 Live Demo

**Scenariusz biznesowy:** Dodajemy do Spring PetClinic nową zakładkę
**„AI Asystent"**, w której właściciel zwierzęcia opisuje objawy i otrzymuje
rekomendację odpowiedniego weterynarza. AI czyta **żywe dane** z działającej
aplikacji Spring (`GET /vets`) za pomocą custom tools.

---

## Architektura integracji

```
Przeglądarka
    │  POST /api/ai/chat  { "message": "Mój kot..." }
    ▼
Spring PetClinic :8080   (AiAssistantController — proxy)
    │  POST http://localhost:8081/chat
    ▼
Python FastAPI :8081      (ai_server.py)
    │  Copilot SDK — sesja z custom tools
    ├─► get_available_vets   →  GET http://localhost:8080/vets  (ŻYWE DANE!)
    ├─► get_visit_load       →  symulowane obciążenie wizytami
    └─► search_pet_owners    →  GET http://localhost:8080/owners
```

---

## Wymagania

- Ćwiczenie [ex_26](ex_26_hello_chat.md) i [ex_29](ex_29_custom_tool.md) ukończone.
- Spring PetClinic uruchomiony (`./mvnw spring-boot:run`).
- Python 3.11+, aktywne venv z SDK.

---

## Krok 1 — Zainstaluj dodatkowe zależności

```powershell
pip install "fastapi>=0.111" "uvicorn[standard]>=0.29" httpx
```

---

## Krok 2 — Uruchom serwis AI

```powershell
cd szkol_referencja/copilot_training_self_paced/10_copilot_python_sdk/solutions/ex_30_live_demo
uvicorn ai_server:app --host 127.0.0.1 --port 8081 --reload
```

Sprawdź:
```powershell
curl http://localhost:8081/health
# → {"status":"ok","service":"petclinic-ai-assistant"}
```

---

## Krok 3 — Uruchom Spring PetClinic

```powershell
# w katalogu głównym projektu
./mvnw spring-boot:run
```

Otwórz: **http://localhost:8080/ai-assistant**

---

## Krok 4 — Live Demo — scenariusze WOW

Wpisz w polu czatu:

### Scenariusz A — Triage po objawach
```
Mój kot ma ból zęba i od dwóch dni nie je. Który weterynarz się tym zajmuje?
```
*AI wywołuje `get_available_vets` → pobiera żywą listę → rekomenduje specjalistę od dentystyki.*

### Scenariusz B — Porównanie dostępności
```
Potrzebuję weterynarza od chirurgii. Który jest mniej zajęty dziś?
```
*AI wywołuje `get_available_vets` + `get_visit_load` → porównuje obciążenie.*

### Scenariusz C — Historia właściciela
```
Jestem Franklin, mam kota Luckiego. Kiedy była jego ostatnia wizyta?
```
*AI wywołuje `search_pet_owners("Franklin")` → pobiera dane z bazy.*

---

## Co dzieje się pod maską

1. Spring `AiAssistantController.chat()` przyjmuje JSON z przeglądarki.
2. Walidacja Pydantic w Springu (`@Valid @Size(max=500)`) — ochrona przed zbyt
   długimi promptami.
3. `RestClient` (Spring 6.1) wysyła żądanie do FastAPI `:8081`.
4. FastAPI uruchamia nową sesję `CopilotClient` dla każdego pytania.
5. Model AI decyduje, które z 3 narzędzi wywołać i w jakiej kolejności.
6. Narzędzie `get_available_vets` robi `GET /vets` na **tej samej** aplikacji
   Spring — model widzi **aktualne** dane.
7. Odpowiedź wraca przez FastAPI → Spring → przeglądarkę (JSON).

---

## Wartość biznesowa

| Bez AI | Z AI Asystentem |
|--------|----------------|
| Właściciel przegląda tabelę weterynarzy | Opisuje objawy naturalnym językiem |
| Sam musi wiedzieć jakie są specjalizacje | AI dopasowuje specjalistę |
| Musi sprawdzać obciążenie | AI sugeruje mniej zajętego |
| Brak personalizacji | Może pytać o historię swoich zwierząt |

---

## Pliki projektu

| Plik | Rola |
|------|------|
| `solutions/ex_30_live_demo/ai_server.py` | Python FastAPI + Copilot SDK |
| `src/main/java/.../ai/AiAssistantController.java` | Spring controller + proxy |
| `src/main/resources/templates/ai/assistant.html` | Thymeleaf chat UI |
| `src/main/resources/templates/fragments/layout.html` | Zaktualizowana nawigacja |

---

## Eksperyment — dodaj własne narzędzie

Jako rozszerzenie dodaj narzędzie `book_visit_recommendation`, które:
- Przyjmuje `vet_id: int` i `preferred_time: str`
- Zwraca symulowane wolne sloty (np. listę godzin)
- Rejestruje narzędzie w sesji SDK

To pokaże pełny cykl: **diagnoza → polecenie specjalisty → propozycja terminu**.
