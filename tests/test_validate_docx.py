from __future__ import annotations

import io
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_docx


WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DRAWING_NAMESPACE = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
DRAWING_MAIN_NAMESPACE = "http://schemas.openxmlformats.org/drawingml/2006/main"
DOCUMENT_RELATIONSHIP_NAMESPACE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
ElementTree.register_namespace("w", WORD_NAMESPACE)


def write_docx(
    path: Path,
    text: str,
    story_parts: dict[str, str] | None = None,
    diagram_count: int = 0,
    diagram_descriptions: list[str] | None = None,
    core_metadata: dict[str, str] | None = None,
    include_diagram_images: bool = True,
) -> None:
    document = ElementTree.Element(f"{{{WORD_NAMESPACE}}}document")
    body = ElementTree.SubElement(document, f"{{{WORD_NAMESPACE}}}body")
    for line in text.splitlines():
        paragraph = ElementTree.SubElement(body, f"{{{WORD_NAMESPACE}}}p")
        run = ElementTree.SubElement(paragraph, f"{{{WORD_NAMESPACE}}}r")
        node = ElementTree.SubElement(run, f"{{{WORD_NAMESPACE}}}t")
        node.text = line
    for index in range(diagram_count):
        paragraph = ElementTree.SubElement(body, f"{{{WORD_NAMESPACE}}}p")
        run = ElementTree.SubElement(paragraph, f"{{{WORD_NAMESPACE}}}r")
        drawing = ElementTree.SubElement(run, f"{{{WORD_NAMESPACE}}}drawing")
        inline = ElementTree.SubElement(drawing, f"{{{DRAWING_NAMESPACE}}}inline")
        description = (
            diagram_descriptions[index]
            if diagram_descriptions is not None
            else f"Descrizione diagramma {index + 1}"
        )
        ElementTree.SubElement(
            inline,
            f"{{{DRAWING_NAMESPACE}}}docPr",
            {"id": str(index + 1), "name": f"Diagramma {index + 1}", "descr": description},
        )
        ElementTree.SubElement(
            inline,
            f"{{{DRAWING_MAIN_NAMESPACE}}}blip",
            {f"{{{DOCUMENT_RELATIONSHIP_NAMESPACE}}}embed": f"rIdImage{index + 1}"},
        )

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
        document_relationships = ElementTree.Element(
            "{http://schemas.openxmlformats.org/package/2006/relationships}Relationships"
        )
        for index in range(diagram_count):
            ElementTree.SubElement(
                document_relationships,
                "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship",
                {
                    "Id": f"rIdImage{index + 1}",
                    "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
                    "Target": f"media/image{index + 1}.png",
                },
            )
        package.writestr("[Content_Types].xml", ElementTree.tostring(content_types))
        package.writestr("_rels/.rels", ElementTree.tostring(relationships))
        package.writestr("word/document.xml", ElementTree.tostring(document))
        if diagram_count:
            package.writestr(
                "word/_rels/document.xml.rels",
                ElementTree.tostring(document_relationships),
            )
        if include_diagram_images:
            for index in range(diagram_count):
                package.writestr(f"word/media/image{index + 1}.png", b"test image")
        if core_metadata is not None:
            properties = ElementTree.Element(
                "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}coreProperties"
            )
            metadata_tags = {
                "creator": "{http://purl.org/dc/elements/1.1/}creator",
                "title": "{http://purl.org/dc/elements/1.1/}title",
                "description": "{http://purl.org/dc/elements/1.1/}description",
                "subject": "{http://purl.org/dc/elements/1.1/}subject",
                "lastModifiedBy": (
                    "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"
                    "lastModifiedBy"
                ),
            }
            for name, value in core_metadata.items():
                node = ElementTree.SubElement(properties, metadata_tags[name])
                node.text = value
            package.writestr("docProps/core.xml", ElementTree.tostring(properties))
        for part_name, part_text in (story_parts or {}).items():
            story_kind = Path(part_name).stem.rstrip("0123456789")
            story = ElementTree.Element(f"{{{WORD_NAMESPACE}}}{story_kind}")
            paragraph = ElementTree.SubElement(story, f"{{{WORD_NAMESPACE}}}p")
            run = ElementTree.SubElement(paragraph, f"{{{WORD_NAMESPACE}}}r")
            node = ElementTree.SubElement(run, f"{{{WORD_NAMESPACE}}}t")
            node.text = part_text
            package.writestr(part_name, ElementTree.tostring(story))


