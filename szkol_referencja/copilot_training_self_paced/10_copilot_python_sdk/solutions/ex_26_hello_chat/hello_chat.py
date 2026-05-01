"""
Rozwiązanie ex_26 — Hello chat.

Cel: pokazać minimalny szkielet sesji Copilot SDK:
1. otwieramy `CopilotClient` (asynchroniczny context manager)
2. tworzymy sesję z modelem `gpt-5` i wymaganym handlerem permissions
3. rejestrujemy handler eventów (`on_event`) i czekamy na `SessionIdleData`
4. drukujemy finalną odpowiedź modelu

Wymagana autoryzacja (jedno z poniższych):
- aktywna sesja po `copilot` (login zrobiony w CLI), albo
- `GITHUB_TOKEN` w środowisku (PAT z dostępem do Copilot).

Uruchomienie:  `python hello_chat.py`
"""

from __future__ import annotations

import asyncio
import sys

from copilot import CopilotClient
from copilot.generated.session_events import AssistantMessageData, SessionIdleData
from copilot.session import PermissionHandler

# pozwala importować _common.py z katalogu nadrzędnego (solutions/)
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from _common import ensure_copilot_cli_on_path  # noqa: E402


PROMPT = (
    "W jednym akapicie po polsku wyjasnij, czym jest Spring PetClinic — "
    "uzywaj zwiezlych zdan, max 60 slow."
)


async def main() -> int:
    ensure_copilot_cli_on_path()

    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="auto",
        ) as session:
            done = asyncio.Event()
            final_text: list[str] = []

            def on_event(event):
                # match po typie payloadu — SDK rozpakowuje JSON do dataclass
                match event.data:
                    case AssistantMessageData() as data:
                        final_text.append(data.content)
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(PROMPT)
            # 90 s zapasu — gpt-5 czasem dłużej rozkmina krótki prompt
            await asyncio.wait_for(done.wait(), timeout=90)

            print("--- ODPOWIEDZ ---")
            print("\n".join(final_text).strip())
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
