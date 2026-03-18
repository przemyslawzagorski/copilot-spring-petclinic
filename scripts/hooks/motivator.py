#!/usr/bin/env python3
"""
PostToolUse hook — losowa wiadomosc motywacyjna po udanej edycji pliku.
Czysta zabawa, ale pokazuje mechanizm systemMessage.
"""
import json
import random
import sys

input_data = json.loads(sys.stdin.read())
tool_name = input_data.get("tool_name", "")

# Reaguj tylko na edycje plikow
FILE_TOOLS = [
    "create_file", "replace_string_in_file", "editFiles",
    "edit_file", "multi_replace_string_in_file",
]
if tool_name not in FILE_TOOLS:
    print(json.dumps({"continue": True}))
    sys.exit(0)

MESSAGES = [
    "Piekny kod! Tak trzymaj!",
    "Kolejna zmiana - kolejny krok do perfekcji!",
    "Ten kod jest lepszy niz wczoraj!",
    "Celny strzal! Dokladnie to bylo potrzebne.",
    "Czysty jak lza. Uncle Bob bylby dumny!",
    "Efektywnosc: 100%. Czas na kawe?",
    "Commit-worthy! Gotowe do review.",
    "Kod tak dobry, ze az spiewa!",
    "LGTM - Looks Good To Me!",
    "Za taki kod nalezy sie pizza!",
    "git commit -m 'feat: pure awesomeness'",
    "Dzis jestes maszynka do kodu!",
    "To byl strzal w dziesiatke!",
    "Senior Engineer energy!",
]

message = random.choice(MESSAGES)

output = {
    "systemMessage": message,
}
print(json.dumps(output, ensure_ascii=False))
