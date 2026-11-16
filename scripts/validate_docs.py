#!/usr/bin/env python3
"""Validate local Markdown links and heading fragments without third-party packages."""

from __future__ import annotations

import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^)]+)\)")
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")
TRACE_ID_PATTERN = re.compile(r"\b(?:FR|NFR|UC)-\d{2}\b")
USE_CASE_HEADING_PATTERN = re.compile(r"^######\s+(UC-\d{2})\b")
USE_CASE_DIAGRAM_NODE_PATTERN = re.compile(
    r"^\s*(UC(\d{2}))\(\(UC-(\d{2})\b",
    re.MULTILINE,
)
USE_CASE_DIAGRAM_ACTOR_PATTERN = re.compile(
    r"^\s*([A-Z][A-Z0-9_]*)\[([^\]]+)\]\s*$",
    re.MULTILINE,
)
USE_CASE_DIAGRAM_EDGE_PATTERN = re.compile(
    r"^\s*([A-Z][A-Z0-9_]*)\s*---\s*(UC\d{2})\s*$",
    re.MULTILINE,
)
FUNCTIONAL_REQUIREMENT_ROW_PATTERN = re.compile(r"^\|\s*(FR-\d{2})\s*\|")
NON_FUNCTIONAL_REQUIREMENT_ROW_PATTERN = re.compile(r"^\|\s*(NFR-\d{2})\s*\|")
CASE_FIELD_PATTERN = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
NUMBERED_SECTION_PATTERN = re.compile(r"^(#{2,6})\s+(\d+(?:\.\d+)+)(?:\s|$)", re.MULTILINE)
MERMAID_BLOCK_PATTERN = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
ROADMAP_ROW_PATTERN = re.compile(r"^\|\s*((?:DOC|OPEN|ENG)-\d{2})\s*\|", re.MULTILINE)
ROADMAP_REFERENCE_PATTERN = re.compile(r"\b(?:DOC|OPEN|ENG)-\d{2}\b")
ADR_FILENAME_PATTERN = re.compile(r"ADR-(\d{4})(?:-[a-z0-9-]+)?\.md$")
ADR_STATUSES = {"Proposto", "Accettato", "Rifiutato", "Sostituito"}
VERIFICATION_STATUSES = {"Non eseguito", "In corso", "Superato", "Non superato", "Bloccato"}


def markdown_files() -> list[Path]:
    return [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        *sorted((ROOT / ".agents/skills").rglob("*.md")),
        *sorted(
            path
            for path in (ROOT / "docs").rglob("*.md")
            if path != ROOT / "docs/GOOGLE_DOCS_SYNC.md"
        ),
    ]


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
    if parsed.scheme:
        try:
            valid_port = parsed.port is None or 0 <= parsed.port <= 65535
            valid_https = (
                parsed.scheme.lower() == "https"
                and parsed.hostname is not None
                and valid_port
            )
            has_credentials = parsed.username is not None or parsed.password is not None
        except ValueError:
            valid_https = False
            has_credentials = False
        if not valid_https or has_credentials:
            return f"{source.relative_to(ROOT)}: usare un URL HTTPS valido senza credenziali: {destination}"
        return None
    if destination.startswith("//"):
        return f"{source.relative_to(ROOT)}: usare un URL HTTPS esplicito: {destination}"

    raw_path = unquote(parsed.path)
    target = (source.parent / raw_path).resolve() if raw_path else source.resolve()
    if not target.exists():
        return f"{source.relative_to(ROOT)}: percorso locale inesistente: {destination}"

    fragment = unquote(parsed.fragment)
    if fragment and target.is_file() and target.suffix.lower() == ".md":
        if fragment not in heading_anchors(target):
            return f"{source.relative_to(ROOT)}: ancora inesistente: {destination}"

    return None


