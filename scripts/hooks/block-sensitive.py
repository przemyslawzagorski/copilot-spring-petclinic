"""PreToolUse hook blokujący operacje na plikach wrażliwych."""

import json
import re
import sys


input_data = json.load(sys.stdin)
tool_input = input_data.get("tool_input", {})
file_path = next(
    (str(tool_input[key]) for key in ("filePath", "file_path", "path", "file") if key in tool_input),
    "",
)
patterns = (
    r"\.env($|\.)",
    r"secrets?[/\\]",
    r"credentials",
    r"prod.*\.(yml|yaml|properties)$",
    r"\.(pem|key|pfx|p12)$",
)
denied = any(re.search(pattern, file_path, re.IGNORECASE) for pattern in patterns)
if denied:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"ZABLOKOWANO: operacja na chronionej ścieżce '{file_path}'."
                    ),
                }
            },
            ensure_ascii=False,
        )
    )