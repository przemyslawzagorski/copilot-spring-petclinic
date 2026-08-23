"""Stop hook przypominający o testach bez blokowania zakończenia sesji."""

import json
import sys

# Windows: konsola bywa w cp1250, a JSON musi byc UTF-8.
# Bez tego polskie znaki w komunikatach hooka wychodza jako krzaki.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


json.load(sys.stdin)
print(
    json.dumps(
        {
            "systemMessage": "Przed przekazaniem zmian potwierdź wynik testów."
        },
        ensure_ascii=False,
    )
)