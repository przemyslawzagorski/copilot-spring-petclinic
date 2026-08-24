"""Wiedza o repozytorium: profil projektu + bezpieczne przechodzenie po plikach.

To jest ta czesc, ktora sprawia, ze serwer jest **uzyteczny w pracy programisty**,
a nie tylko efektowny: agent dostaje wersje i mape modulow jako resource
(zero tokenow na zgadywanie) oraz moze zaindeksowac repo do wlasnego RAG-a.
"""

from __future__ import annotations

import logging
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterator

from .config import settings
from .http import DevKitError

log = logging.getLogger("devkit.repo")

SKIP_DIRS = {
    ".git", ".venv", "venv", "node_modules", "target", "build", "dist", "__pycache__",
    ".gradle", ".idea", ".mvn", "site", ".qdrant_local", ".pytest_cache", "bin", "obj",
}
TEXT_SUFFIXES = {
    ".java", ".kt", ".py", ".md", ".txt", ".xml", ".yml", ".yaml", ".json", ".properties",
    ".sql", ".html", ".css", ".js", ".ts", ".sh", ".ps1", ".gradle", ".cfg", ".toml", ".http",
}
MAX_FILE_BYTES = 400_000
MAVEN_NS = {"m": "http://maven.apache.org/POM/4.0.0"}


def safe_path(raw: str) -> Path:
    """Zamienia sciezke uzytkownika na absolutna i pilnuje, by nie wyszla poza repo."""
    root = settings().repo_root
    candidate = Path(raw)
    resolved = (candidate if candidate.is_absolute() else root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise DevKitError(
            f"Sciezka '{raw}' wychodzi poza katalog projektu ({root}). Indeksowanie jest ograniczone do repo."
        ) from exc
    return resolved


def iter_files(patterns: list[str], *, max_files: int = 200) -> Iterator[Path]:
    """Zwraca pliki tekstowe pasujace do wzorcow glob, z pominieciem smieci build."""
    root = settings().repo_root
    seen: set[Path] = set()
    count = 0
    for pattern in patterns:
        for path in sorted(root.glob(pattern.strip())):
            if count >= max_files:
                return
            if not path.is_file() or path in seen:
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if path.stat().st_size > MAX_FILE_BYTES:
                log.info("Pomijam duzy plik: %s", path)
                continue
            seen.add(path)
            count += 1
            yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(settings().repo_root).as_posix()
    except ValueError:
        return str(path)


def _pom_profile(pom: Path) -> dict[str, Any]:
    try:
        tree = ET.parse(pom)
    except ET.ParseError as exc:  # pragma: no cover
        return {"error": f"pom.xml nie parsuje sie: {exc}"}
    root = tree.getroot()

    def find(path: str) -> str | None:
        node = root.find(path, MAVEN_NS)
        return node.text.strip() if node is not None and node.text else None

    properties = {}
    props_node = root.find("m:properties", MAVEN_NS)
    if props_node is not None:
        for child in props_node:
            tag = child.tag.split("}")[-1]
            properties[tag] = (child.text or "").strip()

    dependencies = []
    for dep in root.findall(".//m:dependencies/m:dependency", MAVEN_NS):
        group = dep.find("m:groupId", MAVEN_NS)
        artifact = dep.find("m:artifactId", MAVEN_NS)
        if artifact is not None:
            dependencies.append(f"{group.text if group is not None else '?'}:{artifact.text}")

    return {
        "artifact": find("m:artifactId"),
        "version": find("m:version"),
        "name": find("m:name"),
        "parent": {
            "artifact": find("m:parent/m:artifactId"),
            "version": find("m:parent/m:version"),
        },
        "java_version": properties.get("java.version") or properties.get("maven.compiler.release"),
        "properties": properties,
        "dependency_count": len(dependencies),
        "dependencies": sorted(set(dependencies))[:60],
    }


def _git_info(root: Path) -> dict[str, Any]:
    def run(*args: str) -> str:
        try:
            return subprocess.run(
                ["git", *args], cwd=root, capture_output=True, text=True, timeout=5, check=False
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):  # pragma: no cover
            return ""

    # `-uno` pomija skanowanie plikow niesledzonych - w repo z .venv i target
    # samo `git status --porcelain` potrafi trwac kilkanascie sekund.
    return {
        "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
        "last_commits": [line for line in run("log", "-5", "--pretty=%h %s").splitlines() if line],
        "modified_tracked_files": len(
            [line for line in run("status", "--porcelain", "-uno").splitlines() if line]
        ),
    }


def _java_packages(root: Path, limit: int = 40) -> list[dict[str, Any]]:
    base = root / "src" / "main" / "java"
    if not base.exists():
        return []
    packages: dict[str, int] = {}
    for path in base.rglob("*.java"):
        package = path.parent.relative_to(base).as_posix().replace("/", ".")
        packages[package] = packages.get(package, 0) + 1
    return [
        {"package": package, "classes": count}
        for package, count in sorted(packages.items(), key=lambda item: -item[1])[:limit]
    ]


def profile() -> dict[str, Any]:
    """Zwiezly profil projektu: stack, wersje, mapa pakietow, stan gita."""
    root = settings().repo_root
    data: dict[str, Any] = {"root": str(root), "name": root.name}

    pom = root / "pom.xml"
    if pom.exists():
        data["build"] = "maven"
        data["maven"] = _pom_profile(pom)
        spring_parent = data["maven"].get("parent", {})
        if spring_parent.get("artifact") == "spring-boot-starter-parent":
            data["spring_boot_version"] = spring_parent.get("version")
    gradle = root / "build.gradle"
    if gradle.exists():
        data["build"] = "maven+gradle" if pom.exists() else "gradle"
        text = read_text(gradle)
        match = re.search(r"id\s+['\"]org\.springframework\.boot['\"]\s+version\s+['\"]([^'\"]+)", text)
        if match:
            data.setdefault("spring_boot_version", match.group(1))

    data["java_packages"] = _java_packages(root)
    data["counts"] = {
        "main_java": sum(1 for _ in (root / "src" / "main" / "java").rglob("*.java"))
        if (root / "src" / "main" / "java").exists()
        else 0,
        "test_java": sum(1 for _ in (root / "src" / "test" / "java").rglob("*.java"))
        if (root / "src" / "test" / "java").exists()
        else 0,
    }
    data["infra"] = {
        marker: (root / marker).exists()
        for marker in ("docker-compose.yml", "k8s", "Dockerfile", ".github/workflows", "mkdocs.yml")
    }
    data["git"] = _git_info(root)
    return data
