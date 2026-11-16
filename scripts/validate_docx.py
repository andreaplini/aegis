#!/usr/bin/env python3
"""Validate generated RAD and SDD DOCX artifacts using the standard library."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CONTENT_TYPES_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/content-types}"
PACKAGE_RELATIONSHIPS_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/relationships}"
OFFICE_DOCUMENT_RELATIONSHIP = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
DOCUMENT_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
REQUIRED_PARTS = {"[Content_Types].xml", "_rels/.rels", "word/document.xml"}
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
        missing_parts = REQUIRED_PARTS - set(package.namelist())
        if missing_parts:
            raise ValueError(f"parti DOCX mancanti: {', '.join(sorted(missing_parts))}")

        content_types = ElementTree.fromstring(package.read("[Content_Types].xml"))
        if content_types.tag != f"{CONTENT_TYPES_NAMESPACE}Types":
            raise ValueError("elenco dei tipi di contenuto non valido")
        main_content = content_types.find(
            f"{CONTENT_TYPES_NAMESPACE}Override[@PartName='/word/document.xml']"
        )
        if main_content is None or main_content.get("ContentType") != DOCUMENT_CONTENT_TYPE:
            raise ValueError("tipo del documento principale non valido")

        relationships = ElementTree.fromstring(package.read("_rels/.rels"))
        if relationships.tag != f"{PACKAGE_RELATIONSHIPS_NAMESPACE}Relationships":
            raise ValueError("relazioni del pacchetto non valide")
        document_relationship = relationships.find(
            f"{PACKAGE_RELATIONSHIPS_NAMESPACE}Relationship[@Type='{OFFICE_DOCUMENT_RELATIONSHIP}']"
        )
        if document_relationship is None or document_relationship.get("Target") != "word/document.xml":
            raise ValueError("relazione al documento principale non valida")

        document = ElementTree.fromstring(package.read("word/document.xml"))
        if document.tag != f"{WORD_NAMESPACE}document" or document.find(f"{WORD_NAMESPACE}body") is None:
            raise ValueError("struttura del documento principale non valida")

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
    if ";" in text:
        errors.append(f"{path}: evitare il punto e virgola nel documento esportato")
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
