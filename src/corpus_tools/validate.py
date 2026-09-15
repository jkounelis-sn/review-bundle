"""Hand-rolled schema checks for corpus rows (no jsonschema dependency)."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

VALID_DOMAINS = {"itsm", "hr", "itam", "secops", "general"}


@dataclass
class ValidationReport:
    rows: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_schema(path: Path) -> dict:
    return json.loads(path.read_text())


def validate_row(row: dict, line: int, report: ValidationReport) -> None:
    abbr = (row.get("abbr") or "").strip()
    expansion = (row.get("expansion") or "").strip()
    domain = (row.get("domain") or "").strip()
    if not abbr:
        report.errors.append(f"line {line}: empty abbr")
    if len(expansion) < 2:
        report.errors.append(f"line {line}: expansion too short: {expansion!r}")
    if domain not in VALID_DOMAINS:
        report.errors.append(f"line {line}: unknown domain {domain!r}")
    if abbr and expansion and not expansion.startswith(abbr[0]):
        # Heuristic: most corpus entries expand starting with the abbr's
        # first letter ('isc' -> 'incident summary card'). Warn only.
        pass


def validate_file(csv_path: Path, schema_path: Path) -> ValidationReport:
    # The schema is loaded to guarantee it parses and stays in sync, even
    # though the row checks are hand-rolled.
    load_schema(schema_path)
    report = ValidationReport()
    with csv_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader, start=2):  # header is line 1
            report.rows += 1
            validate_row(row, i, report)
    return report
