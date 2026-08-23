"""PreToolUse hook blokujący destrukcyjne polecenia terminalowe."""

import json
import re
import sys

# Windows: konsola bywa w cp1250, a JSON musi byc UTF-8.
# Bez tego polskie znaki w komunikatach hooka wychodza jako krzaki.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


input_data = json.load(sys.stdin)
tool_input = input_data.get("tool_input", {})
command = " ".join(
    str(tool_input.get(key, "")) for key in ("command", "cmd", "script", "input")
)
patterns = (
    r"\brm\s+-rf\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bDROP\s+(TABLE|DATABASE)\b",
    r"\bFORMAT\b",
    r"\bRemove-Item\b.*\s-Recurse\b.*\s-Force\b",
)
denied = any(re.search(pattern, command, re.IGNORECASE) for pattern in patterns)
if denied:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "ZABLOKOWANO: polecenie pasuje do destrukcyjnego wzorca."
                    ),
                }
            },
            ensure_ascii=False,
        )
    )