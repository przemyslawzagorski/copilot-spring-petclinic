"""Konfiguracja serwera DevKit MCP.

Wszystko sterowane zmiennymi srodowiskowymi (opcjonalnie z pliku .env obok pakietu).
Zasada projektowa: **brak klucza nie moze wywracac serwera**. Kazdy provider ma stan
(`ready` / `missing_key` / `missing_package`), a narzedzia degraduja sie kontrolowanie.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

try:  # python-dotenv jest opcjonalny
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv(*_args, **_kwargs):  # type: ignore[misc]
        return False


PACKAGE_DIR = Path(__file__).resolve().parent
MODULE_DIR = PACKAGE_DIR.parent  # .../mcp_devkit


def _find_repo_root(start: Path) -> Path:
    """Szuka korzenia repo w gore drzewa (marker: .git / pom.xml)."""
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists() or (candidate / "pom.xml").exists():
            return candidate
    return start


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, "").strip() or default)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    """Zamrozony snapshot konfiguracji, czytany raz przy starcie procesu."""

    # --- RAG / web ---
    jina_api_key: str | None
    tavily_api_key: str | None

    # --- LLM ---
    groq_api_key: str | None
    groq_model: str
    groq_base_url: str
    hf_api_key: str | None
    hf_api_url: str

    # --- pamiec wektorowa ---
    qdrant_url: str | None
    qdrant_api_key: str | None
    qdrant_path: Path
    collection_prefix: str
    embedding_provider: str  # auto | fastembed | jina | hash
    embedding_model: str

    # --- limity / bezpieczenstwo ---
    http_timeout: int
    max_page_chars: int
    max_response_chars: int
    allow_private_urls: bool

    repo_root: Path
    module_dir: Path = field(default=MODULE_DIR)

    @property
    def env_file(self) -> Path:
        return MODULE_DIR / ".env"


@lru_cache(maxsize=1)
def settings() -> Settings:
    load_dotenv(MODULE_DIR / ".env")

    repo_root_env = os.getenv("DEVKIT_REPO_ROOT")
    repo_root = Path(repo_root_env).resolve() if repo_root_env else _find_repo_root(MODULE_DIR)

    qdrant_path_env = os.getenv("QDRANT_PATH")
    qdrant_path = Path(qdrant_path_env) if qdrant_path_env else MODULE_DIR / ".qdrant_local"

    return Settings(
        jina_api_key=os.getenv("JINA_API_KEY") or None,
        tavily_api_key=os.getenv("TAVILY_API_KEY") or None,
        groq_api_key=os.getenv("GROQ_API_KEY") or None,
        groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        groq_base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
        hf_api_key=os.getenv("HF_API_KEY") or os.getenv("HUGGINGFACE_API_KEY") or None,
        hf_api_url=os.getenv("HF_API_URL", "https://api-inference.huggingface.co/models"),
        qdrant_url=os.getenv("QDRANT_URL") or None,
        qdrant_api_key=os.getenv("QDRANT_API_KEY") or None,
        qdrant_path=qdrant_path.resolve(),
        collection_prefix=os.getenv("DEVKIT_COLLECTION_PREFIX", "devkit"),
        embedding_provider=os.getenv("EMBEDDING_PROVIDER", "auto").strip().lower(),
        embedding_model=os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"),
        http_timeout=_env_int("DEVKIT_HTTP_TIMEOUT", 30),
        max_page_chars=_env_int("DEVKIT_MAX_PAGE_CHARS", 8000),
        max_response_chars=_env_int("DEVKIT_MAX_RESPONSE_CHARS", 20000),
        allow_private_urls=_env_flag("DEVKIT_ALLOW_PRIVATE_URLS", False),
        repo_root=repo_root,
    )


def mask(secret: str | None) -> str:
    """Maskuje sekret do bezpiecznego pokazania w logach/resource'ach."""
    if not secret:
        return "-"
    if len(secret) <= 8:
        return "***"
    return f"{secret[:4]}...{secret[-4:]}"


def _package_available(name: str) -> bool:
    from importlib.util import find_spec

    try:
        return find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def capabilities() -> dict[str, dict[str, str]]:
    """Macierz mozliwosci: co dziala teraz, a co wymaga konfiguracji."""
    s = settings()

    def entry(state: str, detail: str, hint: str = "") -> dict[str, str]:
        out = {"state": state, "detail": detail}
        if hint:
            out["hint"] = hint
        return out

    caps: dict[str, dict[str, str]] = {}

    caps["read_page (Jina Reader)"] = (
        entry("ready", f"klucz {mask(s.jina_api_key)} - podniesiony limit")
        if s.jina_api_key
        else entry("ready-degraded", "brak JINA_API_KEY - dziala anonimowo, niski rate limit i cache")
    )

    if s.tavily_api_key:
        caps["web_search"] = entry("ready", f"Tavily ({mask(s.tavily_api_key)})")
    elif s.jina_api_key:
        caps["web_search"] = entry("ready", "Jina Search (s.jina.ai) - brak TAVILY_API_KEY")
    else:
        caps["web_search"] = entry(
            "ready-degraded",
            "fallback DuckDuckGo HTML - brak snippetow wysokiej jakosci",
            "ustaw TAVILY_API_KEY (1000 zapytan/mies. za darmo)",
        )

    caps["delegate / synteza LLM"] = (
        entry("ready", f"Groq: {s.groq_model}")
        if s.groq_api_key
        else entry("disabled", "brak GROQ_API_KEY", "narzedzia zwroca surowy kontekst zamiast syntezy")
    )

    caps["hf_infer"] = (
        entry("ready", f"HF Inference ({mask(s.hf_api_key)})")
        if s.hf_api_key
        else entry("disabled", "brak HF_API_KEY", "opcjonalne: OCR / ASR / modele specjalistyczne")
    )

    if not _package_available("qdrant_client"):
        caps["pamiec wektorowa (Qdrant)"] = entry(
            "missing_package", "brak pakietu qdrant-client", "pip install qdrant-client"
        )
    elif s.qdrant_url:
        caps["pamiec wektorowa (Qdrant)"] = entry("ready", f"Qdrant Cloud: {s.qdrant_url}")
    else:
        caps["pamiec wektorowa (Qdrant)"] = entry("ready", f"tryb lokalny (embedded): {s.qdrant_path}")

    from .embeddings import describe_embedder

    caps["embeddingi"] = describe_embedder()

    return caps
