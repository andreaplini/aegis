from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_docx


WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ElementTree.register_namespace("w", WORD_NAMESPACE)


def write_docx(path: Path, text: str) -> None:
    document = ElementTree.Element(f"{{{WORD_NAMESPACE}}}document")
    body = ElementTree.SubElement(document, f"{{{WORD_NAMESPACE}}}body")
    for line in text.splitlines():
        paragraph = ElementTree.SubElement(body, f"{{{WORD_NAMESPACE}}}p")
        run = ElementTree.SubElement(paragraph, f"{{{WORD_NAMESPACE}}}r")
        node = ElementTree.SubElement(run, f"{{{WORD_NAMESPACE}}}t")
        node.text = line

    with zipfile.ZipFile(path, "w") as package:
        content_types = ElementTree.Element(
            "{http://schemas.openxmlformats.org/package/2006/content-types}Types"
        )
        ElementTree.SubElement(
            content_types,
            "{http://schemas.openxmlformats.org/package/2006/content-types}Override",
            {
                "PartName": "/word/document.xml",
                "ContentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml",
            },
        )
        relationships = ElementTree.Element(
            "{http://schemas.openxmlformats.org/package/2006/relationships}Relationships"
        )
        ElementTree.SubElement(
            relationships,
            "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship",
            {
                "Id": "rId1",
                "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument",
                "Target": "word/document.xml",
            },
        )
        package.writestr("[Content_Types].xml", ElementTree.tostring(content_types))
        package.writestr("_rels/.rels", ElementTree.tostring(relationships))
        package.writestr("word/document.xml", ElementTree.tostring(document))


class DocxValidationTests(unittest.TestCase):
    def test_valid_archive_and_required_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            write_docx(path, "aegis\nTitolo documento\nCaso d'uso")
            self.assertEqual(
                validate_docx.validate_document(path, ("Titolo documento", "Caso d'uso")),
                [],
            )

    def test_rejects_corrupt_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            path.write_text("not a DOCX", encoding="utf-8")
            errors = validate_docx.validate_document(path, ("Titolo",))
            self.assertTrue(any("DOCX non leggibile" in error for error in errors))

    def test_rejects_zip_without_required_docx_parts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            with zipfile.ZipFile(path, "w") as package:
                package.writestr("word/document.xml", "<document />")
            errors = validate_docx.validate_document(path, ("Titolo",))
            self.assertTrue(any("parti DOCX mancanti" in error for error in errors))

    def test_rejects_wrong_project_name_and_long_dash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sdd-is.docx"
            invalid_title = " ".join(("aegis".capitalize(), chr(0x2014), "architettura"))
            write_docx(path, invalid_title + "\nTitolo documento")
            errors = validate_docx.validate_document(path, ("Titolo documento",))
            self.assertTrue(any("esattamente aegis" in error for error in errors))
            self.assertTrue(any("trattino lungo" in error for error in errors))

    def test_rejects_semicolon_punctuation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            write_docx(path, "aegis\nTitolo documento; con punteggiatura non ammessa")
            errors = validate_docx.validate_document(path, ("Titolo documento",))
            self.assertTrue(any("punto e virgola" in error for error in errors))

    def test_rejects_missing_required_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            write_docx(path, "aegis\nSOMMARIO")
            errors = validate_docx.validate_document(path, ("GLOSSARIO",))
            self.assertTrue(any("GLOSSARIO" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
