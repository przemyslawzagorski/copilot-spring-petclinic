"""PostToolUse hook uruchamiający Prettier dla wspieranych plików tekstowych."""

import json
from pathlib import Path
import subprocess
import sys


SUPPORTED_SUFFIXES = {".css", ".html", ".js", ".json", ".md", ".scss", ".yaml", ".yml"}

input_data = json.load(sys.stdin)
tool_input = input_data.get("tool_input", {})
raw_path = next(
    (str(tool_input[key]) for key in ("filePath", "file_path", "path", "file") if key in tool_input),
    "",
)

if raw_path:
    file_path = Path(raw_path).resolve()
    workspace = Path.cwd().resolve()
    if file_path.is_file() and workspace in file_path.parents and file_path.suffix.lower() in SUPPORTED_SUFFIXES:
        subprocess.run(
            ["npx", "prettier", "--write", str(file_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

event_name = input_data.get("hookEventName", "PostToolUse")
print(json.dumps({"hookSpecificOutput": {"hookEventName": event_name}}))