"""DevKit MCP - serwer MCP dla realnej pracy programisty.

Pelna powierzchnia protokolu MCP:
  * TOOLS     - czynnosci (szukaj, czytaj, zapamietaj, zaindeksuj, deleguj),
  * RESOURCES - kontekst do wciagniecia (status, profil repo, pamiec agenta),
  * PROMPTS   - gotowe przeplywy pracy (research, triage logow, decyzja ADR).

Uruchomienie:  python devkit_server.py            (transport stdio)
Diagnostyka:   python devkit_server.py --selftest (bez klienta MCP)
"""

from __future__ import annotations

import atexit
import json
import logging
import os
import sys
from functools import partial
from pathlib import Path
from typing import Any, Callable

# Pakiet `devkit` lezy obok tego pliku - dzialamy niezaleznie od cwd klienta MCP.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import anyio.to_thread  # noqa: E402
from mcp.server.fastmcp import FastMCP  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

from devkit import http, llm, memory, readers, repo, search  # noqa: E402
from devkit.config import capabilities, mask, settings  # noqa: E402
from devkit.embeddings import get_embedder  # noqa: E402

# KRYTYCZNE dla transportu stdio: stdout nalezy do protokolu JSON-RPC.
# Kazdy print() na stdout rozwala ramkowanie wiadomosci - logi ida na stderr.
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)  # bez szumu z kazdego requestu
log = logging.getLogger("devkit")

if sys.platform == "win32":  # polskie znaki w logach na Windows
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

INSTRUCTIONS = """\
DevKit MCP laczy research w sieci, pamiec wektorowa i szybkiego sub-agenta LLM.

Kiedy czego uzywac:
  * `web_search` + `read_page` - gdy potrzebujesz swiezej wiedzy spoza repo,
  * `deep_research` - gdy chcesz gotowa synteze zamiast piecu surowych stron w kontekscie,
  * `index_path` + `ask_repo` - pytania o TEN kod bez wciagania plikow do kontekstu,
  * `memory_save` / `memory_search` - wnioski, decyzje i pulapki, ktore maja przetrwac sesje,
  * `delegate` - zrzuc mechaniczne podzadanie (klasyfikacja logow, regexp, skrypt) na tani model.

Zanim cos zalozysz o projekcie, przeczytaj resource `devkit://repo/profile`.
Stan konfiguracji i to, co jest wylaczone, pokazuje `devkit://status`.
"""

mcp = FastMCP("DevKit RAG", instructions=INSTRUCTIONS)

READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True)
READ_ONLY_LOCAL = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False)
WRITES_MEMORY = ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False)


