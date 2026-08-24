"""Wymienne embeddingi - pamiec dziala zawsze, jakosc rosnie wraz z konfiguracja.

Kolejnosc wyboru dla EMBEDDING_PROVIDER=auto:
  1. fastembed  - lokalny ONNX, offline, bez klucza (najlepszy default)
  2. jina       - API jina-embeddings-v3, gdy jest JINA_API_KEY
  3. hash       - deterministyczny hashing trick; bez zaleznosci, jakosc ograniczona
"""

from __future__ import annotations

import hashlib
import logging
import math
import re
from functools import lru_cache
from typing import Protocol

from .config import settings
from .http import DevKitError, request

log = logging.getLogger("devkit.embeddings")


class Embedder(Protocol):
    name: str
    tag: str  # krotki podpis uzywany w nazwie kolekcji (rozne modele = rozne kolekcje)
    dim: int

    def embed(self, texts: list[str], *, query: bool = False) -> list[list[float]]: ...


class FastEmbedEmbedder:
    """Lokalny model ONNX. Pierwsze uzycie pobiera wagi (~130 MB dla bge-small)."""

    def __init__(self, model_name: str) -> None:
        from fastembed import TextEmbedding

        self._model = TextEmbedding(model_name=model_name)
        self.name = f"fastembed:{model_name}"
        short = re.sub(r"[^a-z0-9]+", "", model_name.split("/")[-1].lower())[:12]
        probe = list(self._model.embed(["wymiar"]))[0]
        self.dim = len(probe)
        self.tag = f"fe{self.dim}{short[:6]}"

    def embed(self, texts: list[str], *, query: bool = False) -> list[list[float]]:
        vectors = self._model.query_embed(texts) if query else self._model.embed(texts)
        return [list(map(float, v)) for v in vectors]


class JinaEmbedder:
    """jina-embeddings-v3 przez API - rozroznia zadanie query vs passage (lepszy recall)."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self.name = "jina:jina-embeddings-v3"
        self.dim = 1024
        self.tag = "jina1024"

    def embed(self, texts: list[str], *, query: bool = False) -> list[list[float]]:
        payload = {
            "model": "jina-embeddings-v3",
            "task": "retrieval.query" if query else "retrieval.passage",
            "input": texts,
        }
        response = request(
            "POST",
            "https://api.jina.ai/v1/embeddings",
            headers={"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"},
            json_body=payload,
            service="jina-embeddings",
        )
        data = response.json().get("data", [])
        return [item["embedding"] for item in data]


class HashEmbedder:
    """Awaryjny embedder: hashing trick na slowach + trigramach, znormalizowany L2.

    Nie rozumie synonimow - laczy tylko dokladne pokrycie leksykalne. Wystarczy,
    zeby narzedzia pamieci dzialaly bez internetu i bez pobierania modelu.
    """

    def __init__(self, dim: int = 512) -> None:
        self.name = "hash:trigram-bow"
        self.dim = dim
        self.tag = f"hash{dim}"

    def _features(self, text: str) -> list[str]:
        words = re.findall(r"\w+", text.lower())
        feats = list(words)
        for word in words:
            padded = f" {word} "
            feats.extend(padded[i : i + 3] for i in range(len(padded) - 2))
        return feats

    def embed(self, texts: list[str], *, query: bool = False) -> list[list[float]]:
        out: list[list[float]] = []
        for text in texts:
            vector = [0.0] * self.dim
            for feat in self._features(text):
                digest = hashlib.blake2b(feat.encode("utf-8"), digest_size=8).digest()
                index = int.from_bytes(digest[:4], "big") % self.dim
                sign = 1.0 if digest[4] % 2 == 0 else -1.0
                vector[index] += sign
            norm = math.sqrt(sum(v * v for v in vector)) or 1.0
            out.append([v / norm for v in vector])
        return out


@lru_cache(maxsize=1)
def get_embedder() -> Embedder:
    """Wybiera embedder raz na proces (model ONNX ladowany leniwie i tylko raz)."""
    s = settings()
    provider = s.embedding_provider

    if provider in {"auto", "fastembed"}:
        try:
            embedder = FastEmbedEmbedder(s.embedding_model)
            log.info("Embeddingi: %s (dim=%s)", embedder.name, embedder.dim)
            return embedder
        except Exception as exc:  # brak pakietu, brak sieci przy pierwszym pobraniu modelu
            if provider == "fastembed":
                raise DevKitError(
                    f"EMBEDDING_PROVIDER=fastembed, ale model sie nie zaladowal: {exc}. "
                    "Zainstaluj `pip install fastembed` albo ustaw EMBEDDING_PROVIDER=hash."
                ) from exc
            log.warning("fastembed niedostepny (%s) - probuje dalej", exc)

    if provider in {"auto", "jina"} and s.jina_api_key:
        log.info("Embeddingi: Jina API")
        return JinaEmbedder(s.jina_api_key)
    if provider == "jina":
        raise DevKitError("EMBEDDING_PROVIDER=jina wymaga JINA_API_KEY w .env")

    log.warning("Embeddingi: fallback hashujacy - wyszukiwanie semantyczne bedzie plytkie")
    return HashEmbedder()


def describe_embedder() -> dict[str, str]:
    """Opis do resource'a `devkit://status` - bez ladowania modelu, jesli to zbedne."""
    s = settings()
    from importlib.util import find_spec

    if s.embedding_provider in {"auto", "fastembed"} and find_spec("fastembed"):
        return {
            "state": "ready",
            "detail": f"fastembed lokalnie: {s.embedding_model} (offline, bez klucza)",
        }
    if s.embedding_provider in {"auto", "jina"} and s.jina_api_key:
        return {"state": "ready", "detail": "jina-embeddings-v3 przez API"}
    return {
        "state": "ready-degraded",
        "detail": "fallback hashujacy - dopasowanie leksykalne, bez semantyki",
        "hint": "pip install fastembed  (albo ustaw JINA_API_KEY)",
    }