def validate_traceability() -> list[str]:
    rad_path = ROOT / "docs/RAD.md"
    sdd_path = ROOT / "docs/SDD.md"
    rad_text = rad_path.read_text(encoding="utf-8")
    rad_ids = set(TRACE_ID_PATTERN.findall(rad_text))
    sdd_text = sdd_path.read_text(encoding="utf-8")
    section_start = "### 3.2 DECOMPOSIZIONE DEL SISTEMA"
    section_end = "#### 3.2.1 DIAGRAMMA DEI MODULI"
    if section_start not in sdd_text or section_end not in sdd_text:
        return ["docs/SDD.md: sezione di decomposizione dei moduli non trovata"]

    module_section = sdd_text.split(section_start, 1)[1].split(section_end, 1)[0]
    module_mappings: dict[str, set[str]] = {}
    for line in module_section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in {"Modulo", "---"}:
            continue
        module_mappings.setdefault(cells[0], set()).update(
            TRACE_ID_PATTERN.findall("|".join(cells[2:]))
        )

    module_ids = set().union(*module_mappings.values()) if module_mappings else set()
    errors: list[str] = []
    missing = sorted(rad_ids - module_ids)
    if missing:
        errors.append(
            "docs/SDD.md: requisiti o casi d’uso RAD non mappati a un modulo: "
            + ", ".join(missing)
        )
    unknown = sorted(module_ids - rad_ids)
    if unknown:
        errors.append(
            "docs/SDD.md: requisiti o casi d’uso non presenti nel RAD: " + ", ".join(unknown)
        )

    rad_lines = rad_text.splitlines()
    case_headings = [
        (index, match.group(1))
        for index, line in enumerate(rad_lines)
        if (match := USE_CASE_HEADING_PATTERN.match(line))
    ]
    participants_by_case: dict[str, set[str]] = {}
    for index, (start, case_id) in enumerate(case_headings):
        end = case_headings[index + 1][0] if index + 1 < len(case_headings) else len(rad_lines)
        participants = next(
            (
                match.group(2).strip()
                for line in rad_lines[start + 1 : end]
                if (match := CASE_FIELD_PATTERN.match(line))
                and match.group(1).strip().casefold() == "attori partecipanti"
            ),
            "",
        )
        participants_by_case[case_id] = {
            actor.strip().rstrip(".").casefold()
            for actor in re.split(r",|\s+e\s+", participants)
            if actor.strip()
        }

    fr_start = "### 3.2 REQUISITI FUNZIONALI"
    fr_end = "### 3.3 REQUISITI NON FUNZIONALI"
    if fr_start not in rad_lines or fr_end not in rad_lines:
        return errors + ["docs/RAD.md: sezione requisiti funzionali non trovata per la tracciabilità"]
    start = rad_lines.index(fr_start) + 1
    end = rad_lines.index(fr_end)
    for line in rad_lines[start:end]:
        if not FUNCTIONAL_REQUIREMENT_ROW_PATTERN.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        requirement_id = cells[0]
        linked_cases = set(re.findall(r"UC-\d{2}", cells[4]))
        responsible_actors = {
            actor.strip().casefold()
            for actor in re.split(r"\s+e\s+", cells[1])
            if actor.strip()
        }
        for case_id in linked_cases:
            absent_actors = sorted(responsible_actors - participants_by_case.get(case_id, set()))
            if absent_actors:
                errors.append(
                    f"docs/RAD.md: {requirement_id} dichiara responsabili non presenti in {case_id}: "
                    + ", ".join(absent_actors)
                )
        mapped_cases: set[str] = set()
        for mapping in module_mappings.values():
            if requirement_id in mapping:
                mapped_cases.update(mapping & linked_cases)
        absent_cases = sorted(linked_cases - mapped_cases)
        if absent_cases:
            errors.append(
                f"docs/SDD.md: {requirement_id} non è collegato nei moduli ai casi d’uso RAD: "
                + ", ".join(absent_cases)
            )
    return errors


def validate_roadmap_ids() -> list[str]:
    path = ROOT / "docs/MILESTONES.md"
    content = path.read_text(encoding="utf-8")
    sections = (
        ("## Roadmap", "## Applicazione degli sprint"),
        ("## Decisioni documentali ancora aperte", "## Criterio di completamento della roadmap"),
        ("## Milestone di ingegneria del prodotto", "## Regole di avanzamento"),
    )
    rows: list[str] = []
    errors: list[str] = []
    for start_heading, end_heading in sections:
        if start_heading not in content or end_heading not in content:
            errors.append(f"docs/MILESTONES.md: sezione roadmap mancante: {start_heading}")
            continue
        section = content.split(start_heading, 1)[1].split(end_heading, 1)[0]
        rows.extend(ROADMAP_ROW_PATTERN.findall(section))

    declared = set(rows)

    duplicates = sorted(identifier for identifier, count in Counter(rows).items() if count > 1)
    if duplicates:
        errors.append(f"docs/MILESTONES.md: ID milestone duplicati: {', '.join(duplicates)}")

    undeclared = sorted(set(ROADMAP_REFERENCE_PATTERN.findall(content)) - declared)
    if undeclared:
        errors.append(
            "docs/MILESTONES.md: riferimenti a ID milestone non dichiarati: "
            + ", ".join(undeclared)
        )
    return errors


