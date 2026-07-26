"""UserPromptSubmit hook bezpiecznie potwierdzający zdarzenie bez logowania treści."""

import json
import sys


json.load(sys.stdin)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit"}}))