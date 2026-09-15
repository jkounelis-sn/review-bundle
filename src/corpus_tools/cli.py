"""CLI entry points: validate / report / sync-status."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .report import render_validation_md
from .validate import validate_file

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = REPO_ROOT / "deps" / "corpus"


def _cmd_validate(args: argparse.Namespace) -> int:
    report = validate_file(CORPUS_DIR / "data" / "corpus.csv", CORPUS_DIR / "schema.json")
    print(render_validation_md(report, "vendor-corpus"))
    return 0 if report.ok else 1


def _cmd_sync_status(args: argparse.Namespace) -> int:
    import subprocess

    rev = subprocess.run(
        ["git", "-C", str(CORPUS_DIR), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True, check=False,
    ).stdout.strip()
    upstream = subprocess.run(
        ["git", "-C", str(CORPUS_DIR), "rev-parse", "--short", "origin/main"],
        capture_output=True, text=True, check=False,
    ).stdout.strip()
    state = "in sync" if rev and rev == upstream else "sync pending"
    print(f"corpus HEAD: {rev or 'unknown'} (upstream: {upstream or 'unknown'}) — {state}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="corpus-tool")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="validate deps/corpus against its schema")
    sub.add_parser("sync-status", help="show vendored corpus sync state")
    args = parser.parse_args(argv)
    if args.command == "validate":
        return _cmd_validate(args)
    return _cmd_sync_status(args)


if __name__ == "__main__":
    sys.exit(main())