def validate_adrs() -> list[str]:
    errors: list[str] = []
    declared_ids: list[str] = []
    adr_directory = ROOT / "docs/adr"
    if not adr_directory.exists():
        return errors

    required_metadata = {
        "id",
        "titolo",
        "stato",
        "data",
        "responsabile",
        "revisori",
        "requisiti correlati",
    }
    required_sections = (
        "## Contesto e problema",
        "## Driver decisionali",
        "## Opzioni considerate",
        "## Decisione",
        "## Verifica e revisione",
    )

    for path in sorted(adr_directory.glob("ADR-*.md")):
        label = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8")
        filename_match = ADR_FILENAME_PATTERN.fullmatch(path.name)
        if not filename_match:
            errors.append(f"{label}: nome file ADR non conforme al formato ADR-NNNN.md")
            continue

        metadata_section = content.split("## Metadati", 1)
        if len(metadata_section) != 2:
            errors.append(f"{label}: sezione Metadati non trovata")
            continue
        metadata_text = metadata_section[1].split("## ", 1)[0]
        metadata: dict[str, str] = {}
        for line in metadata_text.splitlines():
            if not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 2 and cells[0].lower() not in {"campo", "---"}:
                metadata[cells[0].casefold()] = cells[1]

        missing_metadata = sorted(key for key in required_metadata if not metadata.get(key))
        if missing_metadata:
            errors.append(f"{label}: metadati mancanti o vuoti: {', '.join(missing_metadata)}")

        expected_id = f"ADR-{filename_match.group(1)}"
        declared_ids.append(expected_id)
        if metadata.get("id") and metadata["id"] != expected_id:
            errors.append(f"{label}: ID {metadata['id']} diverso dal nome file {expected_id}")
        if metadata.get("stato") and metadata["stato"] not in ADR_STATUSES:
            errors.append(
                f"{label}: stato non valido. Usare uno tra: {', '.join(sorted(ADR_STATUSES))}"
            )

        for heading in required_sections:
            if heading not in content.splitlines():
                errors.append(f"{label}: sezione obbligatoria non trovata: {heading}")

        def table_rows(section: str, heading: str) -> list[list[str]]:
            parts = section.split(heading, 1)
            if len(parts) != 2:
                return []
            body = parts[1].split("## ", 1)[0]
            rows: list[list[str]] = []
            for line in body.splitlines():
                if not line.startswith("|"):
                    continue
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    continue
                rows.append(cells)
            return rows

        expected_tables = {
            "## Opzioni considerate": [
                "Opzione",
                "Vantaggi",
                "Costi e rischi",
                "Requisiti soddisfatti o non soddisfatti",
            ],
            "## Verifica e revisione": [
                "Evidenza richiesta",
                "Criterio di accettazione",
                "Responsabile",
                "Esito e riferimento",
            ],
        }
        for heading, expected_headers in expected_tables.items():
            rows = table_rows(content, heading)
            if not rows:
                continue
            if rows[0] != expected_headers:
                errors.append(
                    f"{label}: intestazione tabella non conforme nella sezione {heading[3:]}"
                )
            data_rows = rows[1:]
            minimum_rows = 2 if heading == "## Opzioni considerate" else 1
            if len(data_rows) < minimum_rows:
                errors.append(
                    f"{label}: righe insufficienti nella sezione {heading[3:]}"
                )
            for row_number, row in enumerate(data_rows, start=1):
                if len(row) != len(expected_headers) or any(not cell for cell in row):
                    errors.append(
                        f"{label}: riga {row_number} incompleta nella sezione {heading[3:]}"
                    )

    duplicates = sorted(
        identifier for identifier, count in Counter(declared_ids).items() if count > 1
    )
    if duplicates:
        errors.append("docs/adr: ID ADR duplicati: " + ", ".join(duplicates))

    return errors


def validate_project_style() -> list[str]:
    errors: list[str] = []
    for source in markdown_files():
        content = source.read_text(encoding="utf-8")
        label = source.relative_to(ROOT)
        if chr(0x2014) in content:
            errors.append(f"{label}: usare punteggiatura semplice, senza trattino lungo")
        if ";" in content:
            errors.append(f"{label}: evitare il punto e virgola nella documentazione di progetto")
        if any(match.group(0) != "aegis" for match in re.finditer(r"\baegis\b", content, re.IGNORECASE)):
            errors.append(f"{label}: il nome del prodotto deve essere scritto esattamente aegis")

    project_pattern = re.compile(r"^\|\s*Progetto\s*\|\s*aegis\s*\|\s*$", re.MULTILINE)
    for name in ("docs/RAD.md", "docs/SDD.md"):
        content = (ROOT / name).read_text(encoding="utf-8")
        if not project_pattern.search(content):
            errors.append(f"{name}: il campo Progetto deve contenere esattamente aegis")
    return errors


def mermaid_description_errors(label: str, content: str) -> list[str]:
    errors = []
    for index, match in enumerate(MERMAID_BLOCK_PATTERN.finditer(content), start=1):
        if not re.search(r"^\s*accDescr:\s*\S", match.group(1), re.MULTILINE):
            errors.append(f"{label}: diagramma Mermaid {index} senza descrizione accessibile accDescr")
    return errors


def validate_mermaid_descriptions() -> list[str]:
    errors: list[str] = []
    for path in markdown_files():
        label = path.relative_to(ROOT).as_posix()
        errors.extend(mermaid_description_errors(label, path.read_text(encoding="utf-8")))
    return errors


def validate_document_structure() -> list[str]:
    errors: list[str] = []
    for document in ("RAD.md", "SDD.md"):
        actual_path = ROOT / "docs" / document
        template_path = ROOT / "docs" / "template" / document
        actual = [
            (len(level), number)
            for level, number in NUMBERED_SECTION_PATTERN.findall(
                without_fenced_code(actual_path.read_text(encoding="utf-8"))
            )
        ]
        template = [
            (len(level), number)
            for level, number in NUMBERED_SECTION_PATTERN.findall(
                without_fenced_code(template_path.read_text(encoding="utf-8"))
            )
        ]
        if actual != template:
            errors.append(
                f"docs/{document}: gerarchia delle sezioni numerate diversa dal modello "
                f"docs/template/{document}"
            )
    return errors


