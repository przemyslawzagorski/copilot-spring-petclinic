"""Pamiec dlugoterminowa agenta na Qdrant.

Dwa tryby, jedno API:
  * lokalny (domyslny) - Qdrant embedded w katalogu `.qdrant_local`, dziala offline,
  * chmurowy - gdy ustawisz QDRANT_URL + QDRANT_API_KEY (darmowy klaster Qdrant Cloud).

Nazwa kolekcji zawiera podpis embeddera (np. `devkit_notes_fe384bgesm`). Dzieki temu
zmiana modelu embeddingow tworzy nowa kolekcje zamiast wysypywac sie na niezgodnosci
wymiarow - stare wektory zostaja nienaruszone.
"""

from __future__ import annotations

import functools
import logging
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, TypeVar

from .config import settings
from .embeddings import get_embedder
from .http import DevKitError

log = logging.getLogger("devkit.memory")

# Import na poziomie modulu, nie w srodku funkcji. qdrant_client ciagnie numpy
# (kilkadziesiat natywnych .pyd). Leniwy import w trakcie obslugi wywolania potrafi
# zakleszczyc sie na blokadach importu, gdy petla zdarzen i watki robocze wchodza
# w niego rownoczesnie - a przy okazji pierwsze wywolanie trwaloby 6 sekund.
try:
    from qdrant_client import QdrantClient, models

    QDRANT_AVAILABLE = True
except ImportError:  # pragma: no cover
    QdrantClient = None  # type: ignore[assignment,misc]
    models = None  # type: ignore[assignment]
    QDRANT_AVAILABLE = False

NAMESPACE = uuid.UUID("6f3d9f9e-2f5a-4d0e-9f0b-1d2c3a4b5c6d")
_client: Any = None
_ensured: set[str] = set()

# Qdrant w trybie embedded ma jednego pisarza i nie jest bezpieczny watkowo,
# a klient MCP potrafi wyslac kilka wywolan rownolegle. Jeden zamek na wszystkie
# operacje pamieci jest tu tansza i pewniejsza opcja niz pula polaczen.
_LOCK = threading.RLock()

F = TypeVar("F", bound=Callable[..., Any])


