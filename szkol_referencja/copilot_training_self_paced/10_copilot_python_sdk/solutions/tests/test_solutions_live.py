"""
Realne testy integracyjne dla rozwiazan modulu 10.

Kazdy test jest oznaczony markerem `live` — wymaga aktywnej autoryzacji
GitHub Copilot. Jesli jej brak, conftest.py automatycznie pomija (skip),
zeby nie sypal falszywie bledami.

Uwaga na koszt:
- Prompty sa krotkie i deterministyczne.
- Timeouty per test ograniczaja maksymalny czas oczekiwania.
- Liczba testow = 5; przy gpt-5 oczekiwany lacny czas ~3-5 min.

Uruchomienie: `pytest -m live -v`  (z katalogu modulu 10).
"""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path

import pytest

from copilot import CopilotClient, define_tool
from copilot.generated.session_events import (
    AssistantMessageData,
    AssistantMessageDeltaData,
    SessionIdleData,
)
from copilot.session import PermissionHandler
from pydantic import BaseModel, Field

SOLUTIONS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOLUTIONS_DIR))
from _common import ensure_copilot_cli_on_path, repo_root  # noqa: E402


pytestmark = [pytest.mark.live, pytest.mark.asyncio]


# ---------------------------------------------------------------------------
# ex_25 — smoke: list_models > 0
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_ex25_list_models_nonempty() -> None:
    ensure_copilot_cli_on_path()
    async with CopilotClient() as client:
        models = await client.list_models()
        assert len(models) > 0, "Lista modeli powinna byc niepusta po zalogowaniu"
        ids = {m.id for m in models}
        # 'auto' to stabilny alias rekomendowany przez SDK; jesli zniknie — alarm
        assert "auto" in ids, f"Brak modelu 'auto' w dostepnych: {sorted(ids)[:15]}"


# ---------------------------------------------------------------------------
# ex_26 — hello chat: model odpowiada na proste pytanie
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_ex26_hello_chat_returns_answer() -> None:
    ensure_copilot_cli_on_path()
    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="auto",
        ) as session:
            done = asyncio.Event()
            chunks: list[str] = []

            def on_event(event):
                match event.data:
                    case AssistantMessageData() as data:
                        if data.content:
                            chunks.append(data.content)
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send("Odpowiedz tylko liczba: ile to 2+2?")
            await asyncio.wait_for(done.wait(), timeout=90)

    full = " ".join(chunks)
    assert full.strip(), "Brak tresci w odpowiedzi modelu"
    assert "4" in full, f"Oczekiwano '4' w odpowiedzi, a otrzymano: {full!r}"


# ---------------------------------------------------------------------------
# ex_27 — petclinic assistant: agent generuje plik raportu w cwd
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_ex27_assistant_writes_report(tmp_workdir: Path, repo_root_dir: Path) -> None:
    # importujemy moduł rozwiazania (jego main pisze raport do cwd)
    sol_path = SOLUTIONS_DIR / "ex_27_petclinic_assistant" / "petclinic_assistant.py"
    spec = importlib.util.spec_from_file_location("petclinic_assistant_sol", sol_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    rc = await module.main()
    report = tmp_workdir / module.REPORT_NAME

    assert rc == 0, f"main() zwrocilo {rc}, oczekiwano 0"
    assert report.exists(), f"Brak pliku raportu w {report}"
    text = report.read_text(encoding="utf-8", errors="replace")
    assert len(text) > 200, "Raport podejrzanie krotki"
    # raport powinien wymieniac przynajmniej jedna znana encje JPA z modulu owner
    assert any(
        token in text for token in ("Owner", "Pet", "Visit")
    ), "Raport nie wspomina zadnych encji JPA z pakietu owner"


# ---------------------------------------------------------------------------
# ex_28 — streaming: dostajemy >1 chunk delty
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_ex28_streaming_emits_deltas() -> None:
    ensure_copilot_cli_on_path()
    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="auto",
            streaming=True,
        ) as session:
            done = asyncio.Event()
            deltas = 0
            final_len = 0

            def on_event(event):
                nonlocal deltas, final_len
                match event.data:
                    case AssistantMessageDeltaData():
                        deltas += 1
                    case AssistantMessageData() as data:
                        final_len = len(data.content or "")
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(
                "Wymien po polsku trzy zalety wzorca Repository — kazdy w jednym zdaniu."
            )
            await asyncio.wait_for(done.wait(), timeout=120)

    assert deltas > 1, f"Streaming powinien zwrocic wiele delty, a zwrocil: {deltas}"
    assert final_len > 50, f"Final message podejrzanie krotki: {final_len} znakow"


# ---------------------------------------------------------------------------
# ex_29 — custom tool: agent wywoluje nasze narzedzie i widzi jego wynik
# ---------------------------------------------------------------------------
class _VetParams(BaseModel):
    vet_id: int = Field(description="Numeryczny id weterynarza.")


@pytest.mark.asyncio
async def test_ex29_custom_tool_invoked() -> None:
    ensure_copilot_cli_on_path()

    call_log: list[int] = []

    @define_tool(
        name="get_vet_status_test",
        description="Zwraca status weterynarza dla testow integracyjnych.",
        params_type=_VetParams,
        skip_permission=True,
    )
    async def get_vet_status_test(params: _VetParams, _invocation) -> str:
        call_log.append(params.vet_id)
        # zwracamy wartownika, ktory MUSI pojawic sie w odpowiedzi modelu,
        # gdyby ten ja zacytowal — to dowod, ze model widzial wynik narzedzia
        return f"VET-{params.vet_id}-OK-XYZTOKEN"

    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="auto",
            tools=[get_vet_status_test],
        ) as session:
            done = asyncio.Event()
            answer: list[str] = []

            def on_event(event):
                match event.data:
                    case AssistantMessageData() as data:
                        if data.content:
                            answer.append(data.content)
                    case SessionIdleData():
                        done.set()

            session.on(on_event)
            await session.send(
                "Wywolaj narzedzie get_vet_status_test dla vet_id=7, "
                "a nastepnie powtorz doslownie wartosc, ktora ono zwrocilo."
            )
            await asyncio.wait_for(done.wait(), timeout=180)

    assert call_log == [7], f"Oczekiwano wywolania narzedzia z vet_id=7, log: {call_log}"
    full = " ".join(answer)
    assert "VET-7-OK-XYZTOKEN" in full, (
        f"Model nie zacytowal wartosci zwroconej przez narzedzie: {full!r}"
    )


# repo_root dostepny — uzywany przez ex_27 fixture
__all__ = ["repo_root"]
