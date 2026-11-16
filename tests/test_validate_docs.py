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

| ID | Responsabile dell’azione | Azione richiesta | Priorità | Caso d’uso |
|---|---|---|---|---|
| FR-01 | Sistema | Consultare un luogo. | Must | UC-01 |

### 3.3 REQUISITI NON FUNZIONALI

| ID | Qualità | Azione richiesta | Criterio di verifica | Responsabile dell’accettazione |
|---|---|---|---|---|
| NFR-01 | Accessibilità | Usare i flussi con screen reader. | Verificare i flussi accessibili. | Referente accessibilità, da designare |

### 3.4 VINCOLI

###### UC-01: Consultare un luogo

| Attori partecipanti | Viaggiatore, sistema |
| Condizioni d’ingresso | Luogo selezionato |
| Condizioni d’uscita | Dettaglio mostrato |
| Requisiti qualitativi | Informazioni accessibili |
| Flusso degli eventi | Il sistema recupera e mostra il luogo |
"""

VALID_SDD = """# SDD

### 3.2 DECOMPOSIZIONE DEL SISTEMA

| Modulo | Responsabilità | Requisiti funzionali e casi d’uso | Requisiti di qualità |
|---|---|---|---|
| Places | Gestire i luoghi. | FR-01, UC-01 | NFR-01 |

#### 3.2.1 DIAGRAMMA DEI MODULI
"""

VALID_USE_CASE_DIAGRAM = """##### Diagramma globale

```mermaid
flowchart TB
  subgraph ACTORS[Attori]
    V[Viaggiatore]
  end
  subgraph SYSTEM[aegis]
    UC01((UC-01 Pianificare un viaggio))
  end
  V --- UC01
```
"""

VALID_ADR = """# ADR-0001: Baseline

## Metadati

| Campo | Valore |
|---|---|
| ID | ADR-0001 |
| Titolo | Baseline |
| Stato | Proposto |
| Data | 16 novembre 2026 |
| Responsabile | Da designare |
| Revisori | Da designare |
| Requisiti correlati | OPEN-08 |

## Contesto e problema
Contesto.

## Driver decisionali
Driver.

## Opzioni considerate
| Opzione | Vantaggi | Costi e rischi | Requisiti soddisfatti o non soddisfatti |
|---|---|---|---|
| A | Vantaggio | Rischio | Requisito |
| B | Vantaggio | Rischio | Requisito |

## Decisione
Non approvata.

