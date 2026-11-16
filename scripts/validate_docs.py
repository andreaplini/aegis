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
TRACE_ID_PATTERN = re.compile(r"\b(?:FR|NFR|UC)-\d{2}\b")
USE_CASE_HEADING_PATTERN = re.compile(r"^######\s+(UC-\d{2})\b")
FUNCTIONAL_REQUIREMENT_ROW_PATTERN = re.compile(r"^\|\s*(FR-\d{2})\s*\|")
NON_FUNCTIONAL_REQUIREMENT_ROW_PATTERN = re.compile(r"^\|\s*(NFR-\d{2})\s*\|")
CASE_FIELD_PATTERN = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
NUMBERED_SECTION_PATTERN = re.compile(r"^(#{2,6})\s+(\d+(?:\.\d+)+)(?:\s|$)", re.MULTILINE)


def markdown_files() -> list[Path]:
    return [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        *sorted((ROOT / ".agents/skills").rglob("*.md")),
        *sorted((ROOT / "docs").rglob("*.md")),
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


def validate_project_style() -> list[str]:
    errors: list[str] = []
    for source in markdown_files():
        content = source.read_text(encoding="utf-8")
        label = source.relative_to(ROOT)
        if chr(0x2014) in content:
            errors.append(f"{label}: usare punteggiatura semplice, senza trattino lungo")
        if any(match.group(0) != "aegis" for match in re.finditer(r"\baegis\b", content, re.IGNORECASE)):
            errors.append(f"{label}: il nome del prodotto deve essere scritto esattamente aegis")

    project_pattern = re.compile(r"^\|\s*Progetto\s*\|\s*aegis\s*\|\s*$", re.MULTILINE)
    for name in ("docs/RAD.md", "docs/SDD.md"):
        content = (ROOT / name).read_text(encoding="utf-8")
        if not project_pattern.search(content):
            errors.append(f"{name}: il campo Progetto deve contenere esattamente aegis")
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
    expected_headers = ["ID", "Qualità", "Azione richiesta", "Criterio di verifica"]
    header_line = next((line for line in section if line.startswith("| ID |")), None)
    if header_line is None:
        return ["docs/RAD.md: tabella NFR senza intestazione"]
    headers = [cell.strip() for cell in header_line.strip().strip("|").split("|")]
    errors: list[str] = []
    if headers != expected_headers:
        errors.append("docs/RAD.md: intestazione tabella NFR non conforme al modello")

    ids: list[str] = []
    for line in section:
        if not NON_FUNCTIONAL_REQUIREMENT_ROW_PATTERN.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        requirement_id = cells[0]
        ids.append(requirement_id)
        if len(cells) != len(expected_headers):
            errors.append(f"docs/RAD.md: {requirement_id} ha un numero di colonne non valido")
            continue
        if not cells[1] or not cells[2] or not cells[3]:
            errors.append(f"docs/RAD.md: {requirement_id} deve avere qualità, azione e criterio di verifica")

    if not ids:
        errors.append("docs/RAD.md: tabella NFR senza requisiti")
    duplicates = sorted({requirement_id for requirement_id in ids if ids.count(requirement_id) > 1})
    if duplicates:
        errors.append(f"docs/RAD.md: requisiti non funzionali duplicati: {', '.join(duplicates)}")
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
    errors.extend(validate_functional_requirements())
    errors.extend(validate_use_case_specs())
    errors.extend(validate_project_style())
    errors.extend(validate_document_structure())
    errors.extend(validate_non_functional_requirements())

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"Documentazione valida: link, ancore, struttura, requisiti, casi d’uso, tracciabilità e stile del nome verificati in {len(files)} file Markdown.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
