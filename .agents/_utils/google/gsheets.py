#!/usr/bin/env python3
"""Google Sheets CLI: create, read, update, export."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve()
sys.path.insert(0, str(_SCRIPT.parent))

from bootstrap import (  # noqa: E402
    exit_on_missing_dependency,
    open_in_browser,
    print_result,
    setup_paths,
)

setup_paths(_SCRIPT)

try:
    from cli_common import (
        add_folder_flag,
        add_open_flag,
        parse_file_id,
        resolve_out_path,
    )
    from config import OUTPUT_DIR
    from sheets_io import (
        create_sheet,
        export_sheet_csv,
        read_sheet,
        update_sheet,
        values_to_csv_text,
    )
except ImportError as exc:
    exit_on_missing_dependency(exc)
    raise


def cmd_create(args: argparse.Namespace) -> int:
    csv_path = Path(args.from_file) if args.from_file else None
    result = create_sheet(title=args.title, csv_path=csv_path, folder_id=args.folder)
    print_result(
        kind="spreadsheet",
        file_id=result["id"],
        url=result["url"],
        title=result["title"],
    )
    if args.open:
        open_in_browser(result["url"])
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    file_id = parse_file_id(args.target)
    values = read_sheet(file_id, a1_range=args.range)
    text = values_to_csv_text(values)
    if args.out:
        out = resolve_out_path(args.out, f"{file_id}.csv", OUTPUT_DIR)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"wrote: {out}")
    else:
        sys.stdout.write(text)
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    file_id = parse_file_id(args.target)
    result = update_sheet(
        file_id, csv_path=Path(args.from_file), a1_range=args.range or "A1"
    )
    print_result(kind="spreadsheet", file_id=result["id"], url=result["url"])
    if args.open:
        open_in_browser(result["url"])
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    file_id = parse_file_id(args.target)
    out = resolve_out_path(args.out, f"{file_id}.csv", OUTPUT_DIR)
    path = export_sheet_csv(file_id, out_path=out, a1_range=args.range)
    print(f"wrote: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Sheets tools for design-ai-fuel")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create a Sheet (optionally from CSV)")
    create.add_argument("--title", required=True)
    create.add_argument("--from", dest="from_file", metavar="FILE.csv")
    add_folder_flag(create)
    add_open_flag(create)
    create.set_defaults(func=cmd_create)

    read = sub.add_parser("read", help="Read a Sheet as CSV")
    read.add_argument("target", help="Sheet URL or id")
    read.add_argument("--range", dest="range", metavar="A1")
    read.add_argument("--out", metavar="PATH")
    read.set_defaults(func=cmd_read)

    update = sub.add_parser("update", help="Update a Sheet from CSV")
    update.add_argument("target", help="Sheet URL or id")
    update.add_argument("--from", dest="from_file", metavar="FILE.csv", required=True)
    update.add_argument("--range", dest="range", metavar="A1", default="A1")
    add_open_flag(update)
    update.set_defaults(func=cmd_update)

    export = sub.add_parser("export", help="Export a Sheet as CSV")
    export.add_argument("target", help="Sheet URL or id")
    export.add_argument("--range", dest="range", metavar="A1")
    export.add_argument("--out", metavar="PATH")
    export.set_defaults(func=cmd_export)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
