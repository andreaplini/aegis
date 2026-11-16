#!/usr/bin/env python3
"""Validate generated RAD and SDD DOCX artifacts using the standard library."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
REQUIRED_TEXT = {
    "rad-is.docx": ("Documento di Analisi dei Requisiti", "SOMMARIO", "UC-01"),
    "sdd-is.docx": (
        "System Design Document",
        "SOMMARIO",
        "GLOSSARIO",
        "Sicurezza d'uso e pericoli operativi",
    ),
}
PRODUCT_NAME_PATTERN = re.compile(r"\baegis\b", re.IGNORECASE)


def document_text(path: Path) -> str:
    with zipfile.ZipFile(path) as package:
        invalid_member = package.testzip()
        if invalid_member:
            raise ValueError(f"archivio DOCX danneggiato nel file {invalid_member}")
        document = ElementTree.fromstring(package.read("word/document.xml"))

    paragraphs: list[str] = []
    for paragraph in document.iter(f"{WORD_NAMESPACE}p"):
        paragraphs.append(
            "".join(node.text or "" for node in paragraph.iter(f"{WORD_NAMESPACE}t"))
        )
    return "\n".join(paragraphs)


def validate_document(path: Path, required_text: tuple[str, ...] | None = None) -> list[str]:
    expected = required_text or REQUIRED_TEXT.get(path.name)
    if expected is None:
        return [f"{path}: nome file DOCX non riconosciuto"]
    if not path.is_file():
        return [f"{path}: file DOCX inesistente"]

    try:
        text = document_text(path)
    except (OSError, KeyError, ValueError, zipfile.BadZipFile, ElementTree.ParseError) as error:
        return [f"{path}: DOCX non leggibile: {error}"]

    errors = [f"{path}: testo richiesto mancante: {marker}" for marker in expected if marker not in text]
    if not PRODUCT_NAME_PATTERN.search(text):
        errors.append(f"{path}: nome progetto aegis non trovato")
    if any(match.group(0) != "aegis" for match in PRODUCT_NAME_PATTERN.finditer(text)):
        errors.append(f"{path}: il nome del prodotto deve essere scritto esattamente aegis")
    if chr(0x2014) in text:
        errors.append(f"{path}: usare punteggiatura semplice, senza trattino lungo")
    return errors


def main(argv: list[str]) -> int:
    paths = [Path(value) for value in argv[1:]]
    if len(paths) != 2:
        print("Uso: python3 scripts/validate_docx.py RAD.docx SDD.docx", file=sys.stderr)
        return 2

    errors = [error for path in paths for error in validate_document(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("DOCX validi: archivio, contenuto, nome aegis e punteggiatura verificati.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
