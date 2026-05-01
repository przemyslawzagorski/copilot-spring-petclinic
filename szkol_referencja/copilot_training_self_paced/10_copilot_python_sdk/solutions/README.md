# Moduł 10 — rozwiązania (Copilot Python SDK)

Zestaw uruchamialnych rozwiązań do ćwiczeń **ex_25..ex_29** plus **realne** testy
integracyjne `pytest` (bez mocków — testy wołają prawdziwe SDK i prawdziwy model).

## Struktura

```
solutions/
├─ _common.py                       # helpery PATH + lokalizacja repo
├─ requirements.txt                 # zależności Pythona
├─ pytest.ini                       # konfiguracja pytest (asyncio_mode=auto, marker live)
├─ ex_25_setup/smoke_test.py        # ex_25 – smoke check + lista modeli
├─ ex_26_hello_chat/hello_chat.py   # ex_26 – pierwsza sesja
├─ ex_27_petclinic_assistant/...    # ex_27 – agent skanuje pakiet owner i pisze raport MD
├─ ex_28_streaming/streaming_chat.py# ex_28 – streaming (AssistantMessageDeltaData)
├─ ex_29_custom_tool/custom_tool.py # ex_29 – własne narzędzie (function calling)
└─ tests/test_solutions_live.py     # pytest – realne wywołania SDK (marker `live`)
```

---

## 1. Wymagania (z oficjalnej dokumentacji)

> *„Python 3.11+ and GitHub Copilot CLI installed and accessible.”*  
> — `github/copilot-sdk/python/README.md`

```powershell
python --version             # 3.11+ (testowane na 3.12.10)
pip install -r .\solutions\requirements.txt
```

### Bundled CLI (już na dysku)

VS Code dostarcza zbundlowane `copilot.bat` w
`%APPDATA%\Code\User\globalStorage\github.copilot-chat\copilotCli\`. Helper
`_common.ensure_copilot_cli_on_path()` dokleja ten katalog do `PATH` w runtime —
**nie musisz nic dodawać ręcznie**.

---

## 2. Autoryzacja — wybierz JEDNĄ z dwóch metod

SDK domyślnie używa sesji standalone CLI (`use_logged_in_user=True`),
a jeśli ustawisz `GITHUB_TOKEN` — token ma priorytet i jest przekazywany
do podprocesu CLI.

### Metoda A — `copilot login` (rekomendowana, OAuth device flow)

```powershell
# 1) Zainstaluj GitHub Copilot CLI (Node.js 20+)
npm install -g @github/copilot

# 2) Uruchom CLI w trybie interaktywnym
copilot

# 3) Wewnątrz TUI wpisz polecenie:
/login
# CLI wyświetli kod (np. ABCD-1234) i URL https://github.com/login/device
# Otwórz URL w przeglądarce, wklej kod, zatwierdź.

# 4) Wyjdź z CLI:
/exit
```

Sesja zapisana przez `copilot login` zostaje na dysku — SDK ją podłapie
automatycznie. Sprawdź:

```powershell
python .\solutions\ex_25_setup\smoke_test.py
# Oczekiwane: "Authenticated as <login> via <oauth>" + lista modeli.
```

### Metoda B — `GITHUB_TOKEN` (do CI / automatów)

Token musi mieć dostęp do GitHub Copilot (np. `gh auth token` u zalogowanego
użytkownika z aktywną subskrypcją Copilot, albo PAT z odpowiednimi scope’ami).

```powershell
$env:GITHUB_TOKEN = "<twoj_token>"
python .\solutions\ex_25_setup\smoke_test.py
```

> ⚠️ Nie commituj tokena. Nie loguj `$env:GITHUB_TOKEN`.

---

## 3. Uruchamianie pojedynczych rozwiązań

```powershell
# z katalogu modułu 10:
cd .\szkol_referencja\copilot_training_self_paced\10_copilot_python_sdk

