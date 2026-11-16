#!/usr/bin/env python3
"""Validate generated RAD and SDD DOCX artifacts using the standard library."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DRAWING_NAMESPACE = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
CONTENT_TYPES_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/content-types}"
PACKAGE_RELATIONSHIPS_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/relationships}"
CORE_PROPERTIES_NAMESPACE = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"
DC_NAMESPACE = "{http://purl.org/dc/elements/1.1/}"
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
REQUIRED_DIAGRAM_COUNTS = {"rad-is.docx": 8, "sdd-is.docx": 1}
PRODUCT_NAME_PATTERN = re.compile(r"\baegis\b", re.IGNORECASE)
MERMAID_SOURCE_PATTERN = re.compile(r"(?m)^\s*(?:flowchart\s|graph\s|sequenceDiagram\b|classDiagram\b)")
STORY_PART_PATTERN = re.compile(
    r"^word/(?:document|header\d+|footer\d+|footnotes|endnotes|comments)\.xml$"
)


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

        story_parts = [
            ElementTree.fromstring(package.read(name))
            for name in package.namelist()
            if name != "word/document.xml" and STORY_PART_PATTERN.fullmatch(name)
        ]

    paragraphs: list[str] = []
    for story in (document, *story_parts):
        for paragraph in story.iter(f"{WORD_NAMESPACE}p"):
            paragraphs.append(
                "".join(node.text or "" for node in paragraph.iter(f"{WORD_NAMESPACE}t"))
            )
    return "\n".join(paragraphs)


def document_diagram_count(path: Path) -> int:
    with zipfile.ZipFile(path) as package:
        document = ElementTree.fromstring(package.read("word/document.xml"))
    return sum(1 for _ in document.iter(f"{WORD_NAMESPACE}drawing"))


def document_diagram_descriptions(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as package:
        document = ElementTree.fromstring(package.read("word/document.xml"))
    return [
        node.get("descr", "").strip()
        for node in document.iter(f"{DRAWING_NAMESPACE}docPr")
    ]


def document_personal_metadata(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as package:
        if "docProps/core.xml" not in package.namelist():
            return []
        properties = ElementTree.fromstring(package.read("docProps/core.xml"))

    personal_fields = (
        (f"{DC_NAMESPACE}creator", "autore"),
        (f"{CORE_PROPERTIES_NAMESPACE}lastModifiedBy", "ultimo modificatore"),
    )
    return [
        label
        for tag, label in personal_fields
        if (node := properties.find(tag)) is not None and (node.text or "").strip()
    ]


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
    try:
        personal_metadata = document_personal_metadata(path)
    except (OSError, KeyError, ValueError, zipfile.BadZipFile, ElementTree.ParseError) as error:
        errors.append(f"{path}: impossibile verificare i metadati personali: {error}")
    else:
        if personal_metadata:
            errors.append(
                f"{path}: rimuovere i metadati personali: {', '.join(personal_metadata)}"
            )
    if not PRODUCT_NAME_PATTERN.search(text):
        errors.append(f"{path}: nome progetto aegis non trovato")
    if any(match.group(0) != "aegis" for match in PRODUCT_NAME_PATTERN.finditer(text)):
        errors.append(f"{path}: il nome del prodotto deve essere scritto esattamente aegis")
    if chr(0x2014) in text:
        errors.append(f"{path}: usare punteggiatura semplice, senza trattino lungo")
    if ";" in text:
        errors.append(f"{path}: evitare il punto e virgola nel documento esportato")
    if MERMAID_SOURCE_PATTERN.search(text):
        errors.append(f"{path}: codice Mermaid non convertito in diagramma")
    if required_text is None and path.name in REQUIRED_DIAGRAM_COUNTS:
        try:
            actual_diagrams = document_diagram_count(path)
        except (OSError, KeyError, ValueError, zipfile.BadZipFile, ElementTree.ParseError) as error:
            errors.append(f"{path}: impossibile contare i diagrammi DOCX: {error}")
        else:
            expected_diagrams = REQUIRED_DIAGRAM_COUNTS[path.name]
            if actual_diagrams != expected_diagrams:
                errors.append(
                    f"{path}: attesi {expected_diagrams} diagrammi, trovati {actual_diagrams}"
                )
            try:
                descriptions = document_diagram_descriptions(path)
            except (OSError, KeyError, ValueError, zipfile.BadZipFile, ElementTree.ParseError) as error:
                errors.append(f"{path}: impossibile leggere le descrizioni dei diagrammi: {error}")
            else:
                if len(descriptions) != actual_diagrams:
                    errors.append(
                        f"{path}: {len(descriptions)} descrizioni alternative per "
                        f"{actual_diagrams} diagrammi"
                    )
                missing_descriptions = sum(not description for description in descriptions)
                if missing_descriptions:
                    errors.append(
                        f"{path}: {missing_descriptions} diagrammi senza descrizione alternativa"
                    )
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

    print("DOCX validi: archivio, contenuto, nome aegis, punteggiatura e diagrammi verificati.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