async def off_loop(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Uruchamia blokujacy kod w watku roboczym.

    FastMCP wywoluje synchroniczne narzedzia wprost w petli zdarzen - 30-sekundowy
    request HTTP zablokowalby wtedy caly serwer (lacznie z anulowaniem i innymi
    wywolaniami). Dostep do Qdranta serializuje zamek w `devkit.memory`.
    """
    return await anyio.to_thread.run_sync(partial(func, *args, **kwargs))


def _tags(raw: str | None) -> list[str]:
    return [tag.strip().lower() for tag in (raw or "").split(",") if tag.strip()]


# ============================================================================
# TOOLS - RESEARCH W SIECI
# ============================================================================


@mcp.tool(title="Szukaj w sieci", annotations=READ_ONLY)
async def web_search(
    query: str,
    max_results: int = 5,
    depth: str = "basic",
    include_domains: str = "",
) -> dict[str, Any]:
    """Szuka w internecie i zwraca wyniki przygotowane pod RAG (tytul, URL, snippet, score).

    Uzywa Tavily, gdy jest TAVILY_API_KEY (najlepsza jakosc snippetow), inaczej schodzi
    na Jina Search, a w ostatecznosci na DuckDuckGo (pole `degraded: true`).

    Args:
        query: Fraza wyszukiwania - konkretna, jak do wyszukiwarki, nie jak do czlowieka.
        max_results: Liczba wynikow 1-15 (domyslnie 5).
        depth: "basic" (szybko) albo "advanced" (glebiej, tylko Tavily).
        include_domains: Opcjonalna lista domen po przecinku, np. "docs.spring.io,github.com".

    Returns:
        dict z kluczami: query, provider, degraded, answer, results[], notes[].
    """
    domains = [d.strip() for d in include_domains.split(",") if d.strip()]
    return await off_loop(
        search.web_search, query, max_results=max_results, depth=depth, include_domains=domains or None
    )


@mcp.tool(title="Czytaj strone jako Markdown", annotations=READ_ONLY)
async def read_page(
    url: str,
    max_chars: int = 8000,
    with_links: bool = False,
    no_cache: bool = False,
) -> dict[str, Any]:
    """Zamienia dowolny URL w czysty Markdown przez Jina Reader (bez HTML-owego szumu).

    Dziala bez klucza API (limit i cache), JINA_API_KEY podnosi limity.
    Adresy prywatne/loopback sa blokowane (ochrona SSRF).

    Args:
        url: Pelny adres http(s).
        max_chars: Twardy limit znakow tresci - chron swoje okno kontekstu (domyslnie 8000).
        with_links: Dolacz podsumowanie linkow ze strony (przydatne przy dokumentacji).
        no_cache: Wymus swieze pobranie zamiast snapshotu z cache (wymaga JINA_API_KEY).

    Returns:
        dict: url, title, published, content (Markdown), chars, truncated, cached.
    """
    return await off_loop(
        readers.read_page, url, max_chars=max_chars, with_links=with_links, no_cache=no_cache
    )


def _deep_research(
    query: str, max_pages: int, save_as: str, tags: str, include_domains: str
) -> dict[str, Any]:
    max_pages = max(1, min(max_pages, 5))
    domains = [d.strip() for d in include_domains.split(",") if d.strip()]
    found = search.web_search(
        query, max_results=max(max_pages * 2, 5), depth="advanced", include_domains=domains or None
    )

    sources: list[dict[str, Any]] = []
    notes: list[str] = list(found.get("notes", []))
    for item in found.get("results", []):
        if len(sources) >= max_pages:
            break
        try:
            page = readers.read_page(item["url"], max_chars=6000)
        except http.DevKitError as exc:
            notes.append(f"pominieto {item['url']}: {exc}")
            continue
        sources.append(
            {
                "title": page["title"] or item.get("title", ""),
                "url": page["url"],
                "text": page["content"],
                "chars": page["chars"],
            }
        )

    if not sources:
        return {
            "query": query,
            "answer": "",
            "sources": [],
            "provider": found.get("provider"),
            "notes": notes + ["Nie udalo sie pobrac zadnej strony - sprobuj innej frazy lub podaj URL wprost."],
        }

    result: dict[str, Any] = {
        "query": query,
        "provider": found.get("provider"),
        "sources": [
            {"n": i, "title": s["title"], "url": s["url"], "chars": s["chars"]}
            for i, s in enumerate(sources, 1)
        ],
    }

    if llm.available():
        synthesis = llm.synthesize(query, sources)
        result["answer"] = synthesis["output"]
        result["synthesized_by"] = synthesis["model"]
        result["usage"] = synthesis["usage"]
    else:
        excerpts = "\n\n".join(
            f"[{i}] {s['title']} ({s['url']})\n{s['text'][:2500]}" for i, s in enumerate(sources, 1)
        )
        result["answer"] = ""
        result["raw_excerpts"], _ = http.truncate(excerpts, 12000)
        notes.append("Brak GROQ_API_KEY - zwrocono surowe wyciagi zamiast syntezy (zsyntetyzuj je sam).")

    if save_as.strip():
        body = result.get("answer") or result.get("raw_excerpts", "")
        result["saved"] = memory.save(
            f"# {save_as.strip()}\n\nPytanie: {query}\n\n{body}\n\nZrodla:\n"
            + "\n".join(f"[{s['n']}] {s['title']} - {s['url']}" for s in result["sources"]),
            title=save_as.strip(),
            tags=_tags(tags) or ["research"],
            source="deep_research",
        )

    result["notes"] = notes
    return result


@mcp.tool(
    title="Glebki research z synteza",
    annotations=ToolAnnotations(readOnlyHint=False, openWorldHint=True),
)
async def deep_research(
    query: str,
    max_pages: int = 3,
    save_as: str = "",
    tags: str = "",
    include_domains: str = "",
) -> dict[str, Any]:
    """Pelny cykl RAG w jednym wywolaniu: szukaj -> przeczytaj -> zsyntetyzuj -> (opcjonalnie) zapamietaj.

    To jest narzedzie ekonomii kontekstu: zamiast wciagac 5 stron dokumentacji do okna
    glownego agenta, ciezka robote robi tani model (Groq), a wraca 10-zdaniowa odpowiedz
    z cytowaniami [n] i lista zrodel. Bez GROQ_API_KEY zwraca przyciete wyciagi do
    samodzielnej syntezy.

    Args:
        query: Pytanie badawcze, np. "co zmienilo sie w Spring Boot 4 w konfiguracji SSL".
        max_pages: Ile stron faktycznie przeczytac (1-5, domyslnie 3).
        save_as: Jesli podane - tytul notatki zapisanej do pamieci wektorowej.
        tags: Tagi notatki po przecinku, np. "spring,upgrade".
        include_domains: Zawez wyszukiwanie do domen po przecinku.

    Returns:
        dict: answer, sources[], provider, saved (id notatki), notes[].
    """
    return await off_loop(_deep_research, query, max_pages, save_as, tags, include_domains)


# ============================================================================
# TOOLS - PAMIEC DLUGOTERMINOWA
# ============================================================================


@mcp.tool(title="Zapisz do pamieci", annotations=WRITES_MEMORY)
async def memory_save(
    text: str, title: str = "", tags: str = "", source: str = "", collection: str = "notes"
) -> dict[str, Any]:
    """Zapisuje wniosek/decyzje/pulapke do pamieci wektorowej, ktora przezyje sesje.

    Zapisuj to, czego nie da sie odtworzyc z kodu: DLACZEGO cos zrobiono tak, a nie inaczej,
    co juz probowano i nie zadzialalo, ustalenia z code review, gotchy srodowiskowe.

    Args:
        text: Tresc notatki (Markdown mile widziany).
        title: Krotki tytul; domyslnie pierwsza linia tekstu.
        tags: Tagi po przecinku - sluza pozniej do filtrowania, np. "decyzja,cache".
        source: Skad to pochodzi (URL, sciezka pliku, numer ticketu).
        collection: Logiczna kolekcja: "notes" (domyslnie) lub wlasna nazwa.

    Returns:
        dict: id, collection, title, tags.
    """
    return await off_loop(
        memory.save,
        text,
        title=title or None,
        tags=_tags(tags),
        source=source or None,
        base=collection,
    )


@mcp.tool(title="Szukaj w pamieci", annotations=READ_ONLY_LOCAL)
async def memory_search(
    query: str, limit: int = 5, tags: str = "", collection: str = "notes"
) -> dict[str, Any]:
    """Wyszukuje semantycznie w pamieci agenta (Qdrant) - pytaj naturalnym jezykiem.

    Args:
        query: Pytanie lub opis szukanej wiedzy.
        limit: Ile trafien zwrocic (domyslnie 5).
        tags: Zawez do tagow po przecinku.
        collection: Kolekcja do przeszukania ("notes", "repo", wlasna).

    Returns:
        dict: collection, count, hits[] (id, score, title, text, tags, source, created_at).
    """
    hits = await off_loop(
        memory.search, query, limit=limit, tags=_tags(tags) or None, base=collection
    )
    return {"collection": memory.collection_name(collection), "count": len(hits), "hits": hits}


@mcp.tool(
    title="Usun z pamieci",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
)
async def memory_delete(note_id: str, collection: str = "notes") -> dict[str, Any]:
    """Usuwa jeden wpis z pamieci po jego id (nieodwracalne).

    Args:
        note_id: UUID zwrocony przez memory_save / memory_search.
        collection: Kolekcja, w ktorej lezy wpis.
    """
    deleted = await off_loop(memory.delete, note_id, base=collection)
    return {"deleted": deleted, "id": note_id}


# ============================================================================
# TOOLS - RAG PO WLASNYM REPOZYTORIUM
# ============================================================================


def _index_path(patterns: str, collection: str, max_files: int, chunk_chars: int) -> dict[str, Any]:
    globs = [p.strip() for p in patterns.split(",") if p.strip()]
    if not globs:
        raise http.DevKitError("Podaj przynajmniej jeden wzorzec glob.")

    batch: list[dict[str, Any]] = []
    files = chunks = 0
    skipped: list[str] = []

    for path in repo.iter_files(globs, max_files=max_files):
        try:
            text = repo.read_text(path)
        except OSError as exc:
            skipped.append(f"{repo.rel(path)}: {exc}")
            continue
        pieces = memory.chunk_text(text, chunk_chars=chunk_chars)
        if not pieces:
            continue
        files += 1
        relative = repo.rel(path)
        for index, piece in enumerate(pieces):
            batch.append(
                {
                    "text": f"# {relative} (fragment {index + 1}/{len(pieces)})\n\n{piece}",
                    "title": f"{relative}#{index + 1}",
                    "tags": [path.suffix.lstrip(".").lower(), "repo"],
                    "source": relative,
                    "seed": f"{relative}:{index}",
                    "extra": {"chunk": index, "chunks_total": len(pieces)},
                }
            )
            chunks += 1
        if len(batch) >= 64:
            memory.save_many(batch, base=collection)
            batch = []

    memory.save_many(batch, base=collection)
    return {
        "files": files,
        "chunks": chunks,
        "collection": memory.collection_name(collection),
        "embedder": get_embedder().name,
        "skipped": skipped[:10],
    }


@mcp.tool(title="Zaindeksuj pliki repo", annotations=WRITES_MEMORY)
async def index_path(
    patterns: str = "src/main/java/**/*.java",
    collection: str = "repo",
    max_files: int = 200,
    chunk_chars: int = 1200,
) -> dict[str, Any]:
    """Indeksuje pliki projektu do bazy wektorowej, zeby pytac o nie bez czytania ich w calosci.

    Idempotentne: ten sam plik i ten sam fragment daja to samo id, wiec ponowne
    uruchomienie aktualizuje wpisy zamiast mnozyc duplikaty.

    Args:
        patterns: Wzorce glob po przecinku, np. "src/main/java/**/*.java,docs/**/*.md".
        collection: Kolekcja docelowa (domyslnie "repo").
        max_files: Bezpiecznik na liczbe plikow (domyslnie 200).
        chunk_chars: Rozmiar fragmentu w znakach (domyslnie 1200).

    Returns:
        dict: files, chunks, collection, embedder, skipped[].
    """
    return await off_loop(_index_path, patterns, collection, max_files, chunk_chars)


def _ask_repo(question: str, limit: int, collection: str, synthesize: bool) -> dict[str, Any]:
    hits = memory.search(question, limit=limit, base=collection)
    if not hits:
        return {
            "answer": "",
            "sources": [],
            "hits_used": 0,
            "notes": [
                f"Kolekcja '{memory.collection_name(collection)}' jest pusta. "
                "Najpierw uruchom index_path(patterns='src/main/java/**/*.java')."
            ],
        }

    sources = [
        {"title": hit["source"] or hit["title"], "url": hit["source"], "text": hit["text"]} for hit in hits
    ]
    result: dict[str, Any] = {
        "hits_used": len(hits),
        "sources": [
            {"n": i, "file": hit["source"], "score": hit["score"], "title": hit["title"]}
            for i, hit in enumerate(hits, 1)
        ],
        "notes": [],
    }

    if synthesize and llm.available():
        synthesis = llm.synthesize(question, sources)
        result["answer"] = synthesis["output"]
        result["synthesized_by"] = synthesis["model"]
        result["usage"] = synthesis["usage"]
    else:
        excerpts = "\n\n".join(f"[{i}] {hit['source']}\n{hit['text']}" for i, hit in enumerate(hits, 1))
        result["answer"] = ""
        result["raw_excerpts"], _ = http.truncate(excerpts, 12000)
        if not llm.available():
            result["notes"].append("Brak GROQ_API_KEY - zwrocono fragmenty zamiast syntezy.")

    return result


@mcp.tool(title="Zapytaj o kod repo (RAG)", annotations=READ_ONLY_LOCAL)
async def ask_repo(
    question: str, limit: int = 6, collection: str = "repo", synthesize: bool = True
) -> dict[str, Any]:
    """Odpowiada na pytania o TEN projekt na podstawie zaindeksowanych fragmentow kodu.

    Wymaga wczesniejszego `index_path`. Zwraca odpowiedz z cytowaniami [n] oraz liste
    plikow zrodlowych - dzieki temu wiesz, gdzie zajrzec, zanim otworzysz cokolwiek.

    Args:
        question: Pytanie o kod, np. "gdzie walidowany jest formularz wlasciciela?".
        limit: Ile fragmentow pobrac z bazy (domyslnie 6).
        collection: Kolekcja z indeksem (domyslnie "repo").
        synthesize: Czy zsyntetyzowac odpowiedz taniej (Groq). False = same fragmenty.

    Returns:
        dict: answer, sources[] (plik + score), hits_used, notes[].
    """
    return await off_loop(_ask_repo, question, limit, collection, synthesize)


# ============================================================================
# TOOLS - DELEGOWANIE DO SZYBKIEGO MODELU
# ============================================================================


@mcp.tool(
    title="Deleguj podzadanie",
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
)
async def delegate(task: str, content: str = "", model: str = "", max_tokens: int = 1024) -> dict[str, Any]:
    """Zrzuca mechaniczne podzadanie na szybki, tani model (Groq) - bez obciazania glownego kontekstu.

    Dobre zastosowania: klasyfikacja bledow z logow, streszczenie 2000 linii diffu,
    wygenerowanie jednorazowego skryptu bash/regexpa, ekstrakcja pol z JSON-a.
    Zle zastosowania: decyzje architektoniczne i wszystko, co wymaga wiedzy o repo.

    Args:
        task: Precyzyjna instrukcja dla sub-agenta (co ma zrobic i w jakim formacie zwrocic).
        content: Duzy material wejsciowy (logi, diff, JSON) - trzymany poza glownym kontekstem.
        model: Nadpisanie modelu, np. "llama-3.1-8b-instant" (szybszy, tanszy).
        max_tokens: Limit dlugosci odpowiedzi.

    Returns:
        dict: model, output, usage (tokeny + czas).
    """
    prompt = f"{task}\n\n--- MATERIAL ---\n{content}" if content.strip() else task
    return await off_loop(
        llm.complete,
        prompt,
        system="Jestes precyzyjnym asystentem inzynierskim. Odpowiadasz zwiezle, w zadanym formacie, bez wstepow.",
        model=model or None,
        max_tokens=max_tokens,
    )


@mcp.tool(title="Model specjalistyczny (Hugging Face)", annotations=READ_ONLY)
async def hf_infer(model: str, inputs: str, parameters_json: str = "") -> Any:
    """Wywoluje model z Hugging Face Inference API (OCR, ASR, klasyfikacja, NER...).

    Opcjonalne - wymaga HF_API_KEY. Przydatne, gdy potrzebujesz modelu, ktorego nie ma
    w glownym stacku (np. odczyt tekstu ze zrzutu ekranu bledu).

    Args:
        model: Identyfikator modelu, np. "facebook/bart-large-cnn".
        inputs: Wejscie tekstowe dla modelu.
        parameters_json: Opcjonalny JSON z parametrami, np. '{"max_length": 120}'.
    """
    parameters = json.loads(parameters_json) if parameters_json.strip() else None
    return await off_loop(llm.hf_infer, model, inputs, parameters=parameters)


# ============================================================================
# RESOURCES - kontekst do wciagniecia przez klienta
# ============================================================================


@mcp.resource("devkit://status", title="Status serwera DevKit", mime_type="application/json")
def resource_status() -> dict[str, Any]:
    """Co jest skonfigurowane, co dziala w trybie degradowanym, a co wylaczone. Sekrety zamaskowane."""
    s = settings()
    return {
        "server": "DevKit RAG MCP",
        "repo_root": str(s.repo_root),
        "capabilities": capabilities(),
        "config": {
            "groq_model": s.groq_model,
            "embedding_provider": s.embedding_provider,
            "embedding_model": s.embedding_model,
            "qdrant": s.qdrant_url or f"local:{s.qdrant_path}",
            "collection_prefix": s.collection_prefix,
            "max_page_chars": s.max_page_chars,
            "allow_private_urls": s.allow_private_urls,
            "env_file": str(s.env_file) + ("" if s.env_file.exists() else " (brak - uzyte wartosci domyslne)"),
        },
        "keys": {
            "JINA_API_KEY": mask(s.jina_api_key),
            "TAVILY_API_KEY": mask(s.tavily_api_key),
            "GROQ_API_KEY": mask(s.groq_api_key),
            "HF_API_KEY": mask(s.hf_api_key),
            "QDRANT_API_KEY": mask(s.qdrant_api_key),
        },
    }


@mcp.resource("devkit://repo/profile", title="Profil projektu", mime_type="application/json")
async def resource_repo_profile() -> dict[str, Any]:
    """Stack, wersje (Java/Spring Boot), mapa pakietow, stan gita - zamiast zgadywania."""
    return await off_loop(repo.profile)


@mcp.resource("devkit://memory/collections", title="Kolekcje pamieci", mime_type="application/json")
async def resource_collections() -> dict[str, Any]:
    """Lista kolekcji w Qdrant wraz z liczba punktow."""
    collections = await off_loop(memory.list_collections)
    return {"embedder": get_embedder().name, "collections": collections}


@mcp.resource("devkit://memory/recent", title="Ostatnie notatki", mime_type="text/markdown")
async def resource_recent_notes() -> str:
    """20 ostatnich wpisow z pamieci - szybki podglad, co agent juz wie."""
    rows = await off_loop(memory.recent, 20)
    if not rows:
        return "# Pamiec DevKit\n\n_Brak notatek._ Zapisz pierwsza narzedziem `memory_save`."
    lines = ["# Ostatnie notatki DevKit", ""]
    for row in rows:
        tags = ", ".join(row["tags"]) or "-"
        lines.append(f"- **{row['title']}** - `{row['id']}` | {row['created_at']} | tagi: {tags}")
    return "\n".join(lines)


@mcp.resource("devkit://memory/note/{note_id}", title="Notatka", mime_type="text/markdown")
async def resource_note(note_id: str) -> str:
    """Pelna tresc pojedynczej notatki po jej id."""
    note = await off_loop(memory.get, note_id)
    if not note:
        return f"# Nie znaleziono\n\nNotatka `{note_id}` nie istnieje w kolekcji notes."
    return (
        f"# {note.get('title', note_id)}\n\n"
        f"- id: `{note_id}`\n- utworzono: {note.get('created_at', '?')}\n"
        f"- tagi: {', '.join(note.get('tags', [])) or '-'}\n- zrodlo: {note.get('source') or '-'}\n\n---\n\n"
        f"{note.get('text', '')}"
    )


@mcp.resource("devkit://llm/models", title="Modele Groq", mime_type="application/json")
async def resource_models() -> dict[str, Any]:
    """Modele dostepne dla Twojego klucza Groq (do ustawienia w GROQ_MODEL)."""
    if not llm.available():
        return {"available": False, "reason": "brak GROQ_API_KEY", "default": settings().groq_model}
    return {"available": True, "default": settings().groq_model, "models": await off_loop(llm.list_models)}


@mcp.resource("devkit://cheatsheet", title="Sciaga DevKit", mime_type="text/markdown")
def resource_cheatsheet() -> str:
    """Kiedy uzyc ktorego narzedzia - sciaga dla agenta i dla czlowieka."""
    return """\
# DevKit MCP - sciaga

| Potrzeba | Narzedzie |
|---|---|
| Swieza wiedza z sieci | `web_search` -> `read_page` |
| Gotowa odpowiedz zamiast 5 stron w kontekscie | `deep_research` |
| Pytanie o ten kod bez otwierania plikow | `index_path` (raz) -> `ask_repo` |
| Wniosek ma przezyc sesje | `memory_save` -> pozniej `memory_search` |
| Mechaniczna robota na duzym wejsciu | `delegate` |
| Wersje, stack, mapa pakietow | resource `devkit://repo/profile` |
| Co jest wlaczone/wylaczone | resource `devkit://status` |

## Przeplywy (prompty)

- `research_library` - zbadaj biblioteke i zapisz wnioski do pamieci
- `triage_logs` - sklasyfikuj bledy z logow tanim modelem, potem zaproponuj fix
- `capture_decision` - zapisz decyzje techniczna w formie ADR
- `rag_review` - review pliku z kontekstem repo i wczesniejszych ustalen
- `context_briefing` - brief na start zadania (profil repo + pamiec)

## Ekonomia kontekstu

`deep_research` i `delegate` celowo przetwarzaja material w tanim modelu i oddaja
tylko wynik. Surowe strony i logi nigdy nie wchodza do glownego okna kontekstu.
"""


# ============================================================================
# PROMPTS - gotowe przeplywy pracy
# ============================================================================


@mcp.prompt(title="Zbadaj biblioteke i zapamietaj")
def research_library(library: str, question: str = "") -> str:
    """Research zewnetrznej biblioteki/frameworka z zapisem wnioskow do pamieci."""
    focus = question.strip() or f"co warto wiedziec o {library} przed uzyciem w tym projekcie"
    return f"""\
Zbadaj temat: **{library}**. Pytanie badawcze: {focus}

Wykonaj po kolei:
1. Przeczytaj resource `devkit://repo/profile`, zeby znac wersje Javy i Spring Boota w tym projekcie.
2. Sprawdz `memory_search(query="{library}")` - byc moze juz to badalismy.
3. Jesli wiedzy brak lub jest stara, uruchom
   `deep_research(query="{library} {focus}", max_pages=3, save_as="{library}: {focus}", tags="research,{library}")`.
4. Odpowiedz mi w formacie:
   - **Werdykt** (2-3 zdania, czy pasuje do naszego stacku)
   - **Wersja zgodna z naszym Spring Boot**
   - **Ryzyka / breaking changes**
   - **Konkretny nastepny krok w tym repo**
5. Podaj id zapisanej notatki, zebym mogl do niej wrocic.

Nie wciagaj calych stron dokumentacji do kontekstu - od tego jest `deep_research`.
"""


@mcp.prompt(title="Triage logow")
def triage_logs(logs: str, service: str = "petclinic") -> str:
    """Klasyfikacja bledow z logow tanim modelem, potem propozycja poprawki."""
    return f"""\
Masz logi z uslugi **{service}**. Przeprowadz triage tanio i konkretnie:

1. Wywolaj `delegate` z zadaniem:
   "Pogrupuj bledy wedlug pierwotnej przyczyny. Dla kazdej grupy podaj: sygnature wyjatku,
    liczbe wystapien, pierwszy i ostatni timestamp, hipoteze przyczyny. Zwroc tabele Markdown."
   i przekaz logi w parametrze `content`. Uzyj modelu `llama-3.1-8b-instant`.
2. Dla najgrozniejszej grupy sprawdz `ask_repo(question="<sygnatura wyjatku> - gdzie w kodzie to powstaje")`.
3. Jesli to znany problem biblioteki, dorzuc `deep_research` na jego temat.
4. Zaproponuj poprawke: plik, linia, na czym polega zmiana. Nie zmieniaj jeszcze kodu.
5. Zapisz wniosek: `memory_save(text=..., title="Triage: <sygnatura>", tags="incydent,{service}")`.

LOGI:
```
{logs[:6000]}
```
"""


@mcp.prompt(title="Zapisz decyzje techniczna (ADR)")
def capture_decision(decision: str, context: str = "") -> str:
    """Zapis decyzji architektonicznej w formacie ADR do pamieci dlugoterminowej."""
    return f"""\
Zapisz nasza decyzje techniczna jako ADR w pamieci dlugoterminowej.

Decyzja: {decision}
Kontekst: {context or "(uzupelnij na podstawie biezacej sesji i stanu repo)"}

1. Sprawdz `memory_search(query="{decision}", tags="decyzja")` - czy nie zapadla juz sprzeczna decyzja.
2. Zloz notatke w formacie ADR:
   `# Tytul` / `## Status` / `## Kontekst` / `## Decyzja` / `## Konsekwencje` / `## Odrzucone alternatywy`.
3. Zapisz: `memory_save(text=<ADR>, title=<tytul>, tags="decyzja,adr", source="sesja Claude Code")`.
4. Pokaz mi zapisana tresc i id notatki.

Konsekwencje maja byc konkretne dla TEGO repo (pliki, moduly, testy), nie ogolnikowe.
"""


@mcp.prompt(title="Review z kontekstem repo")
def rag_review(file_path: str) -> str:
    """Review pliku z uwzglednieniem konwencji projektu i wczesniejszych ustalen."""
    return f"""\
Zrob review pliku `{file_path}` z pelnym kontekstem, nie w prozni:

1. `devkit://repo/profile` - wersje i konwencje projektu.
2. `memory_search(query="konwencje i decyzje dotyczace {file_path}")` - wczesniejsze ustalenia.
3. `ask_repo(question="jak inne klasy w tym projekcie rozwiazuja to samo co {file_path}")` - spojnosc ze wzorcami.
4. Przeczytaj plik i zglos uwagi w kolejnosci: **bledy poprawnosci** -> **bezpieczenstwo** -> **spojnosc z projektem** -> **uproszczenia**.

Dla kazdej uwagi podaj: linie, dlaczego to problem, konkretna poprawke.
Jesli uwaga wynika z zapamietanej decyzji - zacytuj jej id.
Nie zglaszaj stylistyki: formatowanie pilnuje `mvn spring-javaformat:apply`.
"""


@mcp.prompt(title="Brief na start zadania")
def context_briefing(task: str) -> str:
    """Zbiera kontekst przed rozpoczeciem zadania: profil repo + pamiec + luki w wiedzy."""
    return f"""\
Przygotuj mnie do zadania: **{task}**

1. `devkit://repo/profile` - stack, wersje, mapa pakietow, stan gita.
2. `memory_search(query="{task}", limit=8)` - co juz wiemy i jakie decyzje zapadly.
3. `ask_repo(question="ktore pliki sa istotne dla: {task}")` - punkty wejscia w kodzie.
4. Jesli zadanie dotyczy zewnetrznej biblioteki lub API, sprawdz aktualnosc: `deep_research`.

Oddaj brief (maks. 1 ekran):
- **Stan wyjsciowy** (co juz jest)
- **Pliki do ruszenia** (sciezki)
- **Wczesniejsze decyzje, ktorych nie wolno zlamac** (z id notatek)
- **Otwarte pytania do mnie**
- **Plan w 3-5 krokach**
"""


# ============================================================================
# START / DIAGNOSTYKA
# ============================================================================


def _prewarm() -> None:
    """Laduje model embeddingow przed startem petli zdarzen.

    Pierwsze `embed()` kosztuje kilka sekund (a przy pierwszym uruchomieniu takze
    pobranie modelu). Robimy to na starcie, zeby pierwsze wywolanie narzedzia nie
    wygladalo dla klienta jak zawieszenie. DEVKIT_PREWARM=false wylacza.
    """
    if os.getenv("DEVKIT_PREWARM", "true").strip().lower() not in {"1", "true", "yes", "on"}:
        return
    try:
        embedder = get_embedder()
        embedder.embed(["rozgrzewka"])
        log.info("Embedder gotowy: %s (dim=%s)", embedder.name, embedder.dim)
    except Exception as exc:  # serwer ma wstac nawet bez embeddingow
        log.warning("Nie udalo sie rozgrzac embeddera: %s", exc)


def _selftest() -> int:
    """Szybka diagnostyka bez klienta MCP - dobra pierwsza komenda po instalacji."""
    if sys.platform == "win32":
        # Tu (i tylko tu) stdout jest dla czlowieka, nie dla JSON-RPC - konsola
        # Windows domyslnie nie uniesie polskich znakow w raporcie.
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("=== DevKit MCP - selftest ===")
    for name, info in capabilities().items():
        hint = f"  ({info['hint']})" if info.get("hint") else ""
        print(f"  [{info['state']:<14}] {name}: {info['detail']}{hint}")

    print("\n--- profil repo ---")
    profile = repo.profile()
    print(f"  projekt: {profile.get('name')} ({profile.get('build')})")
    print(
        f"  Spring Boot: {profile.get('spring_boot_version')} | "
        f"Java: {profile.get('maven', {}).get('java_version')}"
    )
    print(f"  klasy main/test: {profile['counts']['main_java']}/{profile['counts']['test_java']}")

    print("\n--- pamiec (zapis + odczyt) ---")
    try:
        saved = memory.save(
            "Selftest DevKit: pamiec wektorowa dziala.",
            title="selftest",
            tags=["selftest"],
            point_seed="selftest",
        )
        hits = memory.search("czy pamiec dziala", limit=1)
        print(f"  zapis OK ({saved['id'][:8]}...), wyszukiwanie zwrocilo {len(hits)} trafien")
        memory.delete(saved["id"])
        print("  sprzatanie OK")
    except Exception as exc:
        print(f"  BLAD pamieci: {exc}")
        return 1

    print(
        f"\n  narzedzia: {len(mcp._tool_manager.list_tools())}, "
        f"resources: {len(mcp._resource_manager.list_resources())} + "
        f"{len(mcp._resource_manager.list_templates())} szablonow, "
        f"prompty: {len(mcp._prompt_manager.list_prompts())}"
    )
    print("\nOK - serwer gotowy do podpiecia w .mcp.json")
    return 0


atexit.register(http.close)
atexit.register(memory.close)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    log.info("DevKit MCP startuje (repo: %s)", settings().repo_root)
    _prewarm()
    mcp.run(transport="stdio")
