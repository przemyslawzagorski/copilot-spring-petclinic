# DevKit MCP — adaptacja dla Claude Code

> Kod serwera jest transport-agnostyczny (FastMCP) — ten sam plik obsługuje Claude Code
> i VS Code / Copilot. Różni się tylko miejsce konfiguracji.

---

## Konfiguracja

| Copilot / VS Code | Claude Code |
|---|---|
| `.vscode/mcp.json`, klucz `"servers"` | `.mcp.json` w root repo, klucz `"mcpServers"` |
| `${workspaceFolder}/...` | ścieżki względne do root repo |
| zarządzanie przez GUI | `claude mcp add / list / remove` |
| restart okna po zmianie | serwer wstaje przy starcie sesji |

Oba pliki mają już wpis `devkit` — nie musisz nic dodawać:

```json
"devkit": {
  "type": "stdio",
  "command": ".venv/Scripts/python.exe",
  "args": ["szkol_referencja/copilot_training_self_paced/mcp_devkit/devkit_server.py"]
}
```

Przy pierwszym starcie Claude Code poprosi o zatwierdzenie serwera projektowego
(`⏸ Pending approval` w `claude mcp list`). To celowe zabezpieczenie — `.mcp.json`
przychodzi z repozytorium, więc kod serwera zatwierdzasz świadomie.

---

## Co Claude Code robi z tym serwerem inaczej

**Narzędzia** — wywołuje sam, na podstawie opisów. Dlatego docstringi w `devkit_server.py`
mówią nie tylko *co* narzędzie robi, ale i *kiedy go użyć* (`delegate`: „dobre zastosowania /
złe zastosowania”). Opis narzędzia to kontrakt z modelem, nie dokumentacja dla człowieka.

**Zasoby** — wciągasz je jawnie przez `@`, np. `@devkit://repo/profile`. Model nie ładuje
zasobów samoczynnie, więc zasób nigdy nie zje kontekstu bez Twojej zgody.

**Prompty** — widoczne jako slash-commandy: `/mcp__devkit__research_library`,
`/mcp__devkit__triage_logs`, `/mcp__devkit__capture_decision`, `/mcp__devkit__rag_review`,
`/mcp__devkit__context_briefing`.

---

## Ścieżka pierwszego uruchomienia

```bash
pip install -r szkol_referencja/copilot_training_self_paced/mcp_devkit/requirements.txt
python szkol_referencja/copilot_training_self_paced/mcp_devkit/devkit_server.py --selftest
claude mcp list        # devkit — ✔ Connected
```

W sesji Claude Code:

```
1) Zaindeksuj kod:      Zaindeksuj pakiet owner narzędziem index_path
2) Zapytaj o kod:       Gdzie trafia formularz nowego właściciela? Użyj ask_repo
3) Zapamiętaj wniosek:  Zapisz to w pamięci przez memory_save, tagi: architektura
4) Sprawdź konfigurację: @devkit://status
5) Uruchom przepływ:    /mcp__devkit__context_briefing
```

---

## Współpraca z resztą narzędzi w tym repo

| Element | Jak łączy się z DevKit |
|---|---|
| agent `reviewer` | `/mcp__devkit__rag_review` daje mu kontekst repo i wcześniejsze decyzje |
| agent `tdd-expert` | `ask_repo` wskazuje istniejące wzorce testów zamiast zgadywania |
| agent `security-expert` | `deep_research` sprawdza świeże CVE dla zależności z `pom.xml` |
| skill `/project-versions` | czyta `pom.xml`; `devkit://repo/profile` daje to samo jako zasób MCP |
| moduł 09 (MCP) | `mcp_ex_api` = poziom podstawowy, `mcp_devkit` = poziom produkcyjny |

---

## Typowe pułapki

1. **`print()` na stdout zabija serwer stdio.** Diagnostyka wyłącznie na stderr
   (`logging.basicConfig(stream=sys.stderr)`).
2. **Dwa procesy na jednej lokalnej bazie Qdrant.** Jeśli serwer działa w sesji Claude Code,
   `smoke_test.py` nie wystartuje — i odwrotnie. Zamknij jeden albo użyj Qdrant Cloud.
3. **Klucze API w `.mcp.json`.** Ten plik jest w repo. Klucze trzymaj w `mcp_devkit/.env`
   (jest w `.gitignore`), serwer wczytuje je sam przez `load_dotenv`.
4. **Zmiana `EMBEDDING_MODEL` bez przeindeksowania.** Powstanie nowa, pusta kolekcja —
   `ask_repo` zwróci „kolekcja jest pusta”. Uruchom `index_path` ponownie.
