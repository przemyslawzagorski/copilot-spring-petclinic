# Moduł 10 — Python SDK: adaptacja dla Claude Code

> W tym module zamiast Copilot Python SDK używasz **Anthropic Python SDK**.
> To oficjalny SDK do Claude — bogaty, dojrzały, z pełnym wsparciem dla streaming, tool use i multi-turn.

---

## Instalacja

```bash
pip install anthropic
```

Weryfikacja:
```python
import anthropic
print(anthropic.__version__)
```

---

## Kluczowe różnice: Copilot SDK vs Anthropic SDK

| Copilot Python SDK | Anthropic Python SDK |
|---|---|
| `from copilot import CopilotClient` | `import anthropic` |
| `client = CopilotClient()` | `client = anthropic.Anthropic()` |
| Auth przez GitHub token | Auth przez `ANTHROPIC_API_KEY` |
| Model: `gpt-4o`, `claude-3-5-sonnet` | Model: `claude-sonnet-4-6`, `claude-opus-4-8` |
| `client.chat.completions.create()` | `client.messages.create()` |
| `response.choices[0].message.content` | `response.content[0].text` |
| Streaming: `stream=True` | Streaming: `client.messages.stream()` |

---

## Ex 25 (CC): Pierwszy request do Claude

**Odpowiednik ex_25_setup_sdk.md**

Ustaw klucz API:
```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-..."
```

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Wyjaśnij wzorzec Repository używany w Spring PetClinic w 3 punktach."
        }
    ]
)

print(message.content[0].text)
```

---

## Ex 26 (CC): System prompt i kontekst projektu

**Odpowiednik ex_26_hello_chat.md**

```python
import anthropic

client = anthropic.Anthropic()

# Wczytaj CLAUDE.md jako kontekst
with open("CLAUDE.md", "r", encoding="utf-8") as f:
    project_context = f.read()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    system=f"""Jesteś asystentem Spring PetClinic.
Oto kontekst projektu:

{project_context}

Odpowiadaj po polsku. Odwołuj się do konkretnych klas i metod.""",
    messages=[
        {
            "role": "user",
            "content": "Jak dodać nową encję do projektu?"
        }
    ]
)

print(message.content[0].text)
```

---

## Ex 27 (CC): PetClinic assistant

**Odpowiednik ex_27_petclinic_assistant.md**

Wczytaj kod pakietu `owner` lokalnie i przekaż go jako kontekst do Anthropic SDK.
Wynik zapisz do `petclinic_domain_report.md`; raport powinien zawierać pięć encji
JPA i endpointy kontrolerów.

```python
from pathlib import Path
import anthropic

root = Path(__file__).resolve().parents[4]
owner_sources = "\n\n".join(
    path.read_text(encoding="utf-8")
    for path in (root / "src/main/java/org/springframework/samples/petclinic/owner").glob("*.java")
)

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": f"Przeanalizuj encje JPA i endpointy. Zwróć raport Markdown.\n\n{owner_sources}",
    }],
)
Path("petclinic_domain_report.md").write_text(message.content[0].text, encoding="utf-8")
```

---

## Ex 28 (CC): Streaming odpowiedzi

**Odpowiednik ex_28_streaming.md**

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Napisz test JUnit 5 dla metody findOwnerById w OwnerController."
        }
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # nowa linia po zakończeniu
```

---

## Ex 29 (CC): Tool use (function calling)

**Odpowiednik ex_29_custom_tool.md**

Tool use to odpowiednik Copilot function calling — identyczna koncepcja, inny format:

```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_owner_info",
        "description": "Pobiera informacje o właścicielu zwierzęcia z bazy danych",
        "input_schema": {
            "type": "object",
            "properties": {
                "owner_id": {
                    "type": "integer",
                    "description": "ID właściciela"
                }
            },
            "required": ["owner_id"]
        }
    }
]

def get_owner_info(owner_id: int) -> dict:
    # W realnym kodzie: zapytanie do Spring API lub bazy danych
    return {"id": owner_id, "name": "Jan Kowalski", "pets": ["Burek", "Mruczek"]}

messages = [{"role": "user", "content": "Jakie zwierzęta ma właściciel o ID 1?"}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# Obsłuż tool call
if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    tool_result = get_owner_info(**tool_use.input)

    messages.extend([
        {"role": "assistant", "content": response.content},
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(tool_result, ensure_ascii=False)
                }
            ]
        }
    ])

    final = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    print(final.content[0].text)
```

