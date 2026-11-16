#!/usr/bin/env python3
"""Validate local Markdown links and heading fragments without third-party packages."""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^)]+)\)")
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")


def markdown_files() -> list[Path]:
    return [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]


def without_fenced_code(text: str) -> str:
    kept: list[str] = []
    fence_char: str | None = None
    fence_length = 0

    for line in text.splitlines():
        match = FENCE_PATTERN.match(line)
        if match:
            marker = match.group(1)
            if fence_char is None:
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char = None
                fence_length = 0
            continue
        if fence_char is None:
            kept.append(line)

    return "\n".join(kept)


def heading_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_PATTERN.match(line)
        if not match:
            continue

        title = re.sub(r"`([^`]*)`", r"\1", match.group(1)).lower()
        slug_chars: list[str] = []
        for char in title:
            category = unicodedata.category(char)
            if category[0] in {"L", "N"}:
                slug_chars.append(char)
            elif char.isspace() or char == "-":
                slug_chars.append("-")

        slug = re.sub(r"-+", "-", "".join(slug_chars)).strip("-")
        occurrence = counts.get(slug, 0)
        counts[slug] = occurrence + 1
        anchors.add(slug if occurrence == 0 else f"{slug}-{occurrence}")

    return anchors


def validate_link(source: Path, destination: str) -> str | None:
    destination = destination.strip()
    if destination.startswith("<") and destination.endswith(">"):
        destination = destination[1:-1]

    parsed = urlsplit(destination)
    if parsed.scheme or destination.startswith("//"):
        return None

    raw_path = unquote(parsed.path)
    target = (source.parent / raw_path).resolve() if raw_path else source.resolve()
    if not target.exists():
        return f"{source.relative_to(ROOT)}: percorso locale inesistente: {destination}"

    fragment = unquote(parsed.fragment)
    if fragment and target.is_file() and target.suffix.lower() == ".md":
        if fragment not in heading_anchors(target):
            return f"{source.relative_to(ROOT)}: ancora inesistente: {destination}"

    return None


def main() -> int:
    errors: list[str] = []
    files = markdown_files()
    for source in files:
        text = without_fenced_code(source.read_text(encoding="utf-8"))
        for match in LINK_PATTERN.finditer(text):
            destination = match.group(1).strip()
            if destination.startswith("<"):
                destination = destination[1:-1]
            else:
                destination = destination.split(maxsplit=1)[0]
            error = validate_link(source, destination)
            if error:
                errors.append(error)

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"Documentazione valida: link e ancore locali verificati in {len(files)} file Markdown.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
