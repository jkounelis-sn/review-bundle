"""Markdown rendering for validation results and review deltas."""
from __future__ import annotations

from .validate import ValidationReport


def render_validation_md(report: ValidationReport, dataset: str) -> str:
    status = "PASS" if report.ok else "FAIL"
    lines = [
        f"## Corpus validation — {status}",
        "",
        f"- dataset: `{dataset}`",
        f"- rows checked: {report.rows}",
        f"- errors: {len(report.errors)}",
    ]
    if report.errors:
        lines += ["", "### Errors"] + [f"- {e}" for e in report.errors]
    return "\n".join(lines) + "\n"


def render_delta_summary(old_ver: str, new_ver: str, added: int, fixed: int) -> str:
    return (
        f"Corpus refresh {old_ver} → {new_ver}: "
        f"{added} abbreviation(s) added, {fixed} correction(s). "
        "See deps/corpus/CHANGELOG for row-level detail.\n"
    )