class DocxValidationTests(unittest.TestCase):
    def test_cli_requires_reference_template(self) -> None:
        error_output = io.StringIO()
        with redirect_stderr(error_output):
            result = validate_docx.main(["validate_docx.py", "rad.docx", "sdd.docx"])

        self.assertEqual(result, 2)
        self.assertIn("template.docx", error_output.getvalue())

    def test_requires_rendered_diagrams_without_mermaid_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            required = "aegis\nDocumento di Analisi dei Requisiti\nSOMMARIO\nUC-01"
            write_docx(path, required + "\nsequenceDiagram")
            errors = validate_docx.validate_document(path, expected_diagrams=8)
            self.assertTrue(any("codice Mermaid non convertito" in error for error in errors))
            self.assertTrue(any("attesi 8 diagrammi, trovati 0" in error for error in errors))

            write_docx(path, required, diagram_count=8)
            self.assertEqual(validate_docx.validate_document(path, expected_diagrams=8), [])

            write_docx(path, required, diagram_count=8, include_diagram_images=False)
            errors = validate_docx.validate_document(path, expected_diagrams=8)
            self.assertTrue(any("immagine incorporata mancante" in error for error in errors))

            write_docx(path, required, diagram_count=8, diagram_descriptions=[""] * 8)
            errors = validate_docx.validate_document(path, expected_diagrams=8)
            self.assertTrue(any("diagrammi senza descrizione alternativa" in error for error in errors))

    def test_diagram_validation_uses_the_current_markdown_source_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "RAD.md").write_text(
                "```mermaid\nflowchart LR\nA-->B\n```\n"
                "```mermaid\nsequenceDiagram\nA->>B: C\n```\n",
                encoding="utf-8",
            )
            path = root / "rad-is.docx"
            write_docx(
                path,
                "aegis\nDocumento di Analisi dei Requisiti\nSOMMARIO\nUC-01",
                diagram_count=2,
            )

            with patch.object(validate_docx, "ROOT", root):
                self.assertEqual(validate_docx.source_diagram_count("rad-is.docx"), 2)
                self.assertEqual(validate_docx.validate_document(path), [])

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

    def test_checks_header_and_note_text_for_name_and_punctuation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            write_docx(
                path,
                "aegis\nTitolo documento",
                {
                    "word/header1.xml": " ".join(("aegis".capitalize(), "header")),
                    "word/footnotes.xml": "nota" + chr(0x3B) + " finale",
                },
            )
            errors = validate_docx.validate_document(path, ("Titolo documento",))
            self.assertTrue(any("esattamente aegis" in error for error in errors))
            self.assertTrue(any("punto e virgola" in error for error in errors))

    def test_checks_alternative_diagram_descriptions_for_name_and_punctuation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            descriptions = [
                "Aegis " + chr(0x2014) + " descrizione; non conforme",
                *(f"Descrizione diagramma {index}" for index in range(2, 9)),
            ]
            write_docx(
                path,
                "aegis\nDocumento di Analisi dei Requisiti\nSOMMARIO\nUC-01",
                diagram_count=8,
                diagram_descriptions=descriptions,
            )
            errors = validate_docx.validate_document(path, expected_diagrams=8)
            self.assertTrue(any("esattamente aegis" in error for error in errors))
            self.assertTrue(any("trattino lungo" in error for error in errors))
            self.assertTrue(any("punto e virgola" in error for error in errors))

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

    def test_rejects_personal_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            write_docx(
                path,
                "aegis\nTitolo documento",
                core_metadata={"creator": "Autore", "lastModifiedBy": "Revisore"},
            )
            errors = validate_docx.validate_document(path, ("Titolo documento",))
            self.assertTrue(any("metadati personali" in error for error in errors))

    def test_checks_core_property_text_for_name_and_punctuation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rad-is.docx"
            write_docx(
                path,
                "aegis\nTitolo documento",
                core_metadata={"title": "Aegis; documento"},
            )
            errors = validate_docx.validate_document(path, ("Titolo documento",))
            self.assertTrue(any("esattamente aegis" in error for error in errors))
            self.assertTrue(any("punto e virgola" in error for error in errors))

    def test_reference_template_rejects_semicolons_and_stale_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "template.docx"
            extracted = root / "document.xml"
            write_docx(source, "Template; esempio")
            with zipfile.ZipFile(source) as package:
                extracted.write_bytes(package.read("word/document.xml"))

            errors = validate_docx.validate_reference_template(source, extracted)
            self.assertTrue(any("punto e virgola" in error for error in errors))

            write_docx(source, "Template " + chr(0x2014) + " esempio")
            with zipfile.ZipFile(source) as package:
                extracted.write_bytes(package.read("word/document.xml"))
            errors = validate_docx.validate_reference_template(source, extracted)
            self.assertTrue(any("trattino lungo" in error for error in errors))

            write_docx(source, "Template, esempio")
            with zipfile.ZipFile(source) as package:
                extracted.write_bytes(package.read("word/document.xml"))
            self.assertEqual(validate_docx.validate_reference_template(source, extracted), [])

            extracted.write_bytes(extracted.read_bytes() + b" ")
            errors = validate_docx.validate_reference_template(source, extracted)
            self.assertTrue(any("non corrisponde" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
