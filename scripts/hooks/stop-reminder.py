"""Stop hook przypominający o testach bez blokowania zakończenia sesji."""

import json
import sys


json.load(sys.stdin)
print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": "Przed przekazaniem zmian potwierdź wynik testów.",
            }
        },
        ensure_ascii=False,
    )
)