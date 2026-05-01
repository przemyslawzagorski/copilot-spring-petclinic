"""
Rozwiązanie ex_28 — Streaming odpowiedzi.

Co pokazuje:
- `streaming=True` w `create_session(...)` powoduje emisję
  `AssistantMessageDeltaData` (chunki tekstu) zanim model zakonczy
  generowanie. Dzieki temu mozesz drukowac/forwardowac odpowiedz
  inkrementalnie (np. do UI).
- Po zakonczeniu modelowej tury i tak otrzymasz pelny `AssistantMessageData`
  oraz `SessionIdleData` — uzywamy tego do oczekiwania na koniec.

Uruchomienie: `python streaming_chat.py`
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from copilot import CopilotClient
from copilot.generated.session_events import (
    AssistantMessageData,
    AssistantMessageDeltaData,
    SessionIdleData,
)
from copilot.session import PermissionHandler

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import ensure_copilot_cli_on_path  # noqa: E402


PROMPT = (
    "Po polsku, w 4-5 krotkich punktach, opisz typowy przeplyw zadania "
    "POST /owners/new w Spring PetClinic od kontrolera do bazy."
)


async def main() -> int:
    ensure_copilot_cli_on_path()

    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="auto",
            streaming=True,
        ) as session:
            done = asyncio.Event()
            chunk_count = 0
            final_chars = 0

            def on_event(event):
                nonlocal chunk_count, final_chars
                match event.data:
                    case AssistantMessageDeltaData() as data:
                        chunk_count += 1
                        delta = data.delta_content or ""
                        # write zamiast print, aby uniknac dodatkowych newlinow
                        sys.stdout.write(delta)
                        sys.stdout.flush()
                    case AssistantMessageData() as data:
                        final_chars = len(data.content or "")
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(PROMPT)
            await asyncio.wait_for(done.wait(), timeout=120)

            print()  # nowa linia po streamie
            print(f"[stats] chunkow={chunk_count}  final_len={final_chars}")
            # sanity: streaming powinien dac >1 chunk; jesli 0, model ich nie wysyla
            return 0 if chunk_count > 0 else 3


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
