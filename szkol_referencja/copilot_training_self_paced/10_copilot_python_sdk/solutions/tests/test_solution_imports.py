"""Offline compatibility checks for every module 10 solution."""

from __future__ import annotations

import runpy
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest


SOLUTIONS_DIR = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "relative_path",
    [
        "ex_25_setup/smoke_test.py",
        "ex_26_hello_chat/hello_chat.py",
        "ex_27_petclinic_assistant/petclinic_assistant.py",
        "ex_28_streaming/streaming_chat.py",
        "ex_29_custom_tool/custom_tool.py",
        "ex_30_live_demo/ai_server.py",
    ],
)
def test_solution_imports_with_current_sdk(relative_path: str) -> None:
    module_globals = runpy.run_path(str(SOLUTIONS_DIR / relative_path))
    assert "main" in module_globals or "app" in module_globals


def test_custom_tools_have_handlers() -> None:
    custom_tool = runpy.run_path(
        str(SOLUTIONS_DIR / "ex_29_custom_tool" / "custom_tool.py")
    )["get_vet_status"]
    ai_server = runpy.run_path(
        str(SOLUTIONS_DIR / "ex_30_live_demo" / "ai_server.py")
    )

    assert custom_tool.handler is not None
    assert ai_server["get_available_vets"].handler is not None
    assert ai_server["get_visit_load"].handler is not None
    assert ai_server["search_pet_owners"].handler is not None


def test_repo_root_points_to_maven_project() -> None:
    common = runpy.run_path(str(SOLUTIONS_DIR / "_common.py"))
    assert (common["repo_root"]() / "pom.xml").is_file()


def test_owner_history_contains_visit_dates() -> None:
    ai_server = runpy.run_path(
        str(SOLUTIONS_DIR / "ex_30_live_demo" / "ai_server.py")
    )
    text = ai_server["format_owner_history"](
        [
            {
                "firstName": "George",
                "lastName": "Franklin",
                "pets": [
                    {
                        "name": "Lucky",
                        "visits": [
                            {"date": "2026-07-20", "description": "Kontrola"}
                        ],
                    }
                ],
            }
        ],
        "Franklin",
    )

    assert "Lucky" in text
    assert "2026-07-20" in text
    assert "Kontrola" in text


@pytest.mark.asyncio
async def test_run_session_rejects_missing_authentication() -> None:
    ai_server = runpy.run_path(
        str(SOLUTIONS_DIR / "ex_30_live_demo" / "ai_server.py")
    )
    client = AsyncMock()
    client.__aenter__.return_value = client
    client.get_auth_status.return_value.isAuthenticated = False

    with patch.dict(ai_server["run_copilot_session"].__globals__, {"CopilotClient": lambda: client}):
        with pytest.raises(ai_server["CopilotUnavailableError"], match="copilot login"):
            await ai_server["run_copilot_session"]("test")