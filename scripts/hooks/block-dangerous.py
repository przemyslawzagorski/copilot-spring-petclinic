"""PreToolUse hook blokujący destrukcyjne polecenia terminalowe."""

import json
import re
import sys


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
decision = "deny" if denied else "allow"
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
    }
}
if denied:
    output["hookSpecificOutput"]["permissionDecisionReason"] = (
        "ZABLOKOWANO: polecenie pasuje do destrukcyjnego wzorca."
    )
print(json.dumps(output, ensure_ascii=False))