def validate_glossaries() -> list[str]:
    errors: list[str] = []
    expected_header = ["Termine", "Definizione"]

    for document in ("RAD.md", "SDD.md"):
        label = f"docs/{document}"
        lines = (ROOT / label).read_text(encoding="utf-8").splitlines()
        headings = [index for index, line in enumerate(lines) if line.strip() == "## GLOSSARIO"]
        if len(headings) != 1:
            errors.append(f"{label}: deve contenere un solo glossario")
            continue

        start = headings[0] + 1
        end = next(
            (index for index in range(start, len(lines)) if re.match(r"^#{1,2}\s", lines[index])),
            len(lines),
        )
        section = lines[start:end]
        table_rows = [line for line in section if line.strip().startswith("|")]
        if len(table_rows) < 3:
            errors.append(f"{label}: tabella del glossario priva di definizioni")
            continue

        header = [cell.strip() for cell in table_rows[0].strip().strip("|").split("|")]
        if header != expected_header:
            errors.append(f"{label}: intestazione del glossario non conforme")

        terms: list[str] = []
        for row_number, row in enumerate(table_rows[2:], start=1):
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if len(cells) != 2 or any(not cell for cell in cells):
                errors.append(f"{label}: voce {row_number} del glossario incompleta")
                continue
            terms.append(cells[0].casefold())

        duplicates = sorted(term for term, count in Counter(terms).items() if count > 1)
        if duplicates:
            errors.append(f"{label}: termini duplicati nel glossario: {', '.join(duplicates)}")

    return errors


