from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_docs


VALID_RAD = """# RAD

### 3.2 REQUISITI FUNZIONALI

| ID | Azione | Caso |
|---|---|---|
| FR-01 | Consultare un luogo | UC-01 |
| NFR-01 | Accessibilità | Usare i flussi con screen reader |

###### UC-01: Consultare un luogo

| Attori partecipanti | Viaggiatore, sistema |
| Condizioni d’ingresso | Luogo selezionato |
| Condizioni d’uscita | Dettaglio mostrato |
| Requisiti qualitativi | Informazioni accessibili |
| Flusso degli eventi | Il sistema recupera e mostra il luogo |
"""

VALID_SDD = """# SDD

### 3.2 DECOMPOSIZIONE DEL SISTEMA

| Modulo | Requisiti |
|---|---|
| Places | FR-01, UC-01, NFR-01 |

#### 3.2.1 DIAGRAMMA DEI MODULI
"""


class MarkdownValidationTests(unittest.TestCase):
    def test_non_functional_requirements_have_action_and_verification_criterion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            rad = docs / "RAD.md"
            rad.write_text(
                "### 3.3 REQUISITI NON FUNZIONALI\n"
                "| ID | Qualità | Azione richiesta | Criterio di verifica |\n"
                "|---|---|---|---|\n"
                "| NFR-01 | Accessibilità | Usare la tastiera | Verificare il flusso |\n"
                "### 3.4 VINCOLI\n",
                encoding="utf-8",
            )

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_non_functional_requirements(), [])
                rad.write_text(
                    rad.read_text(encoding="utf-8").replace("| Verificare il flusso |", "|  |"),
                    encoding="utf-8",
                )
                errors = validate_docs.validate_non_functional_requirements()
                self.assertTrue(any("criterio di verifica" in error for error in errors))

    def test_fenced_code_is_ignored_when_scanning_links(self) -> None:
        text = """[valid](docs.md)
```md
[example](missing.md)
```
"""
        result = validate_docs.without_fenced_code(text)
        self.assertIn("[valid](docs.md)", result)
        self.assertNotIn("missing.md", result)

    def test_unicode_and_duplicate_heading_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "headings.md"
            document.write_text("# Accessibilità\n# Accessibilità\n", encoding="utf-8")
            self.assertEqual(
                validate_docs.heading_anchors(document),
                {"accessibilità", "accessibilità-1"},
            )

    def test_local_path_and_anchor_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            source = docs / "source.md"
            target = docs / "target.md"
            source.write_text("# Source\n", encoding="utf-8")
            target.write_text("# Destinazione\n", encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertIsNone(validate_docs.validate_link(source, "target.md#destinazione"))
                self.assertIn("inesistente", validate_docs.validate_link(source, "missing.md"))
                self.assertIn("ancora inesistente", validate_docs.validate_link(source, "target.md#missing"))

    def test_all_requirement_and_case_ids_map_to_a_module(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "RAD.md").write_text(VALID_RAD, encoding="utf-8")
            (docs / "SDD.md").write_text(VALID_SDD, encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_traceability(), [])
                sdd = docs / "SDD.md"
                sdd.write_text(VALID_SDD.replace(", NFR-01", ""), encoding="utf-8")
                self.assertIn("NFR-01", validate_docs.validate_traceability()[0])

    def test_use_case_fields_and_requirement_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            rad = docs / "RAD.md"
            rad.write_text(VALID_RAD, encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_use_case_specs(), [])
                rad.write_text(VALID_RAD.replace("| Condizioni d’uscita | Dettaglio mostrato |\n", ""), encoding="utf-8")
                errors = validate_docs.validate_use_case_specs()
                self.assertTrue(any("condizioni d’uscita" in error for error in errors))

    def test_functional_requirement_cannot_reference_missing_case(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            rad = docs / "RAD.md"
            rad.write_text(VALID_RAD.replace("UC-01 |\n", "UC-02 |\n"), encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                errors = validate_docs.validate_use_case_specs()
                self.assertTrue(any("UC-02" in error for error in errors))

    def test_project_name_and_punctuation_are_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            skill = root / ".agents/skills/sample"
            docs.mkdir()
            skill.mkdir(parents=True)
            (root / "README.md").write_text("# aegis\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("## Skill aegis\n", encoding="utf-8")
            (skill / "SKILL.md").write_text("# aegis\n", encoding="utf-8")
            for name in ("RAD.md", "SDD.md"):
                (docs / name).write_text("| Progetto | aegis |\n", encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_project_style(), [])

                readme = root / "README.md"
                readme.write_text("# " + chr(65) + "egis\n", encoding="utf-8")
                errors = validate_docs.validate_project_style()
                self.assertTrue(any("README.md" in error for error in errors))

                readme.write_text("# aegis " + chr(0x2014) + " piattaforma\n", encoding="utf-8")
                errors = validate_docs.validate_project_style()
                self.assertTrue(any("trattino lungo" in error for error in errors))

                readme.write_text("# aegis\n", encoding="utf-8")
                (docs / "SDD.md").write_text("| Progetto | aegis mobility |\n", encoding="utf-8")
                errors = validate_docs.validate_project_style()
                self.assertTrue(any("campo Progetto" in error for error in errors))

    def test_numbered_document_structure_matches_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            templates = docs / "template"
            templates.mkdir(parents=True)
            for name in ("RAD.md", "SDD.md"):
                (docs / name).write_text("## Introduzione\n### 1.1 Scopo\n### 3.1 Sistema\n", encoding="utf-8")
                (templates / name).write_text("## Introduzione\n### 1.1 Scopo\n### 3.1 Sistema\n", encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_document_structure(), [])
                path = docs / "SDD.md"
                path.write_text(path.read_text(encoding="utf-8").replace("3.1", "3.2"), encoding="utf-8")
                errors = validate_docs.validate_document_structure()
                self.assertEqual(len(errors), 1)
                self.assertIn("SDD.md", errors[0])
                path.write_text(path.read_text(encoding="utf-8").replace("### 3.2", "#### 3.1"), encoding="utf-8")
                errors = validate_docs.validate_document_structure()
                self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