## Verifica e revisione
| Evidenza richiesta | Criterio di accettazione | Responsabile | Esito e riferimento |
|---|---|---|---|
| Revisione | Approvazione | Da designare | In attesa |
"""


class MarkdownValidationTests(unittest.TestCase):
    def test_runbook_requires_complete_revision_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            template_directory = root / "docs/template"
            template_directory.mkdir(parents=True)
            runbook = template_directory / "RUNBOOK.md"
            content = (
                "# Runbook\n\n"
                "## Registro delle revisioni\n\n"
                "| Versione | Data | Modifica e motivazione | Autore | Revisore e approvazione |\n"
                "|---|---|---|---|---|\n"
                "| 1.0 | Da compilare | Da descrivere | Da designare | Da registrare |\n\n"
                "## Scopo e impatto\n"
            )
            runbook.write_text(content, encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_runbook_revision_history(), [])
                runbook.write_text(
                    content.replace("| Da registrare |", "|  |"),
                    encoding="utf-8",
                )
                errors = validate_docs.validate_runbook_revision_history()
                self.assertTrue(any("riga 1 del registro revisioni incompleta" in error for error in errors))

    def test_glossaries_require_complete_unique_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            valid = (
                "# Documento\n\n"
                "## GLOSSARIO\n\n"
                "| Termine | Definizione |\n"
                "|---|---|\n"
                "| Cache | Memoria temporanea di lettura. |\n"
                "| Worker | Processo asincrono. |\n"
            )
            for document in ("RAD.md", "SDD.md"):
                (docs / document).write_text(valid, encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_glossaries(), [])
                sdd = docs / "SDD.md"
                sdd.write_text(
                    valid.replace("| Worker | Processo asincrono. |\n", "| Cache | Definizione alternativa. |\n"),
                    encoding="utf-8",
                )
                errors = validate_docs.validate_glossaries()
                self.assertTrue(any("termini duplicati nel glossario" in error for error in errors))

                sdd.write_text(
                    valid.replace("| Worker | Processo asincrono. |\n", "| Cache | |\n"),
                    encoding="utf-8",
                )
                errors = validate_docs.validate_glossaries()
                self.assertTrue(any("voce 2 del glossario incompleta" in error for error in errors))

                sdd.write_text(valid.replace("## GLOSSARIO\n", "## DEFINIZIONI\n"), encoding="utf-8")
                errors = validate_docs.validate_glossaries()
                self.assertTrue(any("deve contenere un solo glossario" in error for error in errors))

    def test_adrs_require_traceable_metadata_options_and_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adr_directory = root / "docs/adr"
            adr_directory.mkdir(parents=True)
            adr = adr_directory / "ADR-0001.md"
            adr.write_text(VALID_ADR, encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_adrs(), [])
                adr.write_text(
                    VALID_ADR.replace("| ID | ADR-0001 |", "| ID | ADR-0002 |")
                    .replace("| Stato | Proposto |", "| Stato | Approvato |")
                    .replace("| Titolo | Baseline |", "| Titolo | |")
                    .replace("| A | Vantaggio | Rischio | Requisito |", "| A | | Rischio | Requisito |")
                    .replace("| B | Vantaggio | Rischio | Requisito |\n", ""),
                    encoding="utf-8",
                )
                errors = validate_docs.validate_adrs()
                self.assertTrue(any("diverso dal nome file" in error for error in errors))
                self.assertTrue(any("stato non valido" in error for error in errors))
                self.assertTrue(any("righe insufficienti" in error for error in errors))
                self.assertTrue(any("metadati mancanti o vuoti" in error for error in errors))
                self.assertTrue(any("riga 1 incompleta" in error for error in errors))

    def test_roadmap_ids_are_unique_and_references_are_declared(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            milestones = docs / "MILESTONES.md"
            milestones.write_text(
                "## Roadmap\n"
                "| DOC-01 | Documentazione |\n"
                "## Applicazione degli sprint\n"
                "| DOC-01 | Documentazione completata |\n"
                "## Decisioni documentali ancora aperte\n"
                "| OPEN-01 | Decisione |\n"
                "## Criterio di completamento della roadmap\n"
                "## Milestone di ingegneria del prodotto\n"
                "| ENG-01 | Implementazione | OPEN-01 |\n"
                "## Regole di avanzamento\n",
                encoding="utf-8",
            )

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_roadmap_ids(), [])
                milestones.write_text(
                    "## Roadmap\n"
                    "| DOC-01 | Documentazione |\n"
                    "## Applicazione degli sprint\n"
                    "| DOC-01 | Documentazione completata |\n"
                    "## Decisioni documentali ancora aperte\n"
                    "| OPEN-01 | Decisione |\n"
                    "| OPEN-01 | Duplicato |\n"
                    "## Criterio di completamento della roadmap\n"
                    "## Milestone di ingegneria del prodotto\n"
                    "| ENG-01 | Implementazione | OPEN-02 |\n"
                    "## Regole di avanzamento\n",
                    encoding="utf-8",
                )
                errors = validate_docs.validate_roadmap_ids()
                self.assertTrue(any("ID milestone duplicati: OPEN-01" in error for error in errors))
                self.assertTrue(any("ID milestone non dichiarati: OPEN-02" in error for error in errors))

    def test_local_google_docs_registry_is_not_project_documentation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            registry = root / "docs/GOOGLE_DOCS_SYNC.md"
            registry.write_text("# Link privati\n", encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertNotIn(registry, validate_docs.markdown_files())

    def test_mermaid_diagrams_require_accessible_descriptions(self) -> None:
        valid = "```mermaid\nflowchart LR\n  accDescr: Diagramma accessibile.\n  A-->B\n```\n"
        invalid = "```mermaid\nflowchart LR\n  A-->B\n```\n"
        self.assertEqual(validate_docs.mermaid_description_errors("docs/RAD.md", valid), [])
        errors = validate_docs.mermaid_description_errors("docs/RAD.md", invalid)
        self.assertTrue(any("senza descrizione accessibile" in error for error in errors))

    def test_mermaid_description_check_includes_templates_and_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs/template").mkdir(parents=True)
            (root / ".agents/skills/example").mkdir(parents=True)
            (root / "README.md").write_text("# aegis\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("## Skill aegis\n", encoding="utf-8")
            (root / ".agents/skills/example/SKILL.md").write_text("# Skill\n", encoding="utf-8")
            template = root / "docs/template/RAD.md"
            template.write_text("```mermaid\nflowchart LR\n  A-->B\n```\n", encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                errors = validate_docs.validate_mermaid_descriptions()
                self.assertTrue(any("docs/template/RAD.md" in error for error in errors))
                template.write_text(
                    "```mermaid\nflowchart LR\n  accDescr: Diagramma accessibile.\n  A-->B\n```\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_docs.validate_mermaid_descriptions(), [])

    def test_functional_requirements_have_complete_unique_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            rad = docs / "RAD.md"
            valid = (
                "### 3.2 REQUISITI FUNZIONALI\n"
                "| ID | Responsabile dell’azione | Azione richiesta | Priorità | Caso d’uso |\n"
                "|---|---|---|---|---|\n"
                "| FR-01 | Sistema | Mostrare i luoghi richiesti. | Must | UC-01 |\n"
                "### 3.3 REQUISITI NON FUNZIONALI\n"
            )
            rad.write_text(valid, encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_functional_requirements(), [])

                invalid = valid.replace(
                    "### 3.3 REQUISITI NON FUNZIONALI\n",
                    "| FR-02 |  | Descrivere il luogo. | Urgent | UC-X |\n"
                    "| FR-01 | Sistema | Mostrare i luoghi richiesti. | Must | UC-01 |\n"
                    "### 3.3 REQUISITI NON FUNZIONALI\n",
                )
                rad.write_text(invalid, encoding="utf-8")
                errors = validate_docs.validate_functional_requirements()
                self.assertTrue(any("responsabile, azione, priorità e caso d’uso" in error for error in errors))
                self.assertTrue(any("priorità non valida" in error for error in errors))
                self.assertTrue(any("senza caso d’uso valido" in error for error in errors))
                self.assertTrue(any("duplicati" in error for error in errors))

    def test_non_functional_requirements_have_action_criterion_and_acceptance_owner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            rad = docs / "RAD.md"
            rad.write_text(
                "### 3.3 REQUISITI NON FUNZIONALI\n"
                "| ID | Qualità | Azione richiesta | Criterio di verifica | Responsabile dell’accettazione |\n"
                "|---|---|---|---|---|\n"
                "| NFR-01 | Accessibilità | Usare la tastiera | Verificare il flusso | Referente accessibilità |\n"
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
                rad.write_text(
                    rad.read_text(encoding="utf-8").replace("| Referente accessibilità |", "|  |"),
                    encoding="utf-8",
                )
                errors = validate_docs.validate_non_functional_requirements()
                self.assertTrue(any("responsabile dell’accettazione" in error for error in errors))

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

    def test_external_links_require_valid_https_without_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            source = docs / "source.md"
            source.write_text("# Source\n", encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertIsNone(validate_docs.validate_link(source, "https://example.org/path"))
                for destination in (
                    "http://example.org/path",
                    "javascript:alert(1)",
                    "//example.org/path",
                    "https://user:password@example.org/path",
                    "https://example.org:invalid/path",
                    "https:///path",
                ):
                    with self.subTest(destination=destination):
                        self.assertIn("URL HTTPS", validate_docs.validate_link(source, destination))

    def test_module_traceability_rejects_missing_unknown_and_mismatched_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "RAD.md").write_text(VALID_RAD, encoding="utf-8")
            (docs / "SDD.md").write_text(VALID_SDD, encoding="utf-8")

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_traceability(), [])
                sdd = docs / "SDD.md"
                sdd.write_text(VALID_SDD.replace("| NFR-01 |", "|  |"), encoding="utf-8")
                self.assertIn("NFR-01", validate_docs.validate_traceability()[0])

                sdd.write_text(VALID_SDD.replace("NFR-01", "NFR-99"), encoding="utf-8")
                errors = validate_docs.validate_traceability()
                self.assertTrue(any("non presenti nel RAD: NFR-99" in error for error in errors))

                rad = docs / "RAD.md"
                two_requirements = VALID_RAD.replace(
                    "### 3.3 REQUISITI NON FUNZIONALI",
                    "| FR-02 | Sistema | Pianificare un viaggio. | Must | UC-02 |\n"
                    "### 3.3 REQUISITI NON FUNZIONALI",
                )
                rad.write_text(two_requirements, encoding="utf-8")
                mismatched_modules = VALID_SDD.replace(
                    "FR-01, UC-01",
                    "FR-01, UC-02",
                ).replace(
                    "#### 3.2.1 DIAGRAMMA DEI MODULI",
                    "| Routing | Pianificare i viaggi. | FR-02, UC-01 | NFR-01 |\n\n"
                    "#### 3.2.1 DIAGRAMMA DEI MODULI",
                )
                sdd.write_text(mismatched_modules, encoding="utf-8")
                errors = validate_docs.validate_traceability()
                self.assertTrue(any("FR-01 non è collegato" in error for error in errors))
                self.assertTrue(any("FR-02 non è collegato" in error for error in errors))

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

    def test_use_case_diagram_covers_defined_cases_and_actor_associations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            rad = docs / "RAD.md"

            def write_rad(diagram: str = VALID_USE_CASE_DIAGRAM) -> None:
                rad.write_text(
                    VALID_RAD.replace(
                        "### 3.2 REQUISITI FUNZIONALI",
                        diagram + "\n### 3.2 REQUISITI FUNZIONALI",
                    ),
                    encoding="utf-8",
                )

            write_rad()

            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.validate_use_case_diagram(), [])
                write_rad(VALID_USE_CASE_DIAGRAM.replace("V --- UC01\n", ""))
                errors = validate_docs.validate_use_case_diagram()
                self.assertTrue(any("non è collegato ad alcun attore" in error for error in errors))

                write_rad(
                    VALID_USE_CASE_DIAGRAM.replace(
                        "UC-01 Pianificare",
                        "UC-02 Pianificare",
                    )
                )
                errors = validate_docs.validate_use_case_diagram()
                self.assertTrue(any("casi d’uso assenti dal diagramma" in error for error in errors))
                self.assertTrue(any("ID del diagramma senza specifica" in error for error in errors))

                write_rad(VALID_USE_CASE_DIAGRAM.replace("Viaggiatore", "Viandante"))
                errors = validate_docs.validate_use_case_diagram()
                self.assertTrue(any("attore partecipante non rappresentato" in error for error in errors))

                write_rad(VALID_USE_CASE_DIAGRAM.replace("V --- UC01", "V --- UC01\n  V --- UC99"))
                errors = validate_docs.validate_use_case_diagram()
                self.assertTrue(any("verso caso non dichiarato UC-99" in error for error in errors))

                duplicate_diagram = VALID_USE_CASE_DIAGRAM.replace(
                    "  end\n  V --- UC01",
                    "    UC02((UC-01 Duplicato))\n  end\n  V --- UC01",
                )
                write_rad(duplicate_diagram)
                errors = validate_docs.validate_use_case_diagram()
                self.assertTrue(any("ID ripetuti nel diagramma" in error for error in errors))

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
                readme.write_text("# aegis; prodotto\n", encoding="utf-8")
                errors = validate_docs.validate_project_style()
                self.assertTrue(any("punto e virgola" in error for error in errors))

                readme.write_text("# aegis\n", encoding="utf-8")
                agents = root / "AGENTS.md"
                agents.write_text("## aegis; regole\n", encoding="utf-8")
                errors = validate_docs.validate_project_style()
                self.assertTrue(any("AGENTS.md" in error and "punto e virgola" in error for error in errors))
                agents.write_text("## Skill aegis\n", encoding="utf-8")

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