def validate_runbook_revision_history() -> list[str]:
    path = ROOT / "docs/template/RUNBOOK.md"
    label = path.relative_to(ROOT).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    heading = "## Registro delle revisioni"
    headings = [index for index, line in enumerate(lines) if line.strip() == heading]
    if len(headings) != 1:
        return [f"{label}: deve contenere una sola sezione Registro delle revisioni"]

    start = headings[0] + 1
    end = next(
        (index for index in range(start, len(lines)) if re.match(r"^#{1,2}\s", lines[index])),
        len(lines),
    )
    table_rows = [line for line in lines[start:end] if line.strip().startswith("|")]
    if len(table_rows) < 3:
        return [f"{label}: registro delle revisioni privo di righe"]

    expected_headers = [
        "Versione",
        "Data",
        "Modifica e motivazione",
        "Autore",
        "Revisore e approvazione",
    ]
    header = [cell.strip() for cell in table_rows[0].strip().strip("|").split("|")]
    errors: list[str] = []
    if header != expected_headers:
        errors.append(f"{label}: intestazione del registro revisioni non conforme")

    for row_number, row in enumerate(table_rows[2:], start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != len(expected_headers) or any(not cell for cell in cells):
            errors.append(f"{label}: riga {row_number} del registro revisioni incompleta")

    return errors


def validate_runbook_operational_coverage() -> list[str]:
    path = ROOT / "docs/template/RUNBOOK.md"
    label = path.relative_to(ROOT).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    required_sections = {
        "## Segnali e diagnosi": [
            "pulizia cache pendente",
            "notifica pendente o con esito ambiguo",
            "coda di moderazione in crescita",
        ],
        "### Ripristino da backup": [
            "object storage",
            "OPEN-05",
            "cache",
            "sincronizzazione",
            "outbox notifiche",
            "worker",
        ],
        "### Recupero dei lavori asincroni": [
            "sincronizzazione",
            "pulizia cache",
            "outbox",
            "esito ambiguo",
            "idempotenza",
            "OPEN-08",
            "ADR-0005",
        ],
        "### Coda di moderazione": [
            "OPEN-12",
            "autorizzazioni",
            "transizioni",
        ],
    }
    errors: list[str] = []
    for heading, required_terms in required_sections.items():
        indexes = [index for index, line in enumerate(lines) if line.strip() == heading]
        section_name = heading.lstrip("#").strip()
        if len(indexes) != 1:
            errors.append(f"{label}: deve contenere una sola sezione {section_name}")
            continue

        start = indexes[0] + 1
        end = next(
            (
                index
                for index in range(start, len(lines))
                if re.match(r"^#{1,3}\s", lines[index])
            ),
            len(lines),
        )
        section = "\n".join(lines[start:end]).casefold()
        missing = [term for term in required_terms if term.casefold() not in section]
        if missing:
            errors.append(
                f"{label}: sezione {section_name} priva di copertura per {', '.join(missing)}"
            )

    return errors


def validate_non_functional_requirements() -> list[str]:
    path = ROOT / "docs/RAD.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    section_start = "### 3.3 REQUISITI NON FUNZIONALI"
    section_end = "### 3.4 VINCOLI"
    if section_start not in lines or section_end not in lines:
        return ["docs/RAD.md: sezione requisiti non funzionali non trovata"]

    start = lines.index(section_start) + 1
    end = lines.index(section_end)
    section = lines[start:end]
    expected_headers = ["ID", "Qualità", "Azione richiesta", "Criterio di verifica", "Responsabile dell’accettazione"]
    evidence_headers = ["ID", "Esito osservato", "Riferimento evidenza"]
    header_lines = [line for line in section if line.startswith("| ID |")]
    if not header_lines:
        return ["docs/RAD.md: tabella NFR senza intestazione"]
    errors: list[str] = []
    if len(header_lines) != 2:
        errors.append("docs/RAD.md: tabelle NFR incomplete o duplicate")
    if [cell.strip() for cell in header_lines[0].strip().strip("|").split("|")] != expected_headers:
        errors.append("docs/RAD.md: intestazione requisiti NFR non conforme al modello")
    if len(header_lines) > 1 and [cell.strip() for cell in header_lines[1].strip().strip("|").split("|")] != evidence_headers:
        errors.append("docs/RAD.md: intestazione registro verifiche NFR non conforme al modello")

    ids: list[str] = []
    evidence_ids: list[str] = []
    evidence_table_started = False
    for line in section:
        if line in header_lines:
            evidence_table_started = line == header_lines[1] if len(header_lines) > 1 else False
            continue
        if not NON_FUNCTIONAL_REQUIREMENT_ROW_PATTERN.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        requirement_id = cells[0]
        if evidence_table_started:
            evidence_ids.append(requirement_id)
            if len(cells) != len(evidence_headers) or not all(cells[1:]):
                errors.append(f"docs/RAD.md: {requirement_id} deve avere esito osservato e riferimento evidenza")
                continue
            result, evidence_reference = cells[1:]
            if result not in VERIFICATION_STATUSES:
                errors.append(f"docs/RAD.md: {requirement_id} ha uno stato di verifica NFR non valido")
            if result == "Non eseguito":
                if evidence_reference != "Da registrare":
                    errors.append(f"docs/RAD.md: {requirement_id} non eseguito deve avere il riferimento `Da registrare`")
            elif not LINK_PATTERN.search(evidence_reference):
                errors.append(f"docs/RAD.md: {requirement_id} con verifica avviata deve collegare un’evidenza consultabile")
        else:
            ids.append(requirement_id)
            if len(cells) != len(expected_headers) or not all(cells[1:]):
                errors.append(f"docs/RAD.md: {requirement_id} deve avere qualità, azione, criterio di verifica e responsabile dell’accettazione")

    if not ids:
        errors.append("docs/RAD.md: tabella NFR senza requisiti")
    duplicates = sorted({requirement_id for requirement_id in ids if ids.count(requirement_id) > 1})
    if duplicates:
        errors.append(f"docs/RAD.md: requisiti non funzionali duplicati: {', '.join(duplicates)}")
    if sorted(ids) != sorted(evidence_ids):
        errors.append("docs/RAD.md: gli ID del registro verifiche NFR devono corrispondere ai requisiti NFR")
    return errors


def validate_nfr_template() -> list[str]:
    path = ROOT / "docs/template/RAD.md"
    if not path.is_file():
        return ["docs/template/RAD.md: modello RAD non trovato"]

    lines = path.read_text(encoding="utf-8").splitlines()
    section_start = "### 3.3 REQUISITI NON FUNZIONALI"
    section_end = "### 3.4 VINCOLI"
    if section_start not in lines or section_end not in lines:
        return ["docs/template/RAD.md: sezione requisiti non funzionali non trovata"]

    section = lines[lines.index(section_start) + 1 : lines.index(section_end)]
    requirement_headers = ["ID", "Qualità", "Azione richiesta", "Criterio di verifica", "Responsabile dell’accettazione"]
    evidence_headers = ["ID", "Esito osservato", "Riferimento evidenza"]
    header_lines = [line for line in section if line.startswith("| ID |")]
    errors: list[str] = []
    if len(header_lines) != 2:
        return ["docs/template/RAD.md: il modello richiede una tabella NFR e un registro verifiche"]
    actual_headers = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in header_lines]
    if actual_headers != [requirement_headers, evidence_headers]:
        errors.append("docs/template/RAD.md: intestazioni NFR non conformi al modello RAD")

    sample_rows = [line for line in section if line.startswith("| NFR-XX |")]
    if len(sample_rows) != 2:
        errors.append("docs/template/RAD.md: servono un esempio NFR e la relativa riga nel registro")
    for index, row in enumerate(sample_rows):
        expected_count = len(requirement_headers) if index == 0 else len(evidence_headers)
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != expected_count or not all(cells[1:]):
            errors.append("docs/template/RAD.md: esempio NFR o registro verifiche incompleto")
            break
    return errors


