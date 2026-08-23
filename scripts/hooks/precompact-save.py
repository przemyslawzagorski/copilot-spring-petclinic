#!/usr/bin/env python3
"""
PreCompact hook — zapisuje notke o kompakcji kontekstu.
Przydatne do debugowania dlugich sesji agenta.
"""
import json
import os
import sys
from datetime import datetime

# Windows: konsola bywa w cp1250, a JSON musi byc UTF-8.
# Bez tego polskie znaki w komunikatach hooka wychodza jako krzaki.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

input_data = json.loads(sys.stdin.read())
trigger = input_data.get("trigger", "unknown")
transcript_path = input_data.get("transcript_path", "")

log_dir = os.path.join(os.getcwd(), ".copilot")
os.makedirs(log_dir, exist_ok=True)

with open(os.path.join(log_dir, "compaction.log"), "a", encoding="utf-8") as f:
    ts = datetime.now().isoformat()
    f.write(f"[{ts}] Kompakcja (trigger={trigger}). Transkrypt: {transcript_path}\n")

output = {
    "systemMessage": "Kontekst zapisany przed kompakcja.",
}
print(json.dumps(output, ensure_ascii=False))
