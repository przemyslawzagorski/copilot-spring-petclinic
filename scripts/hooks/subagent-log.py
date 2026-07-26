"""Subagent hook potwierdzający lifecycle bez zapisywania danych sesji."""

import json
import sys


input_data = json.load(sys.stdin)
event_name = input_data.get("hookEventName", "SubagentStart")
if event_name not in {"SubagentStart", "SubagentStop"}:
    event_name = "SubagentStart"
print(json.dumps({"hookSpecificOutput": {"hookEventName": event_name}}))