def validate_functional_requirements() -> list[str]:
    path = ROOT / "docs/RAD.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    section_start = "### 3.2 REQUISITI FUNZIONALI"
    section_end = "### 3.3 REQUISITI NON FUNZIONALI"
    if section_start not in lines or section_end not in lines:
        return ["docs/RAD.md: sezione requisiti funzionali non trovata"]

    start = lines.index(section_start) + 1
    end = lines.index(section_end)
    section = lines[start:end]
    acceptance_heading = "#### CRITERI DI ACCETTAZIONE FR"
    if acceptance_heading in section:
        section = section[: section.index(acceptance_heading)]
    expected_headers = ["ID", "Responsabile dell’azione", "Azione richiesta", "Priorità", "Caso d’uso"]
    header_line = next((line for line in section if line.startswith("| ID |")), None)
    if header_line is None:
        return ["docs/RAD.md: tabella FR senza intestazione"]
    headers = [cell.strip() for cell in header_line.strip().strip("|").split("|")]
    errors: list[str] = []
    if headers != expected_headers:
        errors.append("docs/RAD.md: intestazione tabella FR non conforme al modello")

    ids: list[str] = []
    for line in section:
        if not FUNCTIONAL_REQUIREMENT_ROW_PATTERN.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        requirement_id = cells[0]
        ids.append(requirement_id)
        if len(cells) != len(expected_headers):
            errors.append(f"docs/RAD.md: {requirement_id} ha un numero di colonne non valido")
            continue
        if any(not cell for cell in cells[1:]):
            errors.append(
                f"docs/RAD.md: {requirement_id} deve avere responsabile, azione, priorità e caso d’uso"
            )
        if cells[3] and cells[3] not in {"Must", "Should", "Could"}:
            errors.append(f"docs/RAD.md: priorità non valida per {requirement_id}: {cells[3]}")
        if cells[4] and not re.fullmatch(r"UC-\d{2}(?:,\s*UC-\d{2})*", cells[4]):
            errors.append(f"docs/RAD.md: {requirement_id} senza caso d’uso valido")

    if not ids:
        errors.append("docs/RAD.md: tabella FR senza requisiti")
    duplicates = sorted({requirement_id for requirement_id in ids if ids.count(requirement_id) > 1})
    if duplicates:
        errors.append(f"docs/RAD.md: requisiti funzionali duplicati: {', '.join(duplicates)}")
    return errors


def validate_functional_acceptance() -> list[str]:
    path = ROOT / "docs/RAD.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    section_start = "### 3.2 REQUISITI FUNZIONALI"
    criteria_heading = "#### CRITERI DI ACCETTAZIONE FR"
    evidence_heading = "#### REGISTRO DELLE VERIFICHE FR"
    section_end = "### 3.3 REQUISITI NON FUNZIONALI"
    if any(heading not in lines for heading in (section_start, criteria_heading, evidence_heading, section_end)):
        return ["docs/RAD.md: criteri di accettazione o registro delle verifiche FR non trovati"]

    section = lines[lines.index(section_start) + 1 : lines.index(section_end)]
    criteria_start = section.index(criteria_heading) + 1
    evidence_start = section.index(evidence_heading)
    criteria_lines = section[criteria_start:evidence_start]
    evidence_lines = section[evidence_start + 1 :]
    criteria_headers = ["ID", "Criterio di accettazione"]
    evidence_headers = ["ID", "Esito osservato", "Riferimento evidenza"]
    errors: list[str] = []

    def table_header(block: list[str], expected: list[str], label: str) -> None:
        header = next((line for line in block if line.startswith("| ID |")), None)
        actual = [cell.strip() for cell in header.strip().strip("|").split("|")] if header else []
        if actual != expected:
            errors.append(f"docs/RAD.md: intestazione {label} non conforme al modello")

    table_header(criteria_lines, criteria_headers, "criteri FR")
    table_header(evidence_lines, evidence_headers, "registro verifiche FR")

    primary_header = "| ID | Responsabile dell’azione | Azione richiesta | Priorità | Caso d’uso |"
    if primary_header not in section:
        return errors + ["docs/RAD.md: tabella principale dei requisiti FR non trovata"]
    rad_start = section.index(primary_header)
    primary_lines = section[rad_start + 1 : section.index(criteria_heading)]
    requirement_ids: list[str] = []
    for line in primary_lines:
        if FUNCTIONAL_REQUIREMENT_ROW_PATTERN.match(line):
            requirement_ids.append(line.strip().strip("|").split("|")[0].strip())

    def data_rows(block: list[str], pattern: re.Pattern[str]) -> list[list[str]]:
        return [
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in block
            if pattern.match(line)
        ]

    criteria_rows = data_rows(criteria_lines, FUNCTIONAL_REQUIREMENT_ROW_PATTERN)
    evidence_rows = data_rows(evidence_lines, FUNCTIONAL_REQUIREMENT_ROW_PATTERN)
    for row in criteria_rows:
        if len(row) != len(criteria_headers) or not row[1]:
            errors.append(f"docs/RAD.md: {row[0]} deve avere un criterio di accettazione osservabile")
    for row in evidence_rows:
        if len(row) != len(evidence_headers) or not all(row[1:]):
            errors.append(f"docs/RAD.md: {row[0]} deve avere esito osservato e riferimento evidenza")
            continue
        result, evidence_reference = row[1:]
        if result not in VERIFICATION_STATUSES:
            errors.append(f"docs/RAD.md: {row[0]} ha uno stato di verifica FR non valido")
        if result == "Non eseguito":
            if evidence_reference != "Da registrare":
                errors.append(f"docs/RAD.md: {row[0]} non eseguito deve avere il riferimento `Da registrare`")
        elif not LINK_PATTERN.search(evidence_reference):
            errors.append(f"docs/RAD.md: {row[0]} con verifica avviata deve collegare un’evidenza consultabile")

    criteria_ids = [row[0] for row in criteria_rows]
    evidence_ids = [row[0] for row in evidence_rows]
    for label, identifiers in (("criteri", criteria_ids), ("registro verifiche", evidence_ids)):
        duplicates = sorted(identifier for identifier, count in Counter(identifiers).items() if count > 1)
        if duplicates:
            errors.append(f"docs/RAD.md: ID FR duplicati nei {label}: {', '.join(duplicates)}")
        if sorted(identifiers) != sorted(requirement_ids):
            errors.append(f"docs/RAD.md: gli ID FR dei {label} devono corrispondere ai requisiti funzionali")
    return errors