python .\solutions\ex_25_setup\smoke_test.py
python .\solutions\ex_26_hello_chat\hello_chat.py
python .\solutions\ex_27_petclinic_assistant\petclinic_assistant.py   # tworzy petclinic_domain_report.md w cwd
python .\solutions\ex_28_streaming\streaming_chat.py
python .\solutions\ex_29_custom_tool\custom_tool.py
```

Każdy skrypt drukuje opis tego co robi (docstring na górze pliku) — zachęcam
przeczytać przed uruchomieniem, łatwiej zrozumieć co widać w outputie.

---

## 4. Testy realne (pytest)

```powershell
cd .\szkol_referencja\copilot_training_self_paced\10_copilot_python_sdk\solutions
pytest -m live -v
```

- Marker `live` = test woła prawdziwą Copilot Session (kosztuje tokeny).
- Brak autoryzacji ⇒ testy są **automatycznie pomijane** (skip) z czytelną
  wskazówką jak się zalogować — patrz `tests/conftest.py`.
- Łączny czas oczekiwany ~3–5 min (pięć testów na `gpt-5`).

Co weryfikujemy:

| Test | Co sprawdza |
|------|-------------|
| `test_ex25_list_models_nonempty` | `client.list_models()` zwraca >0 i zawiera `gpt-5` |
| `test_ex26_hello_chat_returns_answer` | Model odpowiada na „2+2” i w odpowiedzi jest `4` |
| `test_ex27_assistant_writes_report` | Agent z prawdziwym `cwd=repo_root` tworzy plik `.md` z encjami JPA |
| `test_ex28_streaming_emits_deltas` | `streaming=True` faktycznie emituje >1 `AssistantMessageDeltaData` |
| `test_ex29_custom_tool_invoked` | Model wywołał nasze `@define_tool` i zacytował jego wynik |

---

## 5. Najczęstsze błędy

| Symptom | Przyczyna | Naprawa |
|---------|-----------|---------|
| `JsonRpcError -32603: Not authenticated` | Brak sesji w CLI i nieustawiony `GITHUB_TOKEN` | Metoda A albo B z sekcji 2. |
| `Cannot find GitHub Copilot CLI` | Bundled CLI vs. wrapper, brak `npm i -g @github/copilot` | Wykonaj `npm install -g @github/copilot`. |
| Test `test_ex28_streaming_emits_deltas` fail (`deltas == 0`) | Sesja nie ma `streaming=True` albo SDK zmieniło API zdarzeń | Sprawdź `create_session(..., streaming=True)`. |
| Test `test_ex29_custom_tool_invoked` fail (`call_log == []`) | Model nie wywołał narzędzia (np. wybrano model bez tool-callingu) | Zostaw `model="auto"` lub jawnie ustaw nowoczesny model z tool-callingiem (np. `gpt-5.4`, `claude-sonnet-4.6`). |
| `asyncio.TimeoutError` | Backend wolniejszy niż timeout | Zwiększ `timeout=` w `wait_for(...)` w danym pliku. |

---

## 6. Bezpieczeństwo

- `PermissionHandler.approve_all` jest wygodne na warsztacie, ale w produkcji
  **napisz własny handler** który odrzuca `kind == "shell"` i ogranicza zapis
  poza `working_directory`. Wzorzec w doc-stringu `ex_27`.
- Nie commituj `GITHUB_TOKEN`. Trzymaj w sekrecie CI / `.env` ignorowanym przez
  Git.
- Custom tool w `ex_29` ma `skip_permission=True`, bo to czysty lookup
  in-memory (read-only). Dla narzędzi mutujących stan (DB, FS, sieć)
  **nie używaj** `skip_permission=True`.

---

## 7. Źródła (oficjalne)

- Repo SDK: <https://github.com/github/copilot-sdk>
- Python README: <https://github.com/github/copilot-sdk/blob/main/python/README.md>
- GitHub Copilot CLI (login): <https://docs.github.com/en/copilot/github-copilot-in-the-cli>
