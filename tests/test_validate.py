from pathlib import Path

from corpus_tools.validate import ValidationReport, validate_file, validate_row

FIXTURES = Path(__file__).parent


def _report_for(row: dict) -> ValidationReport:
    rep = ValidationReport()
    validate_row(row, 2, rep)
    return rep


def test_valid_row_passes():
    assert _report_for({"abbr": "isc", "expansion": "incident summary card",
                        "domain": "itsm"}).ok


def test_unknown_domain_fails():
    rep = _report_for({"abbr": "x", "expansion": "something", "domain": "nope"})
    assert not rep.ok and "unknown domain" in rep.errors[0]


def test_validate_file_counts_rows(tmp_path):
    csv = tmp_path / "c.csv"
    csv.write_text("abbr,expansion,domain\nisc,incident summary card,itsm\n")
    schema = tmp_path / "s.json"
    schema.write_text('{"type": "object"}')
    rep = validate_file(csv, schema)
    assert rep.ok and rep.rows == 1