---

## Dodatkowy przykład: Multi-turn conversation

Ten przykład uzupełnia ćwiczenia i pokazuje utrzymywanie historii rozmowy.

```python
import anthropic

client = anthropic.Anthropic()
conversation_history = []

def chat(user_message: str) -> str:
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system="Jesteś pomocnym asystentem Spring PetClinic. Odpowiadaj po polsku.",
        messages=conversation_history
    )

    assistant_message = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message

# Przykład wieloturowej rozmowy
print(chat("Jaka jest architektura Spring PetClinic?"))
print(chat("A jakie wzorce projektowe są w niej używane?"))
print(chat("Pokaż przykład zastosowania wzorca Repository"))
```

---

## Ex 30 (CC): Asystent AI — integracja z projektem

**Odpowiednik ex_30_live_demo.md**

Ten projekt ma już działający AI Triage Assistant w:
- `src/main/java/org/springframework/samples/petclinic/ai/AiAssistantController.java`
- UI: `src/main/resources/templates/ai/assistant.html`

Aby uruchomić istniejące wspólne demo Copilot SDK:
```powershell
pip install -r .\szkol_referencja\copilot_training_self_paced\10_copilot_python_sdk\solutions\requirements.txt
python -m copilot download-runtime
# Wymagana sesja `copilot login` albo COPILOT_GITHUB_TOKEN.
Push-Location .\szkol_referencja\copilot_training_self_paced\10_copilot_python_sdk\solutions\ex_30_live_demo
uvicorn ai_server:app --host 127.0.0.1 --port 8081
```

W drugim terminalu PowerShell:
```powershell
.\mvnw.cmd spring-boot:run
# Otwórz http://localhost:8080/ai-assistant
```

Linux/macOS:
```bash
pip install -r szkol_referencja/copilot_training_self_paced/10_copilot_python_sdk/solutions/requirements.txt
python -m copilot download-runtime
# Wymagana sesja `copilot login` albo COPILOT_GITHUB_TOKEN.
cd szkol_referencja/copilot_training_self_paced/10_copilot_python_sdk/solutions/ex_30_live_demo
uvicorn ai_server:app --host 127.0.0.1 --port 8081
# W drugim terminalu, z root repo: ./mvnw spring-boot:run
```

> Uwaga: ten żywy przykład celowo używa **Copilot SDK**. Claude Code może go
> uruchamiać i modyfikować, ale klucz `ANTHROPIC_API_KEY` nie jest przez ten serwis
> używany. Wariant Anthropic wymaga osobnej implementacji klienta.

**Dodaj własną funkcjonalność** — przykład endpoint analizujący dane właściciela:

```python
# Skrypt pomocniczy: scripts/ai/analyze_owner.py
import anthropic
import requests

def analyze_owner(owner_id: int):
    client = anthropic.Anthropic()

    # Pobierz dane z Spring API
    owner_data = requests.get(f"http://localhost:8080/api/owners/{owner_id}").json()

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Haiku dla szybkości
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": f"Przeanalizuj historię wizyt właściciela: {owner_data}. Podaj 3 rekomendacje."
        }]
    )

    return response.content[0].text

print(analyze_owner(1))
```

---

## Modele Claude — przewodnik wyboru

| Model | ID | Najlepszy do | Szybkość | Koszt |
|---|---|---|---|---|
| Claude Opus 4 | `claude-opus-4-8` | Złożona analiza, architektura | Wolny | Wysoki |
| Claude Sonnet 4 | `claude-sonnet-4-6` | Ogólne zadania (domyślny) | Średni | Średni |
| Claude Haiku 4 | `claude-haiku-4-5-20251001` | Szybkie, proste zadania | Szybki | Niski |

**Reguła:** Używaj Haiku dla prostych zadań w pętlach (wiele requestów), Sonnet dla typowej pracy, Opus dla jednorazowej złożonej analizy.
