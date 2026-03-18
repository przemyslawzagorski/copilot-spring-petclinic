# MCP FastAPI - szybka instrukcja dla uczestnika

## Ważne: gdzie jest właściwa konfiguracja MCP

- Docelowy plik konfiguracyjny MCP w repo: `.vscode/mcp.json`
- Plik `mcp-config.json` w tym folderze ćwiczenia jest tylko przykładem materiałowym.

## 1) Prompt do Copilota (wklej 1:1)

Skonfiguruj mi lokalny serwer MCP w tym projekcie.

Kroki, które wykonaj:
1. Ustaw i użyj lokalnego środowiska Python (`.venv`) w tym workspace.
2. Doinstaluj wymagane pakiety: `mcp` i `httpx`.
3. Utwórz lub zaktualizuj plik `.vscode/mcp.json` z konfiguracją:

```json
{
  "servers": {
    "publiczne-api": {
      "command": "python",
      "args": [
        "${workspaceFolder}/szkol_referencja/copilot_training_self_paced/mcp_ex_api/api_sever.py"
      ]
    }
  }
}
```

4. Uruchom i zweryfikuj serwer z pliku:
   `szkol_referencja/copilot_training_self_paced/mcp_ex_api/api_sever.py`
5. Potwierdź, że startuje bez błędów importów.

## 2) Plik przykładowy do ćwiczeń

- `szkol_referencja/copilot_training_self_paced/mcp_ex_api/mcp-config.json`
- Ten plik zostawiamy jako przykład edukacyjny, ale aktywna konfiguracja projektu jest w `.vscode/mcp.json`.

## 3) Uwagi praktyczne

- Najprościej uruchamiać z aktywnym `.venv`, aby `python` wskazywał właściwy interpreter.
- Jeżeli `python` nie wskazuje na `.venv`, ustaw w `command` pełną ścieżkę do interpretera.
