"""Test dymny DevKit MCP - odpala serwer jako podproces i gada z nim po protokole.

To jest weryfikacja od strony KLIENTA, nie import modulow: dokladnie tak samo
laczy sie Claude Code czy VS Code. Jesli to przechodzi, integracja jest sprawna.

Uruchomienie:
    python smoke_test.py            # testy offline + lokalne
    python smoke_test.py --network  # dodatkowo Jina Reader i wyszukiwarka
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path(__file__).resolve().parent / "devkit_server.py"
PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    (PASSED if condition else FAILED).append(name)
    mark = "OK  " if condition else "FAIL"
    print(f"  [{mark}] {name}{(' - ' + detail) if detail else ''}")


def payload(result) -> dict:
    """Wyciaga tresc z CallToolResult (structuredContent albo JSON z bloku tekstowego)."""
    if getattr(result, "structuredContent", None):
        data = result.structuredContent
        return data.get("result", data) if isinstance(data, dict) else data
    text = result.content[0].text if result.content else "{}"
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"text": text}


async def main(with_network: bool) -> int:
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            print(f"\n=== Polaczono: {init.serverInfo.name} v{init.serverInfo.version} ===\n")

            print("-- powierzchnia protokolu --")
            tools = (await session.list_tools()).tools
            resources = (await session.list_resources()).resources
            templates = (await session.list_resource_templates()).resourceTemplates
            prompts = (await session.list_prompts()).prompts
            check("tools zarejestrowane", len(tools) == 10, f"{len(tools)}: {', '.join(t.name for t in tools)}")
            check("resources zarejestrowane", len(resources) == 6, ", ".join(str(r.uri) for r in resources))
            check("resource template", len(templates) == 1, templates[0].uriTemplate if templates else "-")
            check("prompts zarejestrowane", len(prompts) == 5, ", ".join(p.name for p in prompts))
            check(
                "kazde narzedzie ma opis",
                all(tool.description for tool in tools),
                "opisy sa kontraktem dla modelu",
            )

            print("\n-- resources --")
            status = json.loads((await session.read_resource("devkit://status")).contents[0].text)
            check("devkit://status", "capabilities" in status, f"{len(status['capabilities'])} pozycji")
            check(
                "sekrety zamaskowane",
                all(len(v) <= 12 for v in status["keys"].values()),
                str(status["keys"]),
            )
            profile = json.loads((await session.read_resource("devkit://repo/profile")).contents[0].text)
            check(
                "devkit://repo/profile",
                profile.get("spring_boot_version") is not None,
                f"Spring Boot {profile.get('spring_boot_version')}, Java {profile.get('maven', {}).get('java_version')}",
            )
            cheatsheet = (await session.read_resource("devkit://cheatsheet")).contents[0].text
            check("devkit://cheatsheet", "deep_research" in cheatsheet)

            print("\n-- pamiec wektorowa --")
            saved = payload(
                await session.call_tool(
                    "memory_save",
                    {
                        "text": "Smoke test: CacheConfig cachuje vets i pets, wlascicieli nie.",
                        "title": "smoke: cache",
                        "tags": "smoke,cache",
                    },
                )
            )
            check("memory_save", bool(saved.get("id")), saved.get("id", "")[:8])
            found = payload(await session.call_tool("memory_search", {"query": "co jest cachowane w projekcie", "limit": 3}))
            check("memory_search", found["count"] >= 1, f"{found['count']} trafien")
            note = (await session.read_resource(f"devkit://memory/note/{saved['id']}")).contents[0].text
            check("devkit://memory/note/{id}", "smoke: cache" in note)
            deleted = payload(await session.call_tool("memory_delete", {"note_id": saved["id"]}))
            check("memory_delete", deleted.get("deleted") is True)

            print("\n-- RAG po repo --")
            indexed = payload(
                await session.call_tool(
                    "index_path",
                    {"patterns": "src/main/java/org/springframework/samples/petclinic/owner/*.java", "max_files": 12},
                )
            )
            check("index_path", indexed["chunks"] > 0, f"{indexed['files']} plikow / {indexed['chunks']} fragmentow")
            answer = payload(
                await session.call_tool(
                    "ask_repo", {"question": "gdzie obslugiwany jest formularz wlasciciela", "synthesize": False}
                )
            )
            check("ask_repo", answer["hits_used"] > 0, f"top: {answer['sources'][0]['file'] if answer['sources'] else '-'}")

            print("\n-- bezpieczenstwo --")
            blocked = await session.call_tool("read_page", {"url": "http://169.254.169.254/latest/meta-data/"})
            check("SSRF zablokowany", blocked.isError is True, "adres link-local odrzucony")
            bad_scheme = await session.call_tool("read_page", {"url": "file:///etc/passwd"})
            check("schemat file:// odrzucony", bad_scheme.isError is True)
            outside = await session.call_tool("index_path", {"patterns": "../../../../*.md"})
            check("indeksowanie poza repo puste", payload(outside)["files"] == 0, "glob nie wychodzi poza korzen")

            print("\n-- prompty --")
            briefing = await session.get_prompt("context_briefing", {"task": "dodac endpoint REST dla wizyt"})
            text = briefing.messages[0].content.text
            check("context_briefing", "devkit://repo/profile" in text and "memory_search" in text)
            research = await session.get_prompt("research_library", {"library": "Spring Boot 4", "question": "SSL"})
            check("research_library", "deep_research" in research.messages[0].content.text)

            if with_network:
                print("\n-- siec --")
                page = payload(await session.call_tool("read_page", {"url": "https://example.com", "max_chars": 500}))
                check("read_page (Jina Reader)", "Example Domain" in page.get("title", ""), page.get("provider", ""))
                hits = payload(await session.call_tool("web_search", {"query": "spring petclinic github", "max_results": 3}))
                check(
                    "web_search",
                    len(hits.get("results", [])) > 0,
                    f"provider={hits.get('provider')} degraded={hits.get('degraded')}",
                )

    print(f"\n=== {len(PASSED)} OK, {len(FAILED)} FAIL ===")
    if FAILED:
        print("Nieudane: " + ", ".join(FAILED))
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main("--network" in sys.argv)))