def validate_fr_template() -> list[str]:
    path = ROOT / "docs/template/RAD.md"
    if not path.is_file():
        return ["docs/template/RAD.md: modello RAD non trovato"]
    lines = path.read_text(encoding="utf-8").splitlines()
    section_start = "### 3.2 REQUISITI FUNZIONALI"
    criteria_heading = "#### CRITERI DI ACCETTAZIONE FR"
    evidence_heading = "#### REGISTRO DELLE VERIFICHE FR"
    section_end = "### 3.3 REQUISITI NON FUNZIONALI"
    if any(heading not in lines for heading in (section_start, criteria_heading, evidence_heading, section_end)):
        return ["docs/template/RAD.md: criteri e registro verifiche FR non trovati"]

    section = lines[lines.index(section_start) + 1 : lines.index(section_end)]
    expected_headers = [
        ["ID", "Attore o sistema responsabile", "Azione richiesta", "Priorità", "Caso d’uso collegato"],
        ["ID", "Criterio di accettazione"],
        ["ID", "Esito osservato", "Riferimento evidenza"],
    ]
    header_lines = [line for line in section if line.startswith("| ID |")]
    errors: list[str] = []
    actual_headers = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in header_lines]
    if actual_headers != expected_headers:
        errors.append("docs/template/RAD.md: intestazioni FR non conformi al modello RAD")

    samples = [line for line in section if line.startswith("| FR-XX |")]
    if len(samples) != 3:
        errors.append("docs/template/RAD.md: servono esempio FR, criterio e riga del registro verifiche")
    for index, sample in enumerate(samples):
        cells = [cell.strip() for cell in sample.strip().strip("|").split("|")]
        if len(cells) != len(expected_headers[index]) or not all(cells[1:]):
            errors.append("docs/template/RAD.md: esempio FR, criterio o registro verifiche incompleto")
            break
    return errors


def validate_use_case_specs() -> list[str]:
    rad_path = ROOT / "docs/RAD.md"
    lines = rad_path.read_text(encoding="utf-8").splitlines()
    headings = [(index, match.group(1)) for index, line in enumerate(lines) if (match := USE_CASE_HEADING_PATTERN.match(line))]
    case_ids = [case_id for _, case_id in headings]
    errors: list[str] = []

    duplicates = sorted({case_id for case_id in case_ids if case_ids.count(case_id) > 1})
    if duplicates:
        errors.append(f"docs/RAD.md: casi d’uso duplicati: {', '.join(duplicates)}")

    required_fields = {
        "attori partecipanti",
        "condizioni d’ingresso",
        "condizioni d’uscita",
        "requisiti qualitativi",
        "flusso degli eventi",
    }
    for index, (start, case_id) in enumerate(headings):
        end = headings[index + 1][0] if index + 1 < len(headings) else len(lines)
        section = lines[start + 1 : end]
        fields = {
            match.group(1).strip().lower(): match.group(2).strip()
            for line in section
            if (match := CASE_FIELD_PATTERN.match(line))
        }
        missing = sorted(field for field in required_fields if not fields.get(field))
        if missing:
            errors.append(f"docs/RAD.md: {case_id} senza campi compilati: {', '.join(missing)}")

    table_case_ids: set[str] = set()
    for line in lines:
        if FUNCTIONAL_REQUIREMENT_ROW_PATTERN.match(line):
            table_case_ids.update(re.findall(r"UC-\d{2}", line))

    undefined = sorted(table_case_ids - set(case_ids))
    unreferenced = sorted(set(case_ids) - table_case_ids)
    if undefined:
        errors.append(f"docs/RAD.md: casi d’uso referenziati ma non specificati: {', '.join(undefined)}")
    if unreferenced:
        errors.append(f"docs/RAD.md: casi d’uso non collegati a requisiti funzionali: {', '.join(unreferenced)}")

    return errors