def synchronized(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with _LOCK:
            return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


def _qdrant():
    global _client
    if _client is not None:
        return _client
    if not QDRANT_AVAILABLE:  # pragma: no cover
        raise DevKitError("Brak pakietu qdrant-client. Zainstaluj: pip install qdrant-client")

    s = settings()
    try:
        if s.qdrant_url:
            _client = QdrantClient(url=s.qdrant_url, api_key=s.qdrant_api_key, timeout=s.http_timeout)
            log.info("Qdrant: tryb zdalny (%s)", s.qdrant_url)
        else:
            s.qdrant_path.mkdir(parents=True, exist_ok=True)
            _client = QdrantClient(path=str(s.qdrant_path))
            log.info("Qdrant: tryb lokalny (%s)", s.qdrant_path)
    except Exception as exc:
        if "already accessed by another instance" in str(exc):
            raise DevKitError(
                f"Lokalna baza Qdrant ({s.qdrant_path}) jest zajeta przez inny proces. "
                "Tryb embedded dopuszcza jednego pisarza - zamknij druga sesje serwera "
                "albo przelacz sie na Qdrant Cloud (QDRANT_URL)."
            ) from exc
        raise DevKitError(f"Nie udalo sie polaczyc z Qdrant: {exc}") from exc
    return _client


def close() -> None:
    global _client, _ensured
    if _client is not None:
        try:
            _client.close()
        except Exception:  # pragma: no cover
            pass
        _client = None
        _ensured = set()


def collection_name(base: str) -> str:
    """Pelna nazwa kolekcji = prefiks + nazwa logiczna + podpis embeddera."""
    return f"{settings().collection_prefix}_{base}_{get_embedder().tag}"


@synchronized
def ensure_collection(base: str) -> str:

    name = collection_name(base)
    if name in _ensured:
        return name
    client = _qdrant()
    if not client.collection_exists(name):
        client.create_collection(
            collection_name=name,
            vectors_config=models.VectorParams(size=get_embedder().dim, distance=models.Distance.COSINE),
        )
        # Indeksy payloadu - bez nich filtrowanie po tagach w trybie zdalnym jest wolne.
        # W trybie embedded Qdrant ich nie uzywa, wiec nie ma po co ich zakladac.
        if settings().qdrant_url:
            for field_name in ("tags", "source"):
                try:
                    client.create_payload_index(
                        name, field_name=field_name, field_schema=models.PayloadSchemaType.KEYWORD
                    )
                except Exception as exc:  # pragma: no cover
                    log.warning("Nie udalo sie zalozyc indeksu %s: %s", field_name, exc)
        log.info("Utworzono kolekcje %s", name)
    _ensured.add(name)
    return name


def _point_id(seed: str) -> str:
    return str(uuid.uuid5(NAMESPACE, seed))


@synchronized
def save(
    text: str,
    *,
    title: str | None = None,
    tags: list[str] | None = None,
    source: str | None = None,
    base: str = "notes",
    point_seed: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Zapisuje jeden wpis. `point_seed` daje idempotencje (ten sam seed = nadpisanie)."""

    text = text.strip()
    if not text:
        raise DevKitError("Pusta tresc - nie ma czego zapisac.")

    name = ensure_collection(base)
    vector = get_embedder().embed([text])[0]
    note_id = _point_id(point_seed or f"{time.time_ns()}:{text[:200]}")
    payload = {
        "text": text,
        "title": title or text.splitlines()[0][:120],
        "tags": [t.strip().lower() for t in (tags or []) if t.strip()],
        "source": source or "",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "chars": len(text),
    }
    if extra:
        payload.update(extra)

    _qdrant().upsert(name, points=[models.PointStruct(id=note_id, vector=vector, payload=payload)])
    return {"id": note_id, "collection": name, "title": payload["title"], "tags": payload["tags"]}


@synchronized
def save_many(items: list[dict[str, Any]], *, base: str) -> int:
    """Zapis wsadowy - jedno wywolanie embeddera na cala partie (duzo szybsze)."""

    if not items:
        return 0
    name = ensure_collection(base)
    vectors = get_embedder().embed([item["text"] for item in items])
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    points = []
    for item, vector in zip(items, vectors):
        payload = {
            "text": item["text"],
            "title": item.get("title", ""),
            "tags": item.get("tags", []),
            "source": item.get("source", ""),
            "created_at": now,
            "chars": len(item["text"]),
        }
        payload.update(item.get("extra", {}))
        points.append(models.PointStruct(id=_point_id(item["seed"]), vector=vector, payload=payload))
    _qdrant().upsert(name, points=points)
    return len(points)


@synchronized
def search(
    query: str,
    *,
    limit: int = 5,
    tags: list[str] | None = None,
    base: str = "notes",
    score_threshold: float | None = None,
) -> list[dict[str, Any]]:

    name = collection_name(base)
    client = _qdrant()
    if not client.collection_exists(name):
        return []

    query_filter = None
    if tags:
        query_filter = models.Filter(
            must=[models.FieldCondition(key="tags", match=models.MatchAny(any=[t.lower() for t in tags]))]
        )

    vector = get_embedder().embed([query], query=True)[0]
    hits = client.query_points(
        name,
        query=vector,
        limit=limit,
        query_filter=query_filter,
        score_threshold=score_threshold,
        with_payload=True,
    ).points
    return [
        {
            "id": str(hit.id),
            "score": round(float(hit.score), 4),
            "title": (hit.payload or {}).get("title", ""),
            "text": (hit.payload or {}).get("text", ""),
            "tags": (hit.payload or {}).get("tags", []),
            "source": (hit.payload or {}).get("source", ""),
            "created_at": (hit.payload or {}).get("created_at", ""),
        }
        for hit in hits
    ]


@synchronized
def recent(limit: int = 10, base: str = "notes") -> list[dict[str, Any]]:
    name = collection_name(base)
    client = _qdrant()
    if not client.collection_exists(name):
        return []
    points, _ = client.scroll(name, limit=max(limit * 5, 50), with_payload=True, with_vectors=False)
    rows = [
        {
            "id": str(point.id),
            "title": (point.payload or {}).get("title", ""),
            "tags": (point.payload or {}).get("tags", []),
            "source": (point.payload or {}).get("source", ""),
            "created_at": (point.payload or {}).get("created_at", ""),
            "chars": (point.payload or {}).get("chars", 0),
        }
        for point in points
    ]
    rows.sort(key=lambda row: row["created_at"], reverse=True)
    return rows[:limit]


@synchronized
def get(note_id: str, base: str = "notes") -> dict[str, Any] | None:
    name = collection_name(base)
    client = _qdrant()
    if not client.collection_exists(name):
        return None
    found = client.retrieve(name, ids=[note_id], with_payload=True)
    if not found:
        return None
    return {"id": str(found[0].id), **(found[0].payload or {})}


@synchronized
def delete(note_id: str, base: str = "notes") -> bool:

    name = collection_name(base)
    client = _qdrant()
    if not client.collection_exists(name):
        return False
    client.delete(name, points_selector=models.PointIdsList(points=[note_id]))
    return True


@synchronized
def drop(base: str) -> bool:
    name = collection_name(base)
    client = _qdrant()
    if not client.collection_exists(name):
        return False
    client.delete_collection(name)
    _ensured.discard(name)
    return True


@synchronized
def list_collections() -> list[dict[str, Any]]:
    client = _qdrant()
    prefix = settings().collection_prefix
    out = []
    for collection in client.get_collections().collections:
        if not collection.name.startswith(prefix):
            continue
        info = client.get_collection(collection.name)
        vectors = info.config.params.vectors
        out.append(
            {
                "collection": collection.name,
                "points": info.points_count,
                "vector_size": getattr(vectors, "size", None),
            }
        )
    return sorted(out, key=lambda row: row["collection"])


def chunk_text(text: str, *, chunk_chars: int = 1200, overlap: int = 150) -> list[str]:
    """Dzieli tekst po akapitach, nie w polowie zdania - mniej rozjechanego kontekstu."""
    text = text.strip()
    if len(text) <= chunk_chars:
        return [text] if text else []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(paragraph) > chunk_chars:
            if current:
                chunks.append(current.strip())
                current = ""
            step = max(chunk_chars - overlap, 1)
            for start in range(0, len(paragraph), step):
                piece = paragraph[start : start + chunk_chars].strip()
                if piece:
                    chunks.append(piece)
            continue
        if len(current) + len(paragraph) + 2 > chunk_chars:
            if current:
                chunks.append(current.strip())
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current.strip():
        chunks.append(current.strip())
    return chunks
