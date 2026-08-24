"""PreToolUse hook blokujacy modyfikacje plikow JSON."""

import json
import sys


def get_file_path(tool_input: dict) -> str:
    """Zwraca sciezke pliku z obslugiwanego formatu danych narzedzia."""
    for key in ("filePath", "file_path", "path", "file"):
        if key in tool_input:
            return str(tool_input[key])
    return ""


input_data = json.load(sys.stdin)
tool_input = input_data.get("tool_input", {})
file_path = get_file_path(tool_input)

if file_path.lower().endswith(".json"):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"ZABLOKOWANO: modyfikacja pliku JSON '{file_path}' jest niedozwolona."
            ),
        }
    }
else:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
        }
    }

print(json.dumps(output, ensure_ascii=False))