def validate_use_case_diagram() -> list[str]:
    path = ROOT / "docs/RAD.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    heading = "##### Diagramma globale"
    if heading not in lines:
        return ["docs/RAD.md: diagramma globale dei casi d’uso non trovato"]

    heading_index = lines.index(heading)
    opening_index = next(
        (
            index
            for index in range(heading_index + 1, len(lines))
            if lines[index].strip() == "```mermaid"
        ),
        None,
    )
    if opening_index is None:
        return ["docs/RAD.md: blocco Mermaid del diagramma dei casi d’uso non trovato"]
    closing_index = next(
        (
            index
            for index in range(opening_index + 1, len(lines))
            if lines[index].strip() == "```"
        ),
        None,
    )
    if closing_index is None:
        return ["docs/RAD.md: blocco Mermaid del diagramma dei casi d’uso non chiuso"]

    diagram = "\n".join(lines[opening_index + 1 : closing_index])
    case_ids = {
        match.group(1)
        for line in lines
        if (match := USE_CASE_HEADING_PATTERN.match(line))
    }
    node_matches = USE_CASE_DIAGRAM_NODE_PATTERN.findall(diagram)
    label_ids = [f"UC-{label_number}" for _, _, label_number in node_matches]
    diagram_ids = set(label_ids)
    errors: list[str] = []
    duplicates = sorted(case_id for case_id, count in Counter(label_ids).items() if count > 1)
    if duplicates:
        errors.append(
            "docs/RAD.md: ID ripetuti nel diagramma dei casi d’uso: " + ", ".join(duplicates)
        )
    missing = sorted(case_ids - diagram_ids)
    if missing:
        errors.append("docs/RAD.md: casi d’uso assenti dal diagramma: " + ", ".join(missing))
    unknown = sorted(diagram_ids - case_ids)
    if unknown:
        errors.append("docs/RAD.md: ID del diagramma senza specifica: " + ", ".join(unknown))

    node_labels: dict[str, list[str]] = {}
    for node_id, node_number, label_number in node_matches:
        node_labels.setdefault(f"UC-{label_number}", []).append(node_id)
        if node_number != label_number:
            errors.append(
                f"docs/RAD.md: nodo {node_id} non corrisponde all’etichetta UC-{label_number}"
            )
    for case_id in sorted(case_ids):
        if len(node_labels.get(case_id, [])) != 1:
            errors.append(f"docs/RAD.md: {case_id} deve avere un solo nodo nel diagramma")

    actor_labels = dict(USE_CASE_DIAGRAM_ACTOR_PATTERN.findall(diagram))
    associated_cases: set[str] = set()
    actor_case_edges: set[tuple[str, str]] = set()
    for actor_id, case_node in USE_CASE_DIAGRAM_EDGE_PATTERN.findall(diagram):
        case_id = f"UC-{case_node[2:]}"
        if actor_id not in actor_labels:
            errors.append(f"docs/RAD.md: attore {actor_id} non dichiarato nel diagramma")
        if case_id not in case_ids:
            errors.append(
                f"docs/RAD.md: associazione del diagramma verso caso non dichiarato {case_id}"
            )
        associated_cases.add(case_id)
        actor_case_edges.add((actor_id, case_id))
    for case_id in sorted(case_ids - associated_cases):
        errors.append(f"docs/RAD.md: {case_id} non è collegato ad alcun attore nel diagramma")

    declared_actors = {actor_id for actor_id, _ in actor_case_edges}
    for actor_id in sorted(set(actor_labels) - declared_actors):
        errors.append(f"docs/RAD.md: attore {actor_id} senza associazioni nel diagramma")

    case_headings = [
        (index, match.group(1))
        for index, line in enumerate(lines)
        if (match := USE_CASE_HEADING_PATTERN.match(line))
    ]
    for index, (start, case_id) in enumerate(case_headings):
        end = case_headings[index + 1][0] if index + 1 < len(case_headings) else len(lines)
        fields = {
            match.group(1).strip().lower(): match.group(2).strip().rstrip(".")
            for line in lines[start + 1 : end]
            if (match := CASE_FIELD_PATTERN.match(line))
        }
        raw_participants = fields.get("attori partecipanti", "").casefold()
        unmatched_participants = raw_participants
        for actor_id, label in actor_labels.items():
            normalized_label = label.casefold()
            if normalized_label not in raw_participants:
                continue
            unmatched_participants = unmatched_participants.replace(normalized_label, "", 1)
            if (actor_id, case_id) not in actor_case_edges:
                errors.append(
                    f"docs/RAD.md: attore partecipante {label} non collegato a {case_id} nel diagramma"
                )
        unmatched_participants = re.sub(r"\bsistema\b", "", unmatched_participants)
        unmatched_participants = re.sub(r"\be\b|[\s,.]+", "", unmatched_participants)
        if unmatched_participants:
            errors.append(
                f"docs/RAD.md: attore partecipante non rappresentato nel diagramma per {case_id}"
            )
    return errors


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
    errors.extend(validate_traceability())
    errors.extend(validate_roadmap_ids())
    errors.extend(validate_adrs())
    errors.extend(validate_functional_requirements())
    errors.extend(validate_use_case_specs())
    errors.extend(validate_use_case_diagram())
    errors.extend(validate_project_style())
    errors.extend(validate_mermaid_descriptions())
    errors.extend(validate_document_structure())
    errors.extend(validate_glossaries())
    errors.extend(validate_runbook_revision_history())
    errors.extend(validate_runbook_operational_coverage())
    errors.extend(validate_non_functional_requirements())
    errors.extend(validate_nfr_template())
    errors.extend(validate_functional_acceptance())
    errors.extend(validate_fr_template())

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(
        "Documentazione valida: link, ancore, struttura, milestone, requisiti, casi d’uso, "
        "diagramma dei casi, glossari, runbook, ADR, tracciabilità, descrizioni accessibili e stile del nome "
        f"verificati in {len(files)} file Markdown."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
