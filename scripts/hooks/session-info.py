"""SessionStart hook przekazujący agentowi minimalny kontekst workspace."""

import json
import os
import sys


json.load(sys.stdin)
print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"Workspace: {os.getcwd()}",
            }
        }
    